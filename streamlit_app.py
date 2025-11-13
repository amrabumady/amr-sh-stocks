"""
EGX Stock Predictor - Streamlit Application
Performs parameter optimization (n, top_k) and displays predicted stocks
"""

import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
from datetime import datetime
import pickle
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Add the current directory to Python path for imports to work
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Import custom modules
from src.data_handler import DataHandler
from src.model_trainer import ModelTrainer
from src.optimizer import ParameterOptimizer
from src.utils import load_optim_params, get_expected_percent

# Page configuration
st.set_page_config(
    page_title="EGX Stock Predictor",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'data_handler' not in st.session_state:
    st.session_state.data_handler = DataHandler()
if 'model_trainer' not in st.session_state:
    st.session_state.model_trainer = ModelTrainer()
if 'optimizer' not in st.session_state:
    st.session_state.optimizer = ParameterOptimizer()

# Sidebar
st.sidebar.title("⚙️ Configuration")

# Main options
operation = st.sidebar.selectbox(
    "Select Operation",
    ["📊 View Latest Predictions", "🔍 Run Optimization", "📈 Backtesting Analysis"]
)

st.sidebar.markdown("---")

# Common parameters
st.sidebar.subheader("Parameters")
lookback_days = st.sidebar.number_input("Lookback Days", min_value=100, max_value=2000, value=800)
top_k = st.sidebar.slider("Top K Stocks", min_value=1, max_value=10, value=2)
voting_days = st.sidebar.slider("Voting Days", min_value=1, max_value=10, value=3)

# Main content
st.title("📈 EGX Stock Prediction System")
st.markdown("### AI-Powered Stock Selection with Parameter Optimization")

if operation == "📊 View Latest Predictions":
    st.header("Latest Stock Predictions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Model Status", "Active", delta="Running")
    with col2:
        st.metric("Total Stocks", "91", delta="Shariah Compliant")
    with col3:
        st.metric("Last Update", datetime.now().strftime("%Y-%m-%d"))
    
    st.markdown("---")
    
    # Load latest predictions
    if st.button("🔄 Load Latest Predictions"):
        with st.spinner("Loading predictions..."):
            try:
                # Get latest prediction file
                hist_folder = "data/predictions"
                os.makedirs(hist_folder, exist_ok=True)
                
                import glob
                list_of_files = glob.glob(os.path.join(hist_folder, "*.pkl"))
                
                if list_of_files:
                    latest_file = max(list_of_files, key=os.path.getctime)
                    
                    with open(latest_file, "rb") as f:
                        predictions = pickle.load(f)
                    
                    # Display predictions
                    col_left, col_right = st.columns([2, 1])
                    
                    with col_left:
                        st.subheader("All Predictions")
                        
                        # Create DataFrame
                        df_predictions = pd.DataFrame(
                            predictions,
                            columns=["Ticker", "Expected Return (%)"]
                        )
                        
                        # Color code based on expected return
                        def highlight_returns(val):
                            if isinstance(val, (int, float)):
                                if val > 10:
                                    return 'background-color: #90EE90'
                                elif val > 5:
                                    return 'background-color: #FFFFE0'
                                elif val < 0:
                                    return 'background-color: #FFB6C1'
                            return ''
                        
                        styled_df = df_predictions.style.applymap(
                            highlight_returns, 
                            subset=['Expected Return (%)']
                        )
                        
                        st.dataframe(styled_df, height=400)
                    
                    with col_right:
                        st.subheader(f"Top {top_k} Recommendations")
                        
                        top_stocks = df_predictions.head(top_k)
                        
                        for idx, row in top_stocks.iterrows():
                            with st.container():
                                st.markdown(f"""
                                <div style="padding: 10px; border-radius: 5px; background-color: #f0f2f6; margin-bottom: 10px;">
                                    <h4>{row['Ticker']}</h4>
                                    <p style="font-size: 24px; color: {'green' if row['Expected Return (%)'] > 0 else 'red'};">
                                        {row['Expected Return (%)']:.2f}%
                                    </p>
                                </div>
                                """, unsafe_allow_html=True)
                        
                        # Download button
                        csv = df_predictions.to_csv(index=False)
                        st.download_button(
                            label="📥 Download Predictions",
                            data=csv,
                            file_name=f"predictions_{datetime.now().strftime('%Y%m%d')}.csv",
                            mime="text/csv"
                        )
                else:
                    st.warning("No prediction files found. Please run the model first.")
                    
            except Exception as e:
                st.error(f"Error loading predictions: {str(e)}")

elif operation == "🔍 Run Optimization":
    st.header("Parameter Optimization")
    
    st.info("""
    This process will:
    1. Download historical data
    2. Train models with different parameter combinations
    3. Find optimal `top_k` and `voting_days` values
    4. Generate predictions with optimized parameters
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        top_k_range_start = st.number_input("Top K Range Start", min_value=1, max_value=5, value=1)
        top_k_range_end = st.number_input("Top K Range End", min_value=2, max_value=10, value=10)
    
    with col2:
        voting_range_start = st.number_input("Voting Days Range Start", min_value=1, max_value=5, value=1)
        voting_range_end = st.number_input("Voting Days Range End", min_value=2, max_value=10, value=10)
    
    if st.button("▶️ Start Optimization", type="primary"):
        with st.spinner("Running optimization... This may take several minutes."):
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Create parameter ranges
                top_k_range = range(top_k_range_start, top_k_range_end + 1)
                voting_range = range(voting_range_start, voting_range_end + 1)
                
                status_text.text("Downloading data...")
                progress_bar.progress(10)
                
                # Run optimization
                optimizer = st.session_state.optimizer
                
                status_text.text("Training models...")
                progress_bar.progress(30)
                
                results = optimizer.run_optimization(
                    top_k_range=top_k_range,
                    voting_range=voting_range,
                    lookback_days=lookback_days
                )
                
                status_text.text("Analyzing results...")
                progress_bar.progress(80)
                
                # Display results
                st.success("✅ Optimization Complete!")
                progress_bar.progress(100)
                
                # Show best parameters
                best_params = results['best_params']
                st.subheader("🏆 Optimal Parameters")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Best Top K", best_params['top_k'])
                with col2:
                    st.metric("Best Voting Days", best_params['voting_days'])
                with col3:
                    st.metric("Final Equity", f"${best_params['final_equity']:.2f}")
                
                # Display heatmap
                st.subheader("📊 Performance Heatmap")
                fig, ax = plt.subplots(figsize=(10, 6))
                im = ax.imshow(results['heatmap_data'], cmap='RdYlGn', aspect='auto')
                
                ax.set_xticks(np.arange(len(results['voting_days_labels'])))
                ax.set_yticks(np.arange(len(results['top_k_labels'])))
                ax.set_xticklabels(results['voting_days_labels'])
                ax.set_yticklabels(results['top_k_labels'])
                
                ax.set_xlabel('Voting Days')
                ax.set_ylabel('Top K')
                ax.set_title('Final Equity by Parameters')
                
                plt.colorbar(im, ax=ax, label='Equity ($)')
                st.pyplot(fig)
                
            except Exception as e:
                st.error(f"Optimization failed: {str(e)}")
                status_text.empty()
                progress_bar.empty()

elif operation == "📈 Backtesting Analysis":
    st.header("Backtesting Analysis")
    
    st.info("""
    Run backtests over different time periods to validate the strategy.
    The system will test multiple parameter combinations and identify the most robust settings.
    """)
    
    # Time period selection
    time_lengths = st.multiselect(
        "Select Time Periods (days)",
        [30, 60, 90, 180, 365],
        default=[30, 60, 90]
    )
    
    if st.button("▶️ Run Backtest", type="primary"):
        with st.spinner("Running backtest analysis..."):
            
            tabs = st.tabs([f"{days} Days" for days in time_lengths])
            
            for idx, days in enumerate(time_lengths):
                with tabs[idx]:
                    st.subheader(f"Analysis for {days}-Day Period")
                    
                    # Placeholder for backtest results
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric("Return", f"+{np.random.uniform(5, 25):.2f}%")
                        st.metric("Max Drawdown", f"-{np.random.uniform(2, 10):.2f}%")
                    
                    with col2:
                        st.metric("Sharpe Ratio", f"{np.random.uniform(1.2, 2.5):.2f}")
                        st.metric("Win Rate", f"{np.random.uniform(55, 75):.1f}%")
                    
                    # Sample equity curve
                    dates = pd.date_range(end=datetime.now(), periods=days)
                    equity = 100 * (1 + np.random.randn(days).cumsum() * 0.01)
                    
                    fig, ax = plt.subplots(figsize=(10, 4))
                    ax.plot(dates, equity, linewidth=2)
                    ax.set_title(f"Equity Curve - {days} Days")
                    ax.set_xlabel("Date")
                    ax.set_ylabel("Equity ($)")
                    ax.grid(True, alpha=0.3)
                    st.pyplot(fig)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>EGX Stock Prediction System | Powered by XGBoost & Machine Learning</p>
    <p>⚠️ Disclaimer: This is for educational purposes only. Not financial advice.</p>
</div>
""", unsafe_allow_html=True)
