"""
💰 Where Is My Money Going?
Streamlit Dashboard for Expense Tracking and Analysis
"""

import streamlit as st
import pandas as pd
import os
from datetime import datetime
import io

# Import our custom modules
from ocr_extractor import OCRExtractor
from transaction_parser import TransactionParser
from categorizer import TransactionCategorizer
from analyzer import SpendingAnalyzer
from visualizer import SpendingVisualizer


# Page configuration
st.set_page_config(
    page_title="💰 Where Is My Money Going?",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1E88E5;
    }
    </style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables"""
    if 'df' not in st.session_state:
        st.session_state.df = None
    if 'categorized' not in st.session_state:
        st.session_state.categorized = False


def process_uploaded_file(uploaded_file, tesseract_path=None):
    """Process uploaded file and extract transactions"""
    try:
        # Initialize extractors
        ocr = OCRExtractor(tesseract_path)
        parser = TransactionParser()
        
        file_type = uploaded_file.type
        
        with st.spinner('🔍 Extracting text from document...'):
            # Extract text based on file type
            if 'pdf' in file_type:
                text = ocr.extract_from_bytes(uploaded_file.read(), 'pdf')
            elif 'image' in file_type:
                text = ocr.extract_from_bytes(uploaded_file.read(), 'image')
            else:
                st.error(f"Unsupported file type: {file_type}")
                return None
        
        st.success('✅ Text extracted successfully!')
        
        with st.spinner('📊 Parsing transactions...'):
            # Parse transactions
            df = parser.parse_transactions(text)
        
        if len(df) > 0:
            st.success(f'✅ Found {len(df)} transactions!')
            return df
        else:
            st.warning('⚠️ No transactions found. Try a different file or upload CSV.')
            return None
            
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        return None


def main():
    """Main application"""
    initialize_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">💰 Where Is My Money Going?</h1>', unsafe_allow_html=True)
    st.markdown('---')
    
    # Sidebar
    with st.sidebar:
        st.header("📁 Data Input")
        
        # File upload options
        upload_method = st.radio(
            "Choose input method:",
            ["Upload Bank Statement (PDF/Image)", "Upload CSV", "Use Sample Data"]
        )
        
        if upload_method == "Upload Bank Statement (PDF/Image)":
            st.info("📄 Upload a scanned bank statement or screenshot")
            
            # Tesseract path (optional)
            with st.expander("⚙️ Advanced Settings"):
                tesseract_path = st.text_input(
                    "Tesseract Path (optional)",
                    placeholder="C:/Program Files/Tesseract-OCR/tesseract.exe"
                )
                if not tesseract_path:
                    tesseract_path = None
            
            uploaded_file = st.file_uploader(
                "Upload file",
                type=['pdf', 'png', 'jpg', 'jpeg'],
                help="Upload a PDF or image of your bank statement"
            )
            
            if uploaded_file is not None:
                if st.button('🚀 Process Statement', type='primary'):
                    df = process_uploaded_file(uploaded_file, tesseract_path)
                    if df is not None:
                        st.session_state.df = df
                        st.session_state.categorized = False
        
        elif upload_method == "Upload CSV":
            st.info("📊 Upload a CSV file with transaction data")
            st.caption("Required columns: date, merchant, amount")
            
            uploaded_csv = st.file_uploader(
                "Upload CSV",
                type=['csv'],
                help="Upload a CSV file with columns: date, merchant, amount"
            )
            
            if uploaded_csv is not None:
                try:
                    df = pd.read_csv(uploaded_csv)
                    
                    # Standardize columns
                    parser = TransactionParser()
                    df = parser._standardize_columns(df)
                    
                    st.session_state.df = df
                    st.session_state.categorized = False
                    st.success(f'✅ Loaded {len(df)} transactions!')
                except Exception as e:
                    st.error(f"Error loading CSV: {str(e)}")
        
        else:  # Sample Data
            st.info("📈 Load sample transaction data for demo")
            
            if st.button('📥 Load Sample Data', type='primary'):
                # Create sample data
                sample_data = {
                    'date': pd.date_range(start='2024-01-01', periods=50, freq='D'),
                    'merchant': [
                        'Starbucks', 'Amazon', 'Shell Gas', 'Walmart', 'Netflix',
                        'Uber', 'McDonald\'s', 'Target', 'CVS Pharmacy', 'Electric Company'
                    ] * 5,
                    'amount': [5.75, 45.99, 52.30, 78.45, 15.99,
                              12.50, 8.25, 34.67, 23.45, 125.00] * 5
                }
                df = pd.DataFrame(sample_data)
                
                st.session_state.df = df
                st.session_state.categorized = False
                st.success('✅ Sample data loaded!')
        
        # Categorize button
        if st.session_state.df is not None and not st.session_state.categorized:
            st.markdown("---")
            if st.button('🏷️ Categorize Transactions', type='primary'):
                with st.spinner('Categorizing transactions...'):
                    categorizer = TransactionCategorizer()
                    st.session_state.df = categorizer.categorize_transactions(st.session_state.df)
                    st.session_state.categorized = True
                st.success('✅ Transactions categorized!')
                st.rerun()
    
    # Main content
    if st.session_state.df is not None:
        df = st.session_state.df
        
        # Display tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Overview", 
            "📈 Visualizations", 
            "🔍 Analysis", 
            "⚠️ Anomalies",
            "💾 Export"
        ])
        
        # Tab 1: Overview
        with tab1:
            st.header("Transaction Overview")
            
            # Key metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    label="Total Transactions",
                    value=f"{len(df):,}"
                )
            
            with col2:
                st.metric(
                    label="Total Spent",
                    value=f"${df['amount'].sum():,.2f}"
                )
            
            with col3:
                st.metric(
                    label="Average Transaction",
                    value=f"${df['amount'].mean():,.2f}"
                )
            
            with col4:
                st.metric(
                    label="Largest Transaction",
                    value=f"${df['amount'].max():,.2f}"
                )
            
            st.markdown("---")
            
            # Recent transactions
            st.subheader("Recent Transactions")
            
            # Display columns based on what's available
            display_cols = ['date', 'merchant', 'amount']
            if 'category' in df.columns:
                display_cols.append('category')
            
            st.dataframe(
                df[display_cols].head(20),
                use_container_width=True,
                hide_index=True
            )
            
            # Category breakdown (if available)
            if 'category' in df.columns:
                st.markdown("---")
                st.subheader("Category Breakdown")
                
                categorizer = TransactionCategorizer()
                summary = categorizer.get_category_summary(df)
                
                st.dataframe(summary, use_container_width=True)
        
        # Tab 2: Visualizations
        with tab2:
            st.header("Spending Visualizations")
            
            visualizer = SpendingVisualizer(df)
            
            # Category pie chart
            if 'category' in df.columns:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Spending by Category")
                    fig = visualizer.create_pie_chart(interactive=True)
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    st.subheader("Top Categories")
                    fig = visualizer.create_category_bar_chart(interactive=True)
                    st.plotly_chart(fig, use_container_width=True)
            
            # Time series
            if 'date' in df.columns:
                st.markdown("---")
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    period = st.selectbox(
                        "Time Period",
                        options=['D', 'W', 'M'],
                        format_func=lambda x: {'D': 'Daily', 'W': 'Weekly', 'M': 'Monthly'}[x],
                        index=2
                    )
                
                st.subheader("Spending Over Time")
                fig = visualizer.create_spending_over_time(period=period, interactive=True)
                st.plotly_chart(fig, use_container_width=True)
                
                st.markdown("---")
                st.subheader("Monthly Comparison")
                fig = visualizer.create_monthly_comparison(interactive=True)
                st.plotly_chart(fig, use_container_width=True)
            
            # Top merchants
            if 'merchant' in df.columns:
                st.markdown("---")
                st.subheader("Top Merchants")
                
                top_n = st.slider("Number of merchants to show", 5, 20, 10)
                fig = visualizer.create_top_merchants_chart(top_n=top_n, interactive=True)
                st.plotly_chart(fig, use_container_width=True)
            
            # Heatmap
            if 'category' in df.columns and 'date' in df.columns:
                st.markdown("---")
                st.subheader("Category Spending Heatmap")
                fig = visualizer.create_spending_heatmap(interactive=True)
                st.plotly_chart(fig, use_container_width=True)
        
        # Tab 3: Analysis
        with tab3:
            st.header("Spending Analysis")
            
            analyzer = SpendingAnalyzer(df)
            
            # Get insights
            insights = analyzer.get_insights()
            
            # Basic statistics
            st.subheader("📊 Statistical Summary")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Mean", f"${insights['basic_stats']['average_transaction']:.2f}")
                st.metric("Std Dev", f"${insights['basic_stats']['std_deviation']:.2f}")
            
            with col2:
                st.metric("Median", f"${insights['basic_stats']['median_transaction']:.2f}")
                st.metric("Total Spent", f"${insights['basic_stats']['total_spent']:.2f}")
            
            with col3:
                st.metric("Max", f"${insights['basic_stats']['largest_transaction']:.2f}")
                st.metric("Min", f"${insights['basic_stats']['smallest_transaction']:.2f}")
            
            st.markdown("---")
            
            # Top merchants
            st.subheader("🏪 Top Merchants")
            top_merchants = analyzer.get_top_merchants(n=10)
            st.dataframe(top_merchants, use_container_width=True)
            
            # Spending trends
            if 'date' in df.columns:
                st.markdown("---")
                st.subheader("📈 Spending Trends")
                
                window = st.slider("Moving average window (days)", 3, 30, 7)
                trends = analyzer.get_spending_trends(window=window)
                
                st.line_chart(trends.set_index('date')[['amount', 'moving_avg']])
        
        # Tab 4: Anomalies
        with tab4:
            st.header("Anomaly Detection")
            
            analyzer = SpendingAnalyzer(df)
            
            # Detection method
            col1, col2 = st.columns([1, 2])
            
            with col1:
                method = st.selectbox(
                    "Detection Method",
                    options=['zscore', 'iqr', 'isolation'],
                    format_func=lambda x: {
                        'zscore': 'Z-Score',
                        'iqr': 'Interquartile Range',
                        'isolation': 'Isolation Forest'
                    }[x]
                )
            
            with col2:
                if method == 'zscore':
                    threshold = st.slider("Z-Score Threshold", 1.5, 4.0, 2.5, 0.1)
                else:
                    threshold = 3.0
            
            # Detect anomalies
            if st.button('🔍 Detect Anomalies', type='primary'):
                with st.spinner('Detecting anomalies...'):
                    anomalies = analyzer.detect_anomalies(method=method, threshold=threshold)
                
                if len(anomalies) > 0:
                    st.warning(f"⚠️ Found {len(anomalies)} anomalous transactions")
                    
                    display_cols = ['date', 'merchant', 'amount', 'reason']
                    display_cols = [col for col in display_cols if col in anomalies.columns]
                    
                    st.dataframe(
                        anomalies[display_cols],
                        use_container_width=True,
                        hide_index=True
                    )
                else:
                    st.success("✅ No anomalies detected!")
            
            st.markdown("---")
            
            # Duplicate detection
            st.subheader("🔄 Duplicate Transaction Detection")
            
            time_window = st.slider("Time window (days)", 0, 7, 1)
            
            if st.button('🔍 Find Duplicates', type='primary'):
                with st.spinner('Searching for duplicates...'):
                    duplicates = analyzer.find_duplicate_transactions(time_window=time_window)
                
                if len(duplicates) > 0:
                    st.warning(f"⚠️ Found {len(duplicates)} potential duplicate pairs")
                    st.dataframe(duplicates, use_container_width=True, hide_index=True)
                else:
                    st.success("✅ No duplicate transactions found!")
        
        # Tab 5: Export
        with tab5:
            st.header("Export Data")
            
            st.write("Download your analyzed transaction data in various formats.")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # Export to CSV
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name=f"transactions_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col2:
                # Export to Excel
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                    df.to_excel(writer, sheet_name='Transactions', index=False)
                    
                    if 'category' in df.columns:
                        categorizer = TransactionCategorizer()
                        summary = categorizer.get_category_summary(df)
                        summary.to_excel(writer, sheet_name='Category Summary')
                
                st.download_button(
                    label="📥 Download Excel",
                    data=buffer.getvalue(),
                    file_name=f"transactions_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            
            with col3:
                # Export summary report
                analyzer = SpendingAnalyzer(df)
                insights = analyzer.get_insights()
                
                report = f"""
SPENDING REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
=====================================

SUMMARY
-------
Total Transactions: {insights['basic_stats']['total_transactions']:,}
Total Spent: ${insights['basic_stats']['total_spent']:,.2f}
Average Transaction: ${insights['basic_stats']['average_transaction']:,.2f}
Median Transaction: ${insights['basic_stats']['median_transaction']:,.2f}
Largest Transaction: ${insights['basic_stats']['largest_transaction']:,.2f}
Smallest Transaction: ${insights['basic_stats']['smallest_transaction']:,.2f}

INSIGHTS
--------
Anomalies Detected: {insights['anomaly_count']}
Potential Duplicates: {insights['potential_duplicates']}
"""
                
                if 'top_category' in insights:
                    report += f"\nTop Category: {insights['top_category']} (${insights['top_category_amount']:,.2f})"
                
                if 'top_merchant' in insights:
                    report += f"\nTop Merchant: {insights['top_merchant']} (${insights['top_merchant_amount']:,.2f})"
                
                st.download_button(
                    label="📥 Download Report",
                    data=report,
                    file_name=f"spending_report_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
    
    else:
        # Welcome screen
        st.info("👈 Upload your bank statement or CSV file to get started!")
        
        st.markdown("""
        ### 🎯 Features
        
        - **📄 OCR Processing**: Extract transactions from PDFs and images
        - **🧹 Data Cleaning**: Parse and structure messy transaction data
        - **🏷️ Smart Categorization**: Automatically categorize your expenses
        - **📊 Visualization**: Interactive charts and dashboards
        - **🔍 Anomaly Detection**: Identify unusual spending patterns
        - **💾 Export**: Save insights to CSV/Excel
        
        ### 📋 Instructions
        
        1. **Upload Data**: Choose your preferred input method from the sidebar
        2. **Categorize**: Click "Categorize Transactions" to analyze your spending
        3. **Explore**: Navigate through tabs to view insights and visualizations
        4. **Export**: Download your analyzed data in various formats
        
        ### 🔧 Supported Formats
        
        - PDF bank statements (scanned or digital)
        - Images (PNG, JPG, JPEG)
        - CSV files with columns: date, merchant, amount
        """)


if __name__ == "__main__":
    main()
