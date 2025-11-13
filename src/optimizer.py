"""
Parameter Optimizer Module
Handles optimization of top_k and voting_days parameters
"""

import pandas as pd
import numpy as np
import logging
from typing import List, Dict, Tuple
from itertools import product
from tqdm import tqdm

from src.data_handler import DataHandler
from src.model_trainer import ModelTrainer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ParameterOptimizer:
    """Optimizes top_k and voting_days parameters through backtesting"""
    
    def __init__(self, start_equity: float = 100.0):
        self.start_equity = start_equity
        self.data_handler = DataHandler()
        self.model_trainer = ModelTrainer()
        
    def voting_predictions(
        self,
        dates: List[pd.Timestamp],
        last_date: pd.Timestamp,
        voting_days: int,
        top_k: int,
        predictions_dir: str = "data/predictions"
    ) -> List[str]:
        """
        Get top stocks based on voting across multiple days
        
        Args:
            dates: All available trading dates
            last_date: Last date to consider
            voting_days: Number of recent days to vote
            top_k: Number of top stocks to return
            predictions_dir: Directory containing prediction files
            
        Returns:
            List of top-voted ticker symbols
        """
        # Get relevant dates (up to last_date)
        relevant_dates = [d for d in dates if d <= last_date]
        window_days = sorted(relevant_dates)[-voting_days:]
        
        # Count votes and scores
        vote_counts = {}
        vote_scores = {}
        
        for day in window_days:
            # Load predictions for this day
            predictions = self.model_trainer.load_predictions(
                day.strftime("%Y-%m-%d"),
                predictions_dir
            )
            
            if not predictions:
                continue
            
            # Vote for top_k stocks
            for ticker, score in predictions[:top_k]:
                vote_counts[ticker] = vote_counts.get(ticker, 0) + 1
                vote_scores.setdefault(ticker, []).append(score)
        
        if not vote_counts:
            return []
        
        # Sort by vote count (descending), then by mean score (descending)
        sorted_tickers = sorted(
            vote_counts.keys(),
            key=lambda t: (-vote_counts[t], -np.mean(vote_scores.get(t, [0])))
        )
        
        return sorted_tickers[:top_k]
    
    def simulate_portfolio(
        self,
        dates: List[pd.Timestamp],
        returns_df: pd.DataFrame,
        predictions_by_day: Dict[pd.Timestamp, List[str]],
        top_k: int
    ) -> Tuple[float, pd.DataFrame]:
        """
        Simulate portfolio performance with daily rebalancing
        
        Args:
            dates: Trading dates
            returns_df: Daily returns matrix
            predictions_by_day: Predictions for each day
            top_k: Number of stocks to hold
            
        Returns:
            (final_equity, equity_curve_df)
        """
        first_day = dates[0]
        
        if first_day not in predictions_by_day or len(predictions_by_day[first_day]) < top_k:
            return 0.0, pd.DataFrame()
        
        # Initialize holdings
        holdings = predictions_by_day[first_day][:top_k]
        slots = {ticker: self.start_equity / top_k for ticker in holdings}
        
        curve = []
        prev_equity = self.start_equity
        
        for i, day in enumerate(dates):
            if i > 0:
                # Apply returns
                if day in returns_df.index:
                    for ticker in list(slots.keys()):
                        if ticker in returns_df.columns:
                            daily_return = returns_df.at[day, ticker]
                            slots[ticker] *= (1 + daily_return)
                
                # Calculate equity
                total_equity = sum(slots.values())
                daily_pct = ((total_equity - prev_equity) / prev_equity * 100) if prev_equity != 0 else 0.0
                prev_equity = total_equity
                
                # Record state
                row = {
                    "Date": day.strftime("%Y-%m-%d"),
                    "Equity": round(total_equity, 2),
                    "Daily_%": round(daily_pct, 2)
                }
                
                # Add holdings
                for idx, (ticker, value) in enumerate(sorted(slots.items()), 1):
                    row[f"Stock_{idx}"] = ticker
                    row[f"Value_{idx}"] = round(value, 2)
                
                curve.append(row)
                
                # Check if we need to rebalance
                if i + 1 == len(dates):
                    break
                
                # Rebalance for next day
                tomorrow_preds = predictions_by_day.get(dates[i + 1], [])
                
                new_slots = {}
                held = set()
                
                # Keep existing holdings if still in predictions
                for ticker, value in slots.items():
                    if ticker in tomorrow_preds and len(new_slots) < top_k:
                        new_slots[ticker] = value
                        held.add(ticker)
                
                # Add new holdings
                remaining_equity = total_equity - sum(new_slots.values())
                new_allocation = remaining_equity / max(1, top_k - len(new_slots))
                
                for ticker in tomorrow_preds:
                    if len(new_slots) == top_k:
                        break
                    if ticker not in held:
                        new_slots[ticker] = new_allocation
                        held.add(ticker)
                
                slots = new_slots
            
            else:
                # Initial day
                total_equity = self.start_equity
                row = {
                    "Date": day.strftime("%Y-%m-%d"),
                    "Equity": round(total_equity, 2),
                    "Daily_%": 0.0
                }
                
                for idx, (ticker, value) in enumerate(sorted(slots.items()), 1):
                    row[f"Stock_{idx}"] = ticker
                    row[f"Value_{idx}"] = round(value, 2)
                
                curve.append(row)
        
        return total_equity, pd.DataFrame(curve)
    
    def run_optimization(
        self,
        top_k_range: range,
        voting_range: range,
        lookback_days: int = 365,
        predictions_dir: str = "data/predictions"
    ) -> Dict:
        """
        Run full parameter optimization
        
        Args:
            top_k_range: Range of top_k values to test
            voting_range: Range of voting_days to test
            lookback_days: Days to look back for data
            predictions_dir: Directory containing predictions
            
        Returns:
            Dictionary with optimization results
        """
        logger.info("Starting parameter optimization...")
        
        # Get tickers and dates
        self.data_handler.get_tickers()
        
        yesterday = pd.Timestamp.today().normalize() - pd.Timedelta(days=1)
        dates = self.data_handler.get_trading_days(
            yesterday.strftime("%Y-%m-%d"),
            lookback_days + 30
        )
        
        if not dates:
            logger.error("No trading dates available")
            return {}
        
        # Download data
        start_date = (yesterday - pd.Timedelta(days=lookback_days)).date().isoformat()
        end_date = yesterday.date().isoformat()
        
        bars = self.data_handler.download_bars(
            self.data_handler.tickers,
            start=start_date,
            end=end_date,
            show_progress=True
        )
        
        # Calculate returns
        returns_df = self.data_handler.compute_daily_returns(bars)
        
        # Test all parameter combinations
        cases = list(product(top_k_range, voting_range))
        results = []
        
        for top_k, voting_days in tqdm(cases, desc="Testing parameters"):
            # Get predictions for each day
            predictions_by_day = {}
            for day in dates:
                preds = self.voting_predictions(
                    dates, day, voting_days, top_k, predictions_dir
                )
                predictions_by_day[day] = preds
            
            # Run simulation
            final_equity, curve = self.simulate_portfolio(
                dates, returns_df, predictions_by_day, top_k
            )
            
            results.append({
                "top_k": top_k,
                "voting_days": voting_days,
                "final_equity": round(final_equity, 2),
                "equity_curve": curve
            })
        
        # Find best parameters
        successful_results = [r for r in results if not r["equity_curve"].empty]
        
        if not successful_results:
            logger.warning("No successful simulations")
            return {}
        
        best_result = max(successful_results, key=lambda x: x["final_equity"])
        
        # Create heatmap data
        heatmap_data = []
        top_k_labels = sorted(set(r["top_k"] for r in results))
        voting_labels = sorted(set(r["voting_days"] for r in results))
        
        for k in top_k_labels:
            row = []
            for v in voting_labels:
                equity = next(
                    (r["final_equity"] for r in results 
                     if r["top_k"] == k and r["voting_days"] == v),
                    0.0
                )
                row.append(equity)
            heatmap_data.append(row)
        
        return {
            "best_params": {
                "top_k": best_result["top_k"],
                "voting_days": best_result["voting_days"],
                "final_equity": best_result["final_equity"]
            },
            "all_results": results,
            "heatmap_data": np.array(heatmap_data),
            "top_k_labels": top_k_labels,
            "voting_days_labels": voting_labels
        }
