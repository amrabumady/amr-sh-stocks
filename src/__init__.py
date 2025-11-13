"""
EGX Stock Predictor - Core Package
"""

from src.data_handler import DataHandler
from src.model_trainer import ModelTrainer
from src.optimizer import ParameterOptimizer
from src.utils import (
    load_optim_params,
    get_expected_percent,
    format_percentage,
    calculate_metrics,
    save_to_excel,
    validate_date_format,
    get_latest_prediction_file,
    format_currency
)

__version__ = "1.0.0"
__all__ = [
    "DataHandler",
    "ModelTrainer", 
    "ParameterOptimizer",
    "load_optim_params",
    "get_expected_percent",
    "format_percentage",
    "calculate_metrics",
    "save_to_excel",
    "validate_date_format",
    "get_latest_prediction_file",
    "format_currency"
]
