"""
Utility Functions Module
Common utility functions used across the application
"""

import os
import glob
import pandas as pd
import logging
from typing import Dict, Tuple, Optional, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_optim_params(optim_dir: str = "data/optimizations") -> Tuple[Dict, Dict, int, int, str]:
    """
    Load optimal SMA parameters from CSV file
    
    Args:
        optim_dir: Directory containing optimization files
        
    Returns:
        (vol_sma_dict, pct_sma_dict, default_vol, default_pct, filepath)
    """
    files = glob.glob(os.path.join(optim_dir, "sma_optim_*.csv"))
    
    if not files:
        logger.warning("No optimization file found - using defaults (20, 20)")
        return {}, {}, 20, 20, "N/A"
    
    # Get most recent file
    file = max(files, key=os.path.getmtime)
    
    try:
        df = pd.read_csv(file)
        
        vol_sma_dict = dict(zip(df["Ticker"], df["Best_Vol_SMA"]))
        pct_sma_dict = dict(zip(df["Ticker"], df["Best_Pct_SMA"]))
        
        default_vol = round(df["Best_Vol_SMA"].mean())
        default_pct = round(df["Best_Pct_SMA"].mean())
        
        logger.info(f"Loaded optimization parameters from {file}")
        return vol_sma_dict, pct_sma_dict, default_vol, default_pct, file
    
    except Exception as e:
        logger.error(f"Error loading optimization file: {e}")
        return {}, {}, 20, 20, "N/A"


def get_expected_percent(ticker: str, predictions: List[Tuple[str, float]]) -> Optional[float]:
    """
    Get expected percentage for a specific ticker
    
    Args:
        ticker: Ticker symbol to look up
        predictions: List of (ticker, prediction) tuples
        
    Returns:
        Expected percentage or None if not found
    """
    ticker_upper = ticker.upper()
    
    for pred_ticker, percent in predictions:
        if pred_ticker.upper() == ticker_upper:
            return percent
    
    return None


def format_percentage(value: float, decimals: int = 2) -> str:
    """
    Format percentage value with color coding
    
    Args:
        value: Percentage value
        decimals: Number of decimal places
        
    Returns:
        Formatted string
    """
    formatted = f"{value:.{decimals}f}%"
    
    if value > 0:
        return f"🟢 {formatted}"
    elif value < 0:
        return f"🔴 {formatted}"
    else:
        return f"⚪ {formatted}"


def calculate_metrics(equity_curve: pd.DataFrame) -> Dict[str, float]:
    """
    Calculate performance metrics from equity curve
    
    Args:
        equity_curve: DataFrame with Date, Equity, Daily_% columns
        
    Returns:
        Dictionary of metrics
    """
    if equity_curve.empty or "Equity" not in equity_curve.columns:
        return {}
    
    equity = equity_curve["Equity"].values
    returns = equity_curve["Daily_%"].values if "Daily_%" in equity_curve.columns else []
    
    # Total return
    total_return = ((equity[-1] - equity[0]) / equity[0] * 100) if len(equity) > 0 else 0
    
    # Maximum drawdown
    running_max = pd.Series(equity).expanding().max()
    drawdown = (pd.Series(equity) - running_max) / running_max * 100
    max_drawdown = drawdown.min()
    
    # Sharpe ratio (annualized, assuming daily returns)
    if len(returns) > 1:
        mean_return = returns.mean()
        std_return = returns.std()
        sharpe = (mean_return / std_return * (252 ** 0.5)) if std_return != 0 else 0
    else:
        sharpe = 0
    
    # Win rate
    if len(returns) > 0:
        win_rate = (returns > 0).sum() / len(returns) * 100
    else:
        win_rate = 0
    
    return {
        "Total Return (%)": round(total_return, 2),
        "Max Drawdown (%)": round(max_drawdown, 2),
        "Sharpe Ratio": round(sharpe, 2),
        "Win Rate (%)": round(win_rate, 2),
        "Days Traded": len(equity)
    }


def save_to_excel(
    data: Dict[str, pd.DataFrame],
    filename: str,
    output_dir: str = "data/exports"
):
    """
    Save multiple DataFrames to Excel with multiple sheets
    
    Args:
        data: Dictionary mapping sheet_name -> DataFrame
        filename: Output filename
        output_dir: Output directory
    """
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    
    try:
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            for sheet_name, df in data.items():
                # Ensure sheet name is valid (max 31 chars)
                valid_sheet_name = sheet_name[:31]
                df.to_excel(writer, sheet_name=valid_sheet_name, index=False)
        
        logger.info(f"Saved Excel file: {filepath}")
        return filepath
    
    except Exception as e:
        logger.error(f"Error saving Excel file: {e}")
        return None


def validate_date_format(date_str: str) -> bool:
    """
    Validate date string is in YYYY-MM-DD format
    
    Args:
        date_str: Date string to validate
        
    Returns:
        True if valid, False otherwise
    """
    try:
        pd.Timestamp(date_str)
        return True
    except:
        return False


def get_latest_prediction_file(predictions_dir: str = "data/predictions") -> Optional[str]:
    """
    Get path to the most recent prediction file
    
    Args:
        predictions_dir: Directory containing prediction files
        
    Returns:
        File path or None if no files found
    """
    files = glob.glob(os.path.join(predictions_dir, "*.pkl"))
    
    if not files:
        return None
    
    return max(files, key=os.path.getctime)


def format_currency(value: float, currency: str = "$") -> str:
    """
    Format currency value
    
    Args:
        value: Numeric value
        currency: Currency symbol
        
    Returns:
        Formatted string
    """
    return f"{currency}{value:,.2f}"
