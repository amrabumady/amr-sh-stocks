"""
Configuration Settings for EGX Stock Predictor
"""

# Data Sources
TICKER_LIST_URL = "https://clientn.com/stocks/Shariaa.html"

# Directories
DATA_DIR = "data"
PREDICTIONS_DIR = "data/predictions"
MODELS_DIR = "data/models"
EXPORTS_DIR = "data/exports"

# Model Parameters
RANDOM_STATE = 42
LOOKBACK_DAYS = 800
CACHE_EXPIRE_DAYS = 1

# XGBoost Parameters
XGBOOST_PARAMS = {
    "n_estimators": 300,
    "learning_rate": 0.05,
    "max_depth": 4,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "objective": "reg:squarederror",
    "early_stopping_rounds": 20,
    "eval_metric": "mae"
}

# Feature Engineering
DEFAULT_VOL_WINDOW = 20
DEFAULT_PCT_WINDOW = 20
RSI_PERIOD = 9
ATR_PERIOD = 5

# Trading Parameters
START_EQUITY_USD = 100.0
CIRCUIT_BREAKER_PCT = 0.25  # ±25% daily limit

# Optimization
TOP_K_RANGE = range(1, 11)
VOTING_DAYS_RANGE = range(1, 11)
TOP_N_CASES = 3

# Time Periods for Backtesting
BACKTEST_PERIODS = [30, 60, 90, 180, 365]

# Streamlit Configuration
PAGE_TITLE = "EGX Stock Predictor"
PAGE_ICON = "📈"
LAYOUT = "wide"

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
