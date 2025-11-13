# 🎉 EGX Stock Predictor - Complete Project Package

This folder contains the complete, production-ready Streamlit application converted from your Colab notebook.

## 📦 What's Included

```
egx-stock-predictor/
│
├── 📄 streamlit_app.py        # Main Streamlit application
├── 📁 src/                     # Core modules
│   ├── __init__.py            # Package initialization
│   ├── data_handler.py        # Data downloading & preprocessing
│   ├── model_trainer.py       # Model training & prediction
│   ├── optimizer.py           # Parameter optimization
│   └── utils.py               # Utility functions
│
├── 📁 data/                    # Data storage
│   ├── predictions/           # Saved predictions (.pkl files)
│   ├── models/               # Trained models
│   └── exports/              # Excel exports
│
├── 📋 requirements.txt        # Python dependencies
├── ⚙️ config.py               # Configuration settings
├── 🚀 run.sh                  # Quick start script (Unix/Mac)
│
├── 📖 README.md               # Main documentation
├── ⚡ QUICKSTART.md           # Beginner's guide
├── 💻 EXAMPLES.md             # Code examples
├── 🚢 DEPLOYMENT.md           # Deployment guide
├── 🤝 CONTRIBUTING.md         # Contribution guidelines
│
├── 📜 LICENSE                 # MIT License
└── 🔒 .gitignore             # Git ignore rules
```

## 🚀 Quick Start (3 Steps)

### 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ Run the App
```bash
streamlit run streamlit_app.py
```

### 3️⃣ Open Browser
App automatically opens at `http://localhost:8501`

## 🎯 Key Features

### ✅ What This App Does

1. **Automatic Stock Predictions**
   - Fetches Shariah-compliant EGX stocks
   - Trains XGBoost models
   - Generates return predictions

2. **Parameter Optimization**
   - Tests multiple `top_k` values (1-10)
   - Tests multiple `voting_days` values (1-10)
   - Finds optimal combination

3. **Backtesting Analysis**
   - Tests on 30, 60, 90, 180, 365-day periods
   - Shows equity curves
   - Calculates performance metrics

4. **Interactive Dashboard**
   - View latest predictions
   - Run optimizations
   - Download results

## 🔧 Configuration

Edit `config.py` to customize:

```python
# Model Parameters
LOOKBACK_DAYS = 800           # Historical data window
RANDOM_STATE = 42             # Reproducibility

# Trading Parameters  
START_EQUITY_USD = 100.0      # Starting portfolio value
CIRCUIT_BREAKER_PCT = 0.25    # ±25% daily limit

# Optimization Ranges
TOP_K_RANGE = range(1, 11)    # Test top_k: 1-10
VOTING_DAYS_RANGE = range(1, 11)  # Test voting: 1-10
```

## 📊 How It Works

### Data Flow

```
1. Fetch Tickers → 2. Download Data → 3. Feature Engineering
                                            ↓
                                    4. Train Models
                                            ↓
                                    5. Make Predictions
                                            ↓
                                    6. Voting Mechanism
                                            ↓
                                    7. Select Top Stocks
```

### Technical Indicators Used

- **Log Returns**: Price momentum
- **Volume SMA**: Trading volume trends
- **RSI (9-period)**: Overbought/oversold
- **VP Change**: Volume-price relationship
- **Candle Strength**: Candlestick patterns
- **ATR (5-period)**: Volatility measure

### Machine Learning Model

- **Algorithm**: XGBoost Regressor
- **Training Split**: 75% train, 25% validation
- **Calibration**: Isotonic regression
- **Early Stopping**: Prevents overfitting

## 📖 Documentation Quick Links

| Document | Purpose |
|----------|---------|
| [README.md](README.md) | Complete project documentation |
| [QUICKSTART.md](QUICKSTART.md) | 5-minute beginner guide |
| [EXAMPLES.md](EXAMPLES.md) | Code examples & usage |
| [DEPLOYMENT.md](DEPLOYMENT.md) | Hosting & deployment |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to contribute |

## 🌐 Deploy to Cloud

### Streamlit Community Cloud (Free)

1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect repository
4. Deploy!

Your app will be live at: `https://your-username-egx-predictor.streamlit.app`

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

## 🔄 What Changed from Colab

| Colab Notebook | Streamlit App |
|----------------|---------------|
| Single file | Modular structure |
| Manual execution | Interactive UI |
| Code cells | Button clicks |
| Local only | Deployable online |
| Sequential | Concurrent |

## 💾 Data Persistence

The app automatically saves:

- ✅ Predictions: `data/predictions/{date}.pkl`
- ✅ Models: `data/models/` (if enabled)
- ✅ Exports: `data/exports/*.xlsx`

## ⚠️ Important Notes

### Before Trading

- ❗ This is **educational software only**
- ❗ Not financial advice
- ❗ Past performance ≠ future results
- ❗ Always consult a financial advisor

### Data Usage

- Uses Yahoo Finance API (free)
- Respects rate limits
- Implements caching

### Shariah Compliance

- Stocks list from [ClientN.com](https://clientn.com)
- Pre-screened for Shariah compliance
- Automatically updated

## 🐛 Troubleshooting

### Common Issues

**1. Module not found error**
```bash
pip install -r requirements.txt
```

**2. Port already in use**
```bash
streamlit run streamlit_app.py --server.port 8502
```

**3. Data download fails**
- Check internet connection
- Wait for rate limit reset
- Verify ticker list URL

**4. Slow performance**
- Reduce `LOOKBACK_DAYS` in config.py
- Use smaller parameter ranges
- Enable caching

## 📞 Support & Contact

- **Issues**: Open on GitHub
- **Questions**: Check QUICKSTART.md
- **Website**: [ClientN.com](https://clientn.com)

## 🎓 Learning Path

### Beginner
1. Read [QUICKSTART.md](QUICKSTART.md)
2. Run the app with defaults
3. View predictions
4. Try simple optimization

### Intermediate
1. Read [EXAMPLES.md](EXAMPLES.md)
2. Modify parameters
3. Run backtests
4. Compare results

### Advanced
1. Study source code in `src/`
2. Add custom indicators
3. Modify model parameters
4. Contribute improvements

## 🚀 Next Steps

1. **Install & Run**
   ```bash
   pip install -r requirements.txt
   streamlit run streamlit_app.py
   ```

2. **Read Documentation**
   - Start with [QUICKSTART.md](QUICKSTART.md)
   - Then read [README.md](README.md)

3. **Experiment**
   - Try different parameters
   - Run optimizations
   - Analyze results

4. **Deploy** (Optional)
   - Push to GitHub
   - Deploy to Streamlit Cloud
   - Share with others

## ✨ Features Coming Soon

- [ ] Real-time alerts
- [ ] Portfolio tracking
- [ ] Multi-timeframe analysis
- [ ] Risk management tools
- [ ] Mobile app
- [ ] API access

## 🙏 Credits

- **Data Source**: Yahoo Finance
- **Stock List**: ClientN.com
- **Framework**: Streamlit
- **ML Library**: XGBoost
- **Author**: Amr

## 📄 License

MIT License - See [LICENSE](LICENSE) for details

Free for personal and commercial use.

---

## ✅ Ready to Start?

```bash
# Quick start
pip install -r requirements.txt
streamlit run streamlit_app.py
```

The app will open automatically in your browser!

Need help? Start with [QUICKSTART.md](QUICKSTART.md) 🚀

---

**Made with ❤️ by Amr | Powered by AI & Machine Learning**

*This software is for educational purposes only. Not financial advice.*
