# 🔧 Streamlit Cloud Deployment - Troubleshooting Guide

## ❗ ModuleNotFoundError Fix

If you see this error:
```
ModuleNotFoundError: This app has encountered an error...
from src.data_handler import DataHandler
```

### ✅ Solution

The updated `streamlit_app.py` now includes a fix for this. Make sure your file has these lines at the top:

```python
import sys
import os

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
```

## 🚀 Deployment Checklist

### 1. File Structure on GitHub

Ensure your repository has this structure:
```
your-repo/
├── streamlit_app.py       ← Must be in root
├── requirements.txt       ← Must be in root
├── .streamlit/
│   └── config.toml
├── src/
│   ├── __init__.py       ← Important!
│   ├── data_handler.py
│   ├── model_trainer.py
│   ├── optimizer.py
│   └── utils.py
├── data/
│   ├── predictions/
│   ├── models/
│   └── exports/
└── config.py
```

### 2. Verify __init__.py Files

Make sure these files exist and are not empty:

**src/__init__.py** should contain:
```python
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
```

### 3. Requirements.txt

Ensure all packages are listed with correct versions:
```txt
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
yfinance>=0.2.40
xgboost>=2.0.0,<2.1.0
scikit-learn>=1.4.0
matplotlib>=3.7.0
tqdm>=4.65.0
requests>=2.31.0
openpyxl>=3.1.0
xlsxwriter>=3.1.0
```

### 4. GitHub Push

```bash
# Make sure everything is committed
git add .
git commit -m "Fix imports for Streamlit Cloud"
git push origin main
```

### 5. Streamlit Cloud Settings

In Streamlit Cloud dashboard:
- **Main file path**: `streamlit_app.py`
- **Python version**: 3.9 or 3.10 (recommended)
- **Advanced settings**: Leave default

## 🐛 Common Issues & Solutions

### Issue 1: Import Error After Deployment

**Symptom:**
```
ModuleNotFoundError: No module named 'src'
```

**Solutions:**

**A. Check File Structure**
```bash
# Run this in your project directory
ls -la
ls -la src/
```

You should see:
- `streamlit_app.py` in root
- `src/` directory with `__init__.py`

**B. Update streamlit_app.py**

Make sure it has the sys.path fix:
```python
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
```

**C. Alternative: Use relative imports**

If above doesn't work, try changing imports in `streamlit_app.py`:
```python
# Instead of:
from src.data_handler import DataHandler

# Try:
try:
    from src.data_handler import DataHandler
except ImportError:
    import sys
    sys.path.append('.')
    from src.data_handler import DataHandler
```

### Issue 2: Missing Dependencies

**Symptom:**
```
ModuleNotFoundError: No module named 'xgboost'
```

**Solution:**
Check requirements.txt is in the root directory and properly formatted.

### Issue 3: Data Directory Issues

**Symptom:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'data/predictions'
```

**Solution:**

Add this to the beginning of functions that use data directories:
```python
os.makedirs("data/predictions", exist_ok=True)
os.makedirs("data/models", exist_ok=True)
os.makedirs("data/exports", exist_ok=True)
```

This is already in the code, but if you see this error, directories aren't being created.

### Issue 4: Large File Uploads

**Symptom:**
GitHub won't accept your push

**Solution:**

Add to `.gitignore`:
```
data/predictions/*.pkl
data/models/*.pkl
data/exports/*.xlsx
*.pyc
__pycache__/
```

### Issue 5: Slow App Performance

**Symptoms:**
- App takes long to load
- Frequent timeouts

**Solutions:**

**A. Enable Caching**

Add `@st.cache_data` to expensive functions:
```python
@st.cache_data(ttl=3600)  # Cache for 1 hour
def download_data():
    # Your data download code
    pass
```

**B. Reduce Lookback Days**

In the sidebar, reduce from 800 to 365 days.

**C. Optimize Parameter Ranges**

Use smaller ranges:
- Top K: 1-5 (instead of 1-10)
- Voting Days: 1-5 (instead of 1-10)

## 🔄 Redeployment Steps

If you need to redeploy after fixes:

1. **Update Code Locally**
```bash
# Make your changes
git add .
git commit -m "Fix deployment issues"
git push origin main
```

2. **In Streamlit Cloud**
- Go to your app dashboard
- Click "Reboot app" button
- Or it will auto-redeploy on push

3. **Check Logs**
- Click "Manage app" (bottom right)
- View logs for any errors

## 📋 Pre-Deployment Checklist

Before deploying, verify:

- [ ] `streamlit_app.py` is in root directory
- [ ] `requirements.txt` is in root directory
- [ ] `src/__init__.py` exists and is not empty
- [ ] All imports use `from src.module import Class`
- [ ] sys.path fix is in streamlit_app.py
- [ ] No large files in repo (use .gitignore)
- [ ] All code tested locally first
- [ ] Python version compatible (3.8-3.10)

## 🧪 Local Testing Before Deploy

Always test locally first:

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run app
streamlit run streamlit_app.py
```

If it works locally but fails on Streamlit Cloud, it's likely a path/import issue.

## 🔍 Debugging on Streamlit Cloud

### View Logs

1. Go to your app on Streamlit Cloud
2. Click "Manage app" (bottom right corner)
3. View the logs tab
4. Look for red error messages

### Common Log Messages

**"ModuleNotFoundError"**
- Import issue → Check file structure and sys.path

**"No module named 'X'"**  
- Missing dependency → Check requirements.txt

**"MemoryError"**
- Using too much RAM → Reduce data size or upgrade tier

**"Timeout"**
- App taking too long → Optimize code or use caching

## 💡 Best Practices

1. **Always Test Locally First**
   - Don't push untested code
   - Use same Python version as production

2. **Use Version Pinning**
   ```txt
   # Good
   streamlit==1.28.0
   
   # Also OK
   streamlit>=1.28.0,<2.0.0
   
   # Avoid (can break)
   streamlit
   ```

3. **Add Error Handling**
   ```python
   try:
       from src.data_handler import DataHandler
   except ImportError as e:
       st.error(f"Import error: {e}")
       st.info("Check file structure and requirements.txt")
   ```

4. **Use Secrets for Sensitive Data**
   - Don't hardcode API keys
   - Use Streamlit secrets management

5. **Monitor Performance**
   - Add `st.spinner()` for long operations
   - Use progress bars
   - Cache expensive operations

## 🆘 Still Having Issues?

### Option 1: Use Alternative Import Method

Create a new file `app.py` in root with all code in one file (no imports from src/).

### Option 2: Contact Support

- Streamlit Community Forum
- GitHub Issues
- Streamlit Cloud Support

### Option 3: Deploy Elsewhere

If Streamlit Cloud continues to have issues:
- Try Heroku (see DEPLOYMENT.md)
- Use Docker
- Deploy on your own server

## ✅ Success Verification

Your app is working correctly when:
- ✅ App loads without errors
- ✅ Can view predictions
- ✅ Can run optimization
- ✅ Can download results
- ✅ No red error messages in logs

## 📞 Quick Help

**Error**: ModuleNotFoundError
**Fix**: Add sys.path modification to streamlit_app.py

**Error**: No data found
**Fix**: Check internet connection and yfinance API

**Error**: Slow performance  
**Fix**: Reduce lookback_days, enable caching

**Error**: Memory issues
**Fix**: Reduce parameter ranges or upgrade Streamlit tier

---

**Updated Files:**
- ✅ streamlit_app.py (with sys.path fix)
- ✅ .streamlit/config.toml (new)
- ✅ src/__init__.py (verified)

Re-download the ZIP and redeploy! 🚀
