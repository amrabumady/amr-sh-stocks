"""
Parameter Optimizer Module
Handles optimization of top_k and voting_days parameters
"""

import pandas as pd
import numpy as np
import os
import pickle
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
        Run full parameter optimization with automatic prediction generation
        """
        logger.info("Starting parameter optimization...")
        
        # Ensure predictions directory exists
        os.makedirs(predictions_dir, exist_ok=True)
        
        # Get tickers
        if not self.data_handler.tickers:
            self.data_handler.get_tickers()
        
        if not self.data_handler.tickers:
            logger.error("No tickers available")
            return {"error": "Could not fetch ticker list"}
        
        # Get dates
        yesterday = pd.Timestamp.today().normalize() - pd.Timedelta(days=1)
        dates = self.data_handler.get_trading_days(
            yesterday.strftime("%Y-%m-%d"),
            lookback_days + 30
        )
        
        if not dates or len(dates) < 10:
            logger.error("Insufficient trading dates")
            return {"error": f"Only {len(dates)} trading dates found. Need at least 10."}
        
        logger.info(f"Found {len(dates)} trading dates")
        
        # Download data
        start_date = (yesterday - pd.Timedelta(days=lookback_days)).date().isoformat()
        end_date = yesterday.date().isoformat()
        
        logger.info(f"Downloading data from {start_date} to {end_date}")
        bars = self.data_handler.download_bars(
            self.data_handler.tickers,
            start=start_date,
            end=end_date,
            show_progress=False
        )
        
        if not bars:
            logger.error("No data downloaded")
            return {"error": "Failed to download stock data. Check internet connection."}
        
        logger.info(f"Downloaded data for {len(bars)} stocks")
        
        # Generate predictions for all dates
        logger.info("Generating predictions...")
        prediction_dates = dates[-min(30, len(dates)):]  # Last 30 days or all available
        
        generated_count = 0
        for date in prediction_dates:
            date_str = date.strftime("%Y-%m-%d")
            pred_file = os.path.join(predictions_dir, f"{date_str}.pkl")
            
            # Skip if predictions already exist
            if os.path.exists(pred_file):
                continue
            
            # Generate predictions for this date
            daily_predictions = []
            for ticker, df in bars.items():
                df_filtered = df[df.index <= date]
                if len(df_filtered) >= 60:  # Minimum data requirement
                    try:
                        prediction = self.model_trainer.train_and_predict(
                            df_filtered, vol_window=20, pct_window=20
                        )
                        if prediction is not None:
                            daily_predictions.append((ticker, prediction))
                    except Exception as e:
                        logger.warning(f"Failed to predict {ticker}: {e}")
                        continue
            
            if daily_predictions:
                # Sort by prediction
                daily_predictions.sort(key=lambda x: x[1], reverse=True)
                
                # Save predictions
                try:
                    with open(pred_file, 'wb') as f:
                        pickle.dump(daily_predictions, f)
                    generated_count += 1
                except Exception as e:
                    logger.error(f"Failed to save predictions for {date_str}: {e}")
        
        logger.info(f"Generated predictions for {generated_count} dates")
        
        # Verify predictions exist
        available_pred_files = [f for f in os.listdir(predictions_dir) if f.endswith('.pkl')]
        if len(available_pred_files) < 5:
            return {"error": f"Only {len(available_pred_files)} prediction files generated. Need at least 5 for optimization."}
        
        logger.info(f"Found {len(available_pred_files)} prediction files")
        
        # Calculate returns
        returns_df = self.data_handler.compute_daily_returns(bars)
        
        if returns_df.empty:
            logger.error("Could not compute returns")
            return {"error": "Failed to compute stock returns from data."}
        
        logger.info(f"Computed returns matrix: {returns_df.shape}")
        
        # Test all parameter combinations
        cases = list(product(top_k_range, voting_range))
        results = []
        
        logger.info(f"Testing {len(cases)} parameter combinations...")
        
        for top_k, voting_days in cases:
            # Get predictions for each day using voting
            predictions_by_day = {}
            
            for day in dates:
                try:
                    preds = self.voting_predictions(
                        dates, day, voting_days, top_k, predictions_dir
                    )
                    if preds:
                        predictions_by_day[day] = preds
                except Exception as e:
                    logger.warning(f"Voting failed for {day}: {e}")
                    continue
            
            # Skip if no predictions available
            if not predictions_by_day:
                logger.warning(f"No predictions for top_k={top_k}, voting_days={voting_days}")
                continue
            
            # Run simulation
            try:
                final_equity, curve = self.simulate_portfolio(
                    dates, returns_df, predictions_by_day, top_k
                )
                
                results.append({
                    "top_k": top_k,
                    "voting_days": voting_days,
                    "final_equity": round(final_equity, 2),
                    "equity_curve": curve
                })
            except Exception as e:
                logger.error(f"Simulation failed for top_k={top_k}, voting_days={voting_days}: {e}")
                continue
        
        # Check if we have any successful results
        # Filter for results with non-empty curves and positive equity
        successful_results = []
        for r in results:
            try:
                if (isinstance(r.get("equity_curve"), pd.DataFrame) and 
                    not r["equity_curve"].empty and 
                    r.get("final_equity", 0) > 0):
                    successful_results.append(r)
            except Exception as e:
                logger.warning(f"Invalid result entry: {e}")
                continue
        
        if not successful_results:
            logger.error(f"No successful simulations out of {len(results)} attempts")
            return {
                "error": "All optimization attempts failed.",
                "details": f"Tried {len(cases)} combinations, {len(results)} ran but none succeeded.",
                "suggestion": "Try reducing lookback_days to 180-365 or using smaller parameter ranges (1-5)",
                "attempted": len(cases),
                "completed": len(results)
            }
        
        logger.info(f"Successful simulations: {len(successful_results)} out of {len(cases)}")
        
        # Find best parameters
        best_result = max(successful_results, key=lambda x: x.get("final_equity", 0))
        
        # Validate best_result has required fields
        required_fields = ["top_k", "voting_days", "final_equity"]
        for field in required_fields:
            if field not in best_result:
                logger.error(f"Best result missing required field: {field}")
                return {
                    "error": "Optimization completed but results are invalid",
                    "details": f"Missing required field: {field}",
                    "suggestion": "This is a bug. Please report it with your settings."
                }
        
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
            "successful_count": len(successful_results),
            "total_attempts": len(cases),
            "heatmap_data": np.array(heatmap_data),
            "top_k_labels": top_k_labels,
            "voting_days_labels": voting_labels
        }
