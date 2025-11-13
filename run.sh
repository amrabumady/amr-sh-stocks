#!/bin/bash

# EGX Stock Predictor - Run Script

echo "🚀 Starting EGX Stock Predictor..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "📥 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Run Streamlit app
echo ""
echo "✨ Launching Streamlit app..."
echo "📊 Dashboard will open at http://localhost:8501"
echo ""
streamlit run streamlit_app.py
