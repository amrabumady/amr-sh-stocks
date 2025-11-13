# 🤝 Contributing to EGX Stock Predictor

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Coding Standards](#coding-standards)

## 📜 Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Help others learn

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Git
- GitHub account

### Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/egx-stock-predictor.git
cd egx-stock-predictor
```

## 💻 Development Setup

1. **Create Virtual Environment**

```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. **Install Dependencies**

```bash
pip install -r requirements.txt
```

3. **Install Development Tools** (optional)

```bash
pip install black flake8 pytest
```

4. **Run Application**

```bash
streamlit run streamlit_app.py
```

## 🔨 Making Changes

### Branch Naming

Use descriptive branch names:
- `feature/add-new-indicator`
- `fix/prediction-bug`
- `docs/update-readme`
- `refactor/optimize-model`

### Create Branch

```bash
git checkout -b feature/your-feature-name
```

### Make Changes

1. Edit files
2. Test locally
3. Commit frequently with clear messages

```bash
git add .
git commit -m "Add: New technical indicator RSI-14"
```

### Commit Message Format

```
Type: Brief description

Detailed explanation if needed

- Type: Add, Fix, Update, Remove, Refactor, Docs
- Use present tense: "Add feature" not "Added feature"
- Be specific and clear
```

Examples:
```
Add: Volume-weighted RSI indicator
Fix: Handle missing data in prediction pipeline
Update: Improve parameter optimization speed
Docs: Add installation instructions for Windows
```

## 🧪 Testing

### Manual Testing

1. Run the app: `streamlit run streamlit_app.py`
2. Test all operations:
   - View predictions
   - Run optimization
   - Backtest analysis
3. Check error handling
4. Verify performance

### Code Quality

```bash
# Format code
black streamlit_app.py src/

# Check style
flake8 streamlit_app.py src/

# Run type checks (if using mypy)
mypy streamlit_app.py src/
```

## 📤 Submitting Changes

### Before Submitting

- [ ] Code runs without errors
- [ ] New features are documented
- [ ] Comments explain complex logic
- [ ] No debug/print statements left
- [ ] Tested manually

### Create Pull Request

1. **Push Changes**

```bash
git push origin feature/your-feature-name
```

2. **Open PR on GitHub**
   - Go to repository
   - Click "New Pull Request"
   - Select your branch
   - Fill in description

3. **PR Description Template**

```markdown
## Description
Brief overview of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
How you tested the changes

## Screenshots (if applicable)
Add screenshots for UI changes

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No warnings or errors
```

### Review Process

- Maintainer will review your PR
- Address any feedback
- Once approved, PR will be merged

## 📐 Coding Standards

### Python Style

Follow PEP 8:
- 4 spaces for indentation
- Max line length: 88 characters (Black default)
- Use meaningful variable names
- Add docstrings to functions

### Function Documentation

```python
def calculate_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    """
    Calculate Relative Strength Index
    
    Args:
        series: Price series
        period: RSI period (default: 14)
        
    Returns:
        Series with RSI values
        
    Raises:
        ValueError: If period < 1
    """
    # Implementation
```

### Code Organization

```python
# Imports at top
import standard_library
import third_party
from local_module import function

# Constants
CONSTANT_NAME = value

# Classes
class MyClass:
    pass

# Functions
def my_function():
    pass

# Main code
if __name__ == "__main__":
    pass
```

## 🎯 Areas for Contribution

### High Priority

- Add more technical indicators
- Improve prediction accuracy
- Optimize performance
- Add unit tests
- Enhance UI/UX

### Good First Issues

- Fix typos in documentation
- Add examples
- Improve error messages
- Add input validation
- Create tutorials

### Feature Ideas

- Multi-timeframe analysis
- Risk management features
- Portfolio optimization
- Real-time alerts
- Mobile app support
- API integration

## 🐛 Bug Reports

### Before Reporting

1. Check existing issues
2. Verify it's reproducible
3. Collect error messages
4. Note your environment

### Bug Report Template

```markdown
**Describe the bug**
Clear description

**To Reproduce**
Steps to reproduce:
1. Go to...
2. Click on...
3. See error

**Expected behavior**
What should happen

**Screenshots**
If applicable

**Environment:**
- OS: [e.g., Windows 10]
- Python version: [e.g., 3.9.7]
- Streamlit version: [e.g., 1.28.0]

**Additional context**
Any other information
```

## 💡 Feature Requests

### Feature Request Template

```markdown
**Feature Description**
Clear description of proposed feature

**Use Case**
Why this feature is needed

**Possible Implementation**
Ideas on how to implement

**Alternatives**
Alternative solutions considered
```

## 📚 Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [XGBoost Documentation](https://xgboost.readthedocs.io)
- [pandas Documentation](https://pandas.pydata.org/docs/)
- [Python Style Guide (PEP 8)](https://pep8.org)

## ❓ Questions?

- Open a GitHub Discussion
- Check existing issues
- Contact via ClientN.com

## 🎉 Recognition

Contributors will be:
- Added to CONTRIBUTORS.md
- Mentioned in release notes
- Credited in documentation

---

Thank you for contributing to EGX Stock Predictor! 🚀

Every contribution, no matter how small, makes a difference.
