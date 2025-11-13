# 📈 EGX Stock Predictor

AI-powered stock prediction system for Egyptian Exchange (EGX) Shariah-compliant stocks with automated parameter optimization.

## 🌟 Features

- **Automated Stock Predictions**: Uses XGBoost and technical indicators to predict stock returns
- **Parameter Optimization**: Automatically finds optimal `top_k` and `voting_days` parameters
- **Backtesting Engine**: Validates strategies across multiple time periods
- **Interactive Dashboard**: Beautiful Streamlit UI for easy interaction
- **Voting Mechanism**: Aggregates predictions across multiple days for robust recommendations

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/egx-stock-predictor.git
cd egx-stock-predictor
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
streamlit run streamlit_app.py
```

The app will open in your default browser at `http://localhost:8501`

## 📊 How It Works

### 1. Data Collection
- Fetches Shariah-compliant EGX tickers from ClientN
- Downloads historical OHLCV data using Yahoo Finance
- Applies data cleaning and validation

### 2. Feature Engineering
The system creates multiple technical indicators:
- **Log Returns**: Normalized price changes
- **Volume SMA**: Volume moving average
- **RSI Indicators**: Multiple RSI calculations
- **Volume-Price Change**: Combined volume and price momentum
- **Candle Strength**: Candlestick pattern strength
- **ATR**: Average True Range for volatility

### 3. Model Training
- **Algorithm**: XGBoost Regressor
- **Calibration**: Isotonic regression for probability calibration
- **Validation**: 75/25 train-test split with early stopping

### 4. Optimization
Tests multiple parameter combinations:
- `top_k`: Number of stocks to hold (1-10)
- `voting_days`: Number of days to aggregate predictions (1-10)

Finds the combination that maximizes portfolio equity.

### 5. Prediction & Voting
- Generates daily predictions for all stocks
- Votes across multiple days for stability
- Returns top-k stocks by vote count and expected return

## 🎯 Usage Guide

### View Latest Predictions
1. Select "📊 View Latest Predictions" from sidebar
2. Click "🔄 Load Latest Predictions"
3. View ranked stocks with expected returns
4. Download predictions as CSV

### Run Optimization
1. Select "🔍 Run Optimization" from sidebar
2. Configure parameter ranges:
   - Top K Range: 1-10
   - Voting Days Range: 1-10
3. Click "▶️ Start Optimization"
4. View performance heatmap and optimal parameters

### Backtesting Analysis
1. Select "📈 Backtesting Analysis"
2. Choose time periods (30, 60, 90, 180, 365 days)
3. Click "▶️ Run Backtest"
4. Analyze equity curves and metrics

## 📁 Project Structure

```
egx-stock-predictor/
├── streamlit_app.py          # Main Streamlit application
├── src/
│   ├── __init__.py           # Package initialization
│   ├── data_handler.py       # Data downloading and preprocessing
│   ├── model_trainer.py      # Model training and prediction
│   ├── optimizer.py          # Parameter optimization
│   └── utils.py              # Utility functions
├── data/
│   ├── predictions/          # Saved predictions (pickle files)
│   ├── models/              # Trained models
│   └── exports/             # Excel exports
├── requirements.txt          # Python dependencies
├── README.md                # This file
└── .gitignore              # Git ignore rules
```

## 🔧 Configuration

Key parameters can be adjusted in the sidebar:
- **Lookback Days**: Historical data window (default: 800)
- **Top K Stocks**: Number of stocks to select (default: 2)
- **Voting Days**: Days to aggregate predictions (default: 3)

## 📈 Performance Metrics

The system tracks:
- **Total Return**: Overall portfolio performance
- **Max Drawdown**: Largest peak-to-trough decline
- **Sharpe Ratio**: Risk-adjusted returns
- **Win Rate**: Percentage of profitable days

## 🛠️ Technology Stack

- **Framework**: Streamlit
- **Machine Learning**: XGBoost, scikit-learn
- **Data**: yfinance, pandas, numpy
- **Visualization**: matplotlib
- **Deployment**: Streamlit Community Cloud

## 📝 API Reference

### DataHandler
```python
from src import DataHandler

handler = DataHandler()
tickers = handler.get_tickers()
bars = handler.download_bars(tickers, start="2023-01-01", end="2024-01-01")
```

### ModelTrainer
```python
from src import ModelTrainer

trainer = ModelTrainer()
prediction = trainer.train_and_predict(df, vol_window=20, pct_window=20)
```

### ParameterOptimizer
```python
from src import ParameterOptimizer

optimizer = ParameterOptimizer()
results = optimizer.run_optimization(
    top_k_range=range(1, 11),
    voting_range=range(1, 11)
)
```

## 🚨 Disclaimer

**This software is for educational and research purposes only.**

- Not financial advice
- Past performance does not guarantee future results
- Trading involves risk of loss
- Always consult a licensed financial advisor

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Amr**
- Website: [ClientN.com](https://clientn.com)

## 🙏 Acknowledgments

- ClientN for Shariah-compliant ticker list
- Yahoo Finance for market data
- Streamlit for the amazing framework

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Contact via ClientN.com

## 🔄 Updates

### Version 1.0.0
- Initial release
- Core prediction engine
- Parameter optimization
- Streamlit dashboard
- Backtesting system

---

Made with ❤️ by Amr | Powered by AI & Machine Learning
