# ⚡ Quick Start Guide

Get up and running with EGX Stock Predictor in 5 minutes!

## 🎯 What You'll Learn

- Install the application
- Run your first prediction
- Understand the results
- Make your first optimization

## 📋 Prerequisites

Before starting, ensure you have:
- ✅ Computer with Windows, Mac, or Linux
- ✅ Internet connection
- ✅ Python 3.8 or newer ([Download Python](https://www.python.org/downloads/))

### Check Python Version

```bash
python --version
# or
python3 --version
```

You should see: `Python 3.8.x` or higher

## 🚀 Installation (3 Steps)

### Step 1: Download the Code

**Option A: Using Git** (Recommended)
```bash
git clone https://github.com/yourusername/egx-stock-predictor.git
cd egx-stock-predictor
```

**Option B: Download ZIP**
1. Go to the [GitHub repository](https://github.com/yourusername/egx-stock-predictor)
2. Click green "Code" button
3. Select "Download ZIP"
4. Extract the ZIP file
5. Open terminal/command prompt in the extracted folder

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

⏱️ This will take 2-3 minutes

### Step 3: Run the App

```bash
streamlit run streamlit_app.py
```

🎉 The app will automatically open in your browser!

## 🎮 First Time Usage

### 1. View Latest Predictions

1. In the sidebar, ensure "📊 View Latest Predictions" is selected
2. Click "🔄 Load Latest Predictions" button
3. Wait a few seconds while data is fetched

**What you'll see:**
- List of all EGX Shariah-compliant stocks
- Expected return percentage for each
- Color coding (green = positive, red = negative)

### 2. Understanding the Results

```
Ticker: INFI.CA
Expected Return: +15.5%
```

This means:
- **INFI.CA** is predicted to increase by **15.5%**
- This is based on historical patterns and technical indicators

⚠️ **Important**: This is a prediction, not a guarantee!

### 3. Download Predictions

Click the "📥 Download Predictions" button to save results as CSV

## 🔍 Running Your First Optimization

### What is Optimization?

Optimization finds the best parameters (top_k and voting_days) to maximize returns.

### Steps:

1. Select "🔍 Run Optimization" from sidebar
2. Use default settings for first run:
   - Top K Range: 1 to 10
   - Voting Days Range: 1 to 10
3. Click "▶️ Start Optimization"
4. Wait 5-10 minutes (grab a coffee! ☕)

### Results:

You'll see:
- **Best Top K**: Number of stocks to hold
- **Best Voting Days**: Days to aggregate predictions
- **Final Equity**: Simulated portfolio value
- **Heatmap**: Visual representation of all combinations

## 📊 Example Results

```
Best Parameters Found:
├─ Top K: 3 stocks
├─ Voting Days: 5 days
└─ Final Equity: $145.50 (45.5% return)

Top 3 Recommended Stocks:
1. INFI.CA  (+17.5%)
2. TMGH.CA  (+15.2%)
3. SMFR.CA  (+12.8%)
```

## 🎯 Next Steps

### Try Different Settings

Experiment with parameters:

**Conservative Strategy:**
- Top K: 5-10 stocks (more diversification)
- Voting Days: 7-10 days (more stable)

**Aggressive Strategy:**
- Top K: 1-3 stocks (concentrated)
- Voting Days: 1-3 days (reactive)

### Run Backtesting

1. Select "📈 Backtesting Analysis"
2. Choose time periods (30, 60, 90 days)
3. Click "▶️ Run Backtest"
4. Compare performance across periods

## 🆘 Troubleshooting

### Problem: App won't start

**Solution:**
```bash
# Try updating Streamlit
pip install --upgrade streamlit

# Run again
streamlit run streamlit_app.py
```

### Problem: "No module named 'streamlit'"

**Solution:**
```bash
# Install requirements again
pip install -r requirements.txt
```

### Problem: Data download fails

**Solution:**
- Check internet connection
- Wait a few minutes (API rate limits)
- Try again

### Problem: App is slow

**Solution:**
- Reduce lookback days (sidebar)
- Use smaller parameter ranges
- Close other applications

## 💡 Tips for Beginners

### 1. Start Simple
- Use default parameters first
- Run predictions before optimization
- Understand results before customizing

### 2. Don't Trust Blindly
- This is a tool, not magic
- Always verify predictions
- Use as one input among many

### 3. Learn Gradually
- Read the README for concepts
- Check EXAMPLES.md for code samples
- Experiment with settings

### 4. Track Your Learning
- Save prediction files
- Compare different parameter sets
- Note what works and what doesn't

## 📚 Learning Resources

### Understanding Stock Prediction
- [Technical Analysis Basics](https://www.investopedia.com/terms/t/technicalanalysis.asp)
- [Machine Learning in Finance](https://www.investopedia.com/terms/m/machine-learning.asp)

### Technical Indicators Used
- **RSI** (Relative Strength Index): Momentum indicator
- **SMA** (Simple Moving Average): Trend indicator
- **ATR** (Average True Range): Volatility indicator
- **Volume Analysis**: Trading activity

### Python & Streamlit
- [Python Tutorial](https://docs.python.org/3/tutorial/)
- [Streamlit Documentation](https://docs.streamlit.io)
- [Pandas Basics](https://pandas.pydata.org/docs/user_guide/10min.html)

## 🎓 Concepts Explained Simply

### What is "Top K"?
The number of stocks to select and hold in your portfolio.
- Top K = 1: Only hold the best stock
- Top K = 5: Hold the top 5 stocks
- Top K = 10: Hold the top 10 stocks

### What is "Voting Days"?
The number of recent days to consider when selecting stocks.
- Voting Days = 1: Only use today's predictions
- Voting Days = 5: Aggregate last 5 days
- Voting Days = 10: Consider last 10 days

Higher voting days = more stable but less reactive

### What is "Expected Return"?
The predicted percentage change in stock price.
- +10% means stock expected to go up 10%
- -5% means stock expected to go down 5%

### What is "Backtesting"?
Testing the strategy on historical data to see how it would have performed.

## ✅ Quick Checklist

Before making any decisions:

- [ ] Understand how the system works
- [ ] Run multiple tests with different parameters
- [ ] Compare results across time periods
- [ ] Check latest predictions
- [ ] Read the disclaimer (this is not financial advice!)
- [ ] Consult a financial advisor
- [ ] Start with small amounts if testing live

## 🔄 Daily Workflow

### Morning Routine (5 minutes)
1. Open app
2. Load latest predictions
3. Check top recommendations
4. Note any significant changes

### Weekly Analysis (30 minutes)
1. Run new optimization
2. Compare with previous week
3. Analyze backtest results
4. Adjust parameters if needed

### Monthly Review (1 hour)
1. Run comprehensive backtest
2. Review prediction accuracy
3. Fine-tune parameters
4. Document learnings

## 🎯 Success Metrics

Track these to measure improvement:
- **Prediction Accuracy**: % of correct predictions
- **Return Rate**: Average predicted vs actual
- **Stability**: Consistency of recommendations
- **Risk Management**: Maximum drawdown

## 🚀 You're Ready!

You now know:
- ✅ How to install and run the app
- ✅ How to view predictions
- ✅ How to run optimization
- ✅ How to interpret results
- ✅ Where to learn more

## 📞 Need Help?

- 📖 Read the [full documentation](README.md)
- 💻 Check [code examples](EXAMPLES.md)
- 🐛 Report [issues on GitHub](https://github.com/yourusername/egx-stock-predictor/issues)
- 💬 Ask questions in Discussions

---

**Remember**: This tool is for educational purposes. Always do your own research and consult professionals before making investment decisions.

Happy predicting! 🎉📈
