# EGX Stock Predictor - Usage Examples

This document shows how to use the EGX Stock Predictor modules programmatically.

## Basic Usage

### 1. Get Stock Tickers

```python
from src import DataHandler

# Initialize handler
handler = DataHandler()

# Get list of Shariah-compliant EGX tickers
tickers = handler.get_tickers()
print(f"Found {len(tickers)} tickers")
print(tickers[:5])  # First 5 tickers
```

### 2. Download Historical Data

```python
from src import DataHandler
from datetime import datetime, timedelta

handler = DataHandler()
tickers = handler.get_tickers()

# Define date range
end_date = datetime.now().strftime("%Y-%m-%d")
start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")

# Download data
bars = handler.download_bars(
    tickers=tickers[:10],  # First 10 tickers for demo
    start=start_date,
    end=end_date,
    show_progress=True
)

print(f"Downloaded data for {len(bars)} tickers")
```

### 3. Train Model and Predict

```python
from src import ModelTrainer

trainer = ModelTrainer()

# Train and predict for a single stock
ticker = "INFI.CA"
df = bars[ticker]

prediction = trainer.train_and_predict(
    df=df,
    vol_window=20,
    pct_window=20
)

print(f"Prediction for {ticker}: {prediction}%")
```

### 4. Generate Predictions for All Stocks

```python
from src import DataHandler, ModelTrainer
from datetime import datetime

handler = DataHandler()
trainer = ModelTrainer()

# Get data
tickers = handler.get_tickers()
end_date = datetime.now().strftime("%Y-%m-%d")
start_date = (datetime.now() - timedelta(days=800)).strftime("%Y-%m-%d")

bars = handler.download_bars(tickers, start_date, end_date)

# Generate predictions
predictions = []
for ticker, df in bars.items():
    result = trainer.process_ticker(ticker, df, vol_window=20, pct_window=20)
    if result:
        predictions.append(result)

# Sort by prediction
predictions.sort(key=lambda x: x[1], reverse=True)

# Display top 10
print("Top 10 Predictions:")
for i, (ticker, pred) in enumerate(predictions[:10], 1):
    print(f"{i}. {ticker}: {pred}%")
```

### 5. Save and Load Predictions

```python
from src import ModelTrainer
from datetime import datetime

trainer = ModelTrainer()

# Save predictions
date_str = datetime.now().strftime("%Y-%m-%d")
trainer.save_predictions(predictions, date_str)

# Load predictions
loaded_predictions = trainer.load_predictions(date_str)
print(f"Loaded {len(loaded_predictions)} predictions")
```

### 6. Run Parameter Optimization

```python
from src import ParameterOptimizer

optimizer = ParameterOptimizer()

# Run optimization
results = optimizer.run_optimization(
    top_k_range=range(1, 6),      # Test top_k: 1-5
    voting_range=range(1, 6),     # Test voting_days: 1-5
    lookback_days=180             # Use 180 days of data
)

# Display best parameters
best = results['best_params']
print(f"Best top_k: {best['top_k']}")
print(f"Best voting_days: {best['voting_days']}")
print(f"Final equity: ${best['final_equity']:.2f}")
```

### 7. Get Voting-Based Recommendations

```python
from src import ParameterOptimizer, DataHandler
from datetime import datetime

optimizer = ParameterOptimizer()
handler = DataHandler()

# Get trading days
today = datetime.now().strftime("%Y-%m-%d")
dates = handler.get_trading_days(today, n_days=30)

# Get recommendations using voting
recommendations = optimizer.voting_predictions(
    dates=dates,
    last_date=dates[-1],
    voting_days=3,
    top_k=5
)

print("Top 5 Recommended Stocks:")
for i, ticker in enumerate(recommendations, 1):
    print(f"{i}. {ticker}")
```

### 8. Calculate Performance Metrics

```python
from src import calculate_metrics
import pandas as pd

# Assuming you have an equity curve DataFrame
equity_curve = pd.DataFrame({
    'Date': ['2024-01-01', '2024-01-02', '2024-01-03'],
    'Equity': [100, 105, 110],
    'Daily_%': [0, 5, 4.76]
})

metrics = calculate_metrics(equity_curve)

print("Performance Metrics:")
for key, value in metrics.items():
    print(f"{key}: {value}")
```

### 9. Compute Daily Returns Matrix

```python
from src import DataHandler

handler = DataHandler()

# Download data
bars = handler.download_bars(
    tickers=handler.get_tickers()[:20],
    start="2024-01-01",
    end="2024-12-31"
)

# Calculate returns matrix
returns = handler.compute_daily_returns(bars)

print(f"Returns shape: {returns.shape}")
print(f"Date range: {returns.index[0]} to {returns.index[-1]}")
```

### 10. Custom Feature Engineering

```python
from src import ModelTrainer
import pandas as pd

trainer = ModelTrainer()

# Create features for a stock
df = bars["INFI.CA"]
features = trainer.create_features(
    df=df,
    vol_window=20,
    pct_window=20
)

print("Features created:")
print(features.columns.tolist())
print(f"\nFeature shape: {features.shape}")
print(f"\nLast 5 rows:")
print(features.tail())
```

## Advanced Examples

### Portfolio Simulation

```python
from src import ParameterOptimizer, DataHandler

optimizer = ParameterOptimizer(start_equity=10000.0)
handler = DataHandler()

# Setup
dates = handler.get_trading_days("2024-12-31", n_days=90)
bars = handler.download_bars(handler.get_tickers(), "2024-10-01", "2024-12-31")
returns = handler.compute_daily_returns(bars)

# Create predictions by day (you would load these from saved files)
predictions_by_day = {
    date: ["INFI.CA", "TMGH.CA", "SMFR.CA"]  # Example
    for date in dates
}

# Simulate
final_equity, curve = optimizer.simulate_portfolio(
    dates=dates,
    returns_df=returns,
    predictions_by_day=predictions_by_day,
    top_k=3
)

print(f"Starting equity: $10,000")
print(f"Final equity: ${final_equity:,.2f}")
print(f"Return: {((final_equity - 10000) / 10000 * 100):.2f}%")
```

### Export to Excel

```python
from src import save_to_excel
import pandas as pd

# Create sample data
predictions_df = pd.DataFrame(predictions, columns=["Ticker", "Prediction"])
metrics_df = pd.DataFrame([metrics])

# Save to Excel with multiple sheets
filepath = save_to_excel(
    data={
        "Predictions": predictions_df,
        "Metrics": metrics_df,
        "Equity_Curve": equity_curve
    },
    filename="analysis_results.xlsx"
)

print(f"Saved to: {filepath}")
```

### Utility Functions

```python
from src import (
    get_expected_percent,
    format_percentage,
    format_currency,
    validate_date_format
)

# Get prediction for specific ticker
prediction = get_expected_percent("INFI.CA", predictions)
print(f"INFI.CA prediction: {prediction}%")

# Format values
print(format_percentage(15.5))  # 🟢 15.50%
print(format_currency(1234.56))  # $1,234.56

# Validate date
is_valid = validate_date_format("2024-12-31")
print(f"Date valid: {is_valid}")
```

## Error Handling

```python
from src import DataHandler, ModelTrainer

handler = DataHandler()
trainer = ModelTrainer()

try:
    # Get tickers
    tickers = handler.get_tickers()
    
    # Download data with error handling
    bars = handler.download_bars(tickers, "2024-01-01", "2024-12-31")
    
    # Process each ticker
    for ticker, df in bars.items():
        try:
            prediction = trainer.train_and_predict(df, 20, 20)
            if prediction:
                print(f"{ticker}: {prediction}%")
        except Exception as e:
            print(f"Error processing {ticker}: {e}")
            
except Exception as e:
    print(f"Fatal error: {e}")
```

## Integration with Streamlit

```python
import streamlit as st
from src import DataHandler, ModelTrainer

st.title("Custom Stock Analysis")

# Get user inputs
ticker = st.text_input("Enter ticker symbol:")

if st.button("Analyze"):
    handler = DataHandler()
    trainer = ModelTrainer()
    
    # Download data
    bars = handler.download_bars([ticker], "2023-01-01", "2024-12-31")
    
    if ticker in bars:
        # Make prediction
        prediction = trainer.train_and_predict(bars[ticker], 20, 20)
        
        # Display result
        st.success(f"Prediction for {ticker}: {prediction}%")
    else:
        st.error(f"No data found for {ticker}")
```

## Tips and Best Practices

1. **Data Caching**: Cache downloaded data to avoid repeated API calls
2. **Error Handling**: Always wrap API calls in try-except blocks
3. **Progress Tracking**: Use `show_progress=True` for long operations
4. **Parameter Tuning**: Start with default parameters, then optimize
5. **Validation**: Always validate predictions before trading
6. **Logging**: Enable logging to track operations

## Common Issues

### Issue: "No data downloaded"
**Solution**: Check ticker symbols and date ranges

### Issue: "Insufficient data for modeling"
**Solution**: Increase lookback_days parameter

### Issue: "Optimization takes too long"
**Solution**: Reduce parameter ranges or use smaller dataset

---

For more examples, see the Streamlit app code in `streamlit_app.py`
