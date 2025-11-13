"""
Data Handler Module
Handles stock data downloading, caching, and preprocessing
"""

import pandas as pd
import numpy as np
import yfinance as yf
import requests
import ast
import re
import json
import logging
from typing import List, Dict, Optional
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataHandler:
    """Handles data downloading and preprocessing for EGX stocks"""
    
    TICKER_LIST_URL = "https://clientn.com/stocks/Shariaa.html"
    CACHE_EXPIRE_DAYS = 1
    
    def __init__(self):
        self.tickers = []
        self.cache = {}
        
    def get_tickers(self, url: Optional[str] = None) -> List[str]:
        """
        Fetch list of Shariah-compliant EGX tickers from ClientN
        
        Args:
            url: URL to fetch tickers from (uses default if None)
            
        Returns:
            List of ticker symbols
        """
        if url is None:
            url = self.TICKER_LIST_URL
            
        try:
            response = requests.get(url, timeout=15)
            txt = response.text.strip()
            
            # Try to parse as Python literal
            try:
                ticker_list = ast.literal_eval(txt)
            except Exception:
                # Fallback: extract JSON-like list
                match = re.search(r'\[.*\]', txt, re.S)
                if match:
                    ticker_list = json.loads(match.group(0).replace("'", '"'))
                else:
                    ticker_list = []
            
            if not ticker_list:
                raise RuntimeError("Ticker list parsing failed")
            
            self.tickers = sorted({t.upper().strip() for t in ticker_list})
            logger.info(f"Loaded {len(self.tickers)} tickers")
            return self.tickers
            
        except Exception as e:
            logger.error(f"Failed to fetch tickers: {e}")
            # Fallback to hardcoded list if available
            return self._get_fallback_tickers()
    
    def _get_fallback_tickers(self) -> List[str]:
        """Return a fallback list of common EGX tickers"""
        return [
            'INFI.CA', 'TMGH.CA', 'SMFR.CA', 'MBSC.CA', 'MOSC.CA',
            'INEG.CA', 'MOED.CA', 'EGAS.CA', 'AJWA.CA', 'OLFI.CA'
        ]
    
    def download_bars(
        self, 
        tickers: List[str], 
        start: str, 
        end: str,
        show_progress: bool = True
    ) -> Dict[str, pd.DataFrame]:
        """
        Download OHLCV data for multiple tickers
        
        Args:
            tickers: List of ticker symbols
            start: Start date (YYYY-MM-DD)
            end: End date (YYYY-MM-DD)
            show_progress: Show download progress
            
        Returns:
            Dictionary mapping ticker -> DataFrame
        """
        data = {}
        
        from tqdm import tqdm
        iterator = tqdm(tickers, desc="Downloading") if show_progress else tickers
        
        for ticker in iterator:
            # Try up to 3 times
            for attempt in range(3):
                try:
                    df = yf.download(
                        ticker,
                        start=start,
                        end=end,
                        interval="1d",
                        progress=False,
                        auto_adjust=False,
                        threads=False
                    )
                    
                    # Filter out zero volume days
                    if not df.empty and "Volume" in df.columns:
                        df = df[df["Volume"] > 0]
                    
                    # Remove timezone info
                    if not df.empty:
                        df.index = df.index.tz_localize(None)
                    
                    data[ticker] = df
                    break
                    
                except Exception as e:
                    if attempt == 2:
                        logger.warning(f"{ticker} download failed: {e}")
                        data[ticker] = pd.DataFrame()
        
        logger.info(f"Downloaded data for {len(data)} tickers")
        return data
    
    def get_trading_days(
        self, 
        last_date: str, 
        n_days: int,
        skip_dates: Optional[set] = None
    ) -> List[pd.Timestamp]:
        """
        Get list of trading days within a period
        
        Args:
            last_date: End date (YYYY-MM-DD)
            n_days: Number of calendar days to look back
            skip_dates: Set of dates to exclude
            
        Returns:
            List of trading day timestamps
        """
        if not self.tickers:
            self.get_tickers()
        
        if not self.tickers:
            logger.error("No tickers available")
            return []
        
        ticker = self.tickers[0]
        end_date = pd.Timestamp(last_date).normalize()
        start_date = end_date - pd.Timedelta(days=n_days)
        
        try:
            df = yf.download(
                ticker,
                start=start_date.date().isoformat(),
                end=last_date,
                interval="1d",
                progress=False,
                auto_adjust=False,
                threads=False
            )
            
            if not df.empty:
                df.index = df.index.tz_localize(None)
                
                # Exclude skip dates
                if skip_dates:
                    clean_idx = [d for d in df.index if d not in skip_dates]
                else:
                    clean_idx = df.index.tolist()
                
                return sorted(clean_idx)
        
        except Exception as e:
            logger.error(f"Error downloading trading days: {e}")
        
        return []
    
    def compute_daily_returns(self, bars: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """
        Compute daily returns matrix with circuit breaker
        
        Args:
            bars: Dictionary of ticker -> OHLCV DataFrame
            
        Returns:
            DataFrame with returns (±25% cap applied)
        """
        closes = {
            ticker: df["Close"] 
            for ticker, df in bars.items()
            if not df.empty and "Close" in df.columns
        }
        
        if not closes:
            return pd.DataFrame()
        
        close_df = pd.concat(closes, axis=1).sort_index()
        
        # Flatten MultiIndex columns if present
        if isinstance(close_df.columns, pd.MultiIndex):
            close_df.columns = close_df.columns.get_level_values(0)
        
        # Calculate returns
        returns = close_df.pct_change().fillna(0.0)
        
        # Apply circuit breaker (±25%)
        returns = returns.mask(returns.abs() > 0.25, 0.0)
        
        return returns
