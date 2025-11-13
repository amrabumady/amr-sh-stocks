"""
Model Trainer Module
Handles feature engineering, model training, and prediction
"""

import pandas as pd
import numpy as np
import pickle
import os
import logging
from typing import Optional, Tuple
from xgboost import XGBRegressor
from sklearn.calibration import IsotonicRegression

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelTrainer:
    """Handles model training and prediction for stock data"""
    
    def __init__(self, random_state: int = 42):
        self.random_state = random_state
        self.models = {}
        
    @staticmethod
    def calculate_rsi(series: pd.Series, period: int = 14) -> pd.Series:
        """
        Calculate RSI (Relative Strength Index)
        
        Args:
            series: Price series
            period: RSI period
            
        Returns:
            RSI values
        """
        delta = series.diff()
        gain = delta.clip(lower=0).ewm(alpha=1/period, adjust=False).mean()
        loss = (-delta.clip(upper=0)).ewm(alpha=1/period, adjust=False).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    @staticmethod
    def get_column(obj, name: str):
        """Extract column safely from DataFrame or Series"""
        series = obj[name]
        return series.iloc[:, 0] if isinstance(series, pd.DataFrame) else series
    
    def create_features(
        self, 
        df: pd.DataFrame, 
        vol_window: int, 
        pct_window: int
    ) -> pd.DataFrame:
        """
        Create technical indicator features
        
        Args:
            df: OHLCV DataFrame
            vol_window: Volume SMA window
            pct_window: Return SMA window
            
        Returns:
            Feature DataFrame
        """
        # Use lagged data (shift by 1)
        lag = df.shift(1)
        features = pd.DataFrame(index=df.index)
        
        # Extract OHLCV
        close = self.get_column(lag, "Close")
        volume = self.get_column(lag, "Volume")
        high = self.get_column(lag, "High")
        low = self.get_column(lag, "Low")
        open_price = self.get_column(lag, "Open")
        
        # Log returns
        features["LogRet"] = np.log(close).diff() * 100
        
        # Volume SMA
        features["Vol_SMA"] = volume.rolling(vol_window).mean()
        
        # Price change SMA (target variable base)
        features["Pct_SMA"] = features["LogRet"].rolling(pct_window).mean()
        
        # Volume-Price change
        features["VP_Change"] = features["Vol_SMA"] * close.diff()
        
        # RSI indicators
        features["RSI_9_Close"] = self.calculate_rsi(close, 9)
        features["RSI_9_VPChange"] = self.calculate_rsi(features["VP_Change"], 9)
        
        # RSI momentum
        features["d_RSI_9_Close"] = (
            features["RSI_9_Close"] - 
            features["RSI_9_Close"].rolling(3).mean()
        )
        features["d_RSI_9_VPChange"] = (
            features["RSI_9_VPChange"] - 
            features["RSI_9_VPChange"].rolling(3).mean()
        )
        
        # Candle strength
        features["Candle_Strength"] = (
            (open_price - close).abs() / (high - low).abs()
        )
        
        # Average True Range
        features["ATR5"] = (high - low).rolling(5).mean()
        
        # Time features
        features["DoW"] = lag.index.dayofweek
        features["MonthEnd"] = lag.index.is_month_end.astype(int)
        features["Date_Ord"] = lag.index.map(pd.Timestamp.toordinal)
        
        # Clean up
        features = features.replace([np.inf, -np.inf], np.nan)
        features = features.dropna()
        
        return features
    
    def train_and_predict(
        self,
        df: pd.DataFrame,
        vol_window: int,
        pct_window: int
    ) -> Optional[float]:
        """
        Train model and make prediction for next period
        
        Args:
            df: OHLCV DataFrame
            vol_window: Volume SMA window
            pct_window: Return SMA window
            
        Returns:
            Predicted percentage return, or None if insufficient data
        """
        # Create features
        features = self.create_features(df, vol_window, pct_window)
        
        if len(features) < 60:
            return None
        
        # Separate features and target
        X = features.drop("Pct_SMA", axis=1)
        y = features["Pct_SMA"]
        
        # Train/test split (75/25)
        split_idx = int(len(X) * 0.75)
        
        X_train, X_test = X[:split_idx], X[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]
        
        # Train XGBoost model
        model = XGBRegressor(
            n_estimators=300,
            learning_rate=0.05,
            max_depth=4,
            subsample=0.8,
            colsample_bytree=0.8,
            objective="reg:squarederror",
            random_state=self.random_state,
            early_stopping_rounds=20,
            eval_metric="mae"
        )
        
        eval_set = [(X_test, y_test)]
        model.fit(
            X_train, 
            y_train,
            eval_set=eval_set,
            verbose=False
        )
        
        # Isotonic calibration (if enough test data)
        calibrator = None
        if len(X_test) > 30:
            calibrator = IsotonicRegression(out_of_bounds="clip")
            test_pred = model.predict(X_test)
            calibrator.fit(test_pred, y_test)
        
        # Make prediction for the last data point
        raw_pred = model.predict(X.iloc[[-1]])[0]
        
        if calibrator:
            calibrated_pred = float(calibrator.predict([raw_pred])[0])
        else:
            calibrated_pred = raw_pred
        
        # Convert average return to total expected return
        # Multiply by window and subtract recent returns
        prediction = round(
            calibrated_pred * pct_window - y.tail(pct_window - 1).sum(),
            2
        )
        
        return prediction
    
    def process_ticker(
        self,
        ticker: str,
        df: pd.DataFrame,
        vol_window: int,
        pct_window: int
    ) -> Optional[Tuple[str, float]]:
        """
        Process single ticker and return prediction
        
        Args:
            ticker: Stock ticker symbol
            df: OHLCV DataFrame
            vol_window: Volume SMA window
            pct_window: Return SMA window
            
        Returns:
            (ticker, prediction) tuple or None
        """
        if df.empty:
            return None
        
        try:
            prediction = self.train_and_predict(df, vol_window, pct_window)
            
            if prediction is not None:
                return (ticker, prediction)
        
        except Exception as e:
            logger.warning(f"Error processing {ticker}: {e}")
        
        return None
    
    def save_predictions(
        self,
        predictions: list,
        date_str: str,
        output_dir: str = "data/predictions"
    ):
        """
        Save predictions to pickle file
        
        Args:
            predictions: List of (ticker, prediction) tuples
            date_str: Date string (YYYY-MM-DD)
            output_dir: Output directory
        """
        os.makedirs(output_dir, exist_ok=True)
        
        file_path = os.path.join(output_dir, f"{date_str}.pkl")
        
        with open(file_path, "wb") as f:
            pickle.dump(predictions, f)
        
        logger.info(f"Saved predictions to {file_path}")
    
    def load_predictions(
        self,
        date_str: str,
        predictions_dir: str = "data/predictions"
    ) -> Optional[list]:
        """
        Load predictions from pickle file
        
        Args:
            date_str: Date string (YYYY-MM-DD)
            predictions_dir: Directory containing predictions
            
        Returns:
            List of (ticker, prediction) tuples or None
        """
        file_path = os.path.join(predictions_dir, f"{date_str}.pkl")
        
        if not os.path.exists(file_path):
            logger.warning(f"Prediction file not found: {file_path}")
            return None
        
        try:
            with open(file_path, "rb") as f:
                predictions = pickle.load(f)
            
            logger.info(f"Loaded predictions from {file_path}")
            return predictions
        
        except Exception as e:
            logger.error(f"Error loading predictions: {e}")
            return None
