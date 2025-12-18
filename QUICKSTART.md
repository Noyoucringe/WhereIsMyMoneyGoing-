# 💰 Where Is My Money Going - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### 1. Install Dependencies (2 minutes)

```bash
# Install Python packages
pip install -r requirements.txt

# Install Tesseract OCR (Windows)
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
```

### 2. Launch the Dashboard (30 seconds)

```bash
streamlit run app.py
```

Your browser will open automatically at `http://localhost:8501`

### 3. Try Sample Data (1 minute)

1. In the sidebar, select **"Use Sample Data"**
2. Click **"📥 Load Sample Data"**
3. Click **"🏷️ Categorize Transactions"**
4. Explore the tabs: Overview, Visualizations, Analysis, Anomalies

### 4. Upload Your Own Data (1-2 minutes)

#### Option A: Upload CSV (Easiest)

1. Select **"Upload CSV"** in the sidebar
2. Upload a CSV with columns: `date`, `merchant`, `amount`
3. Click **"🏷️ Categorize Transactions"**

Sample CSV format:
```csv
date,merchant,amount
2024-01-15,Starbucks,5.75
2024-01-16,Amazon,45.99
2024-01-17,Netflix,15.99
```

#### Option B: Upload Bank Statement (PDF/Image)

1. Select **"Upload Bank Statement"** in the sidebar
2. Upload your PDF or image file
3. Click **"🚀 Process Statement"**
4. Wait for OCR processing
5. Click **"🏷️ Categorize Transactions"**

## 📊 Features Overview

### Overview Tab
- Key metrics (total spent, average transaction, etc.)
- Recent transactions table
- Category breakdown

### Visualizations Tab
- **Pie Chart**: Spending by category
- **Line Chart**: Spending over time
- **Bar Chart**: Top categories and merchants
- **Heatmap**: Category spending by month

### Analysis Tab
- Statistical summary
- Top merchants analysis
- Spending trends with moving averages

### Anomalies Tab
- Unusual transaction detection (3 methods):
  - Z-Score (statistical)
  - IQR (interquartile range)
  - Isolation Forest (ML)
- Duplicate transaction detection

### Export Tab
- Download CSV
- Download Excel (with category summary)
- Download text report

## 🎯 Common Use Cases

### Monthly Budget Review
```python
# Use the "Monthly Comparison" chart
# Set period to "Monthly" in time series
# Check category breakdown
```

### Find Subscription Charges
```python
# Look at "Subscriptions" category
# Check for recurring charges in Analysis tab
```

### Detect Fraudulent Transactions
```python
# Go to Anomalies tab
# Run anomaly detection with Z-Score method
# Review unusual transactions
```

### Track Spending Trends
```python
# Use "Spending Over Time" visualization
# Adjust moving average window
# Compare monthly totals
```

## ⚡ Command Line Usage

### Process a PDF Statement
```bash
python money.py --pdf statement.pdf --output results.csv
```

### Analyze CSV
```bash
python money.py --csv transactions.csv --report --visualize
```

### Quick Dashboard Launch
```bash
python money.py
# or
python money.py --dashboard
```

## 🔧 Troubleshooting

### "Tesseract not found"
- Install Tesseract: https://github.com/UB-Mannheim/tesseract/wiki
- Or use CSV upload instead

### "No transactions found"
- Try CSV upload first (more reliable)
- Check if PDF is text-based (not scanned image)
- Try sample data to verify setup

### Module import errors
```bash
pip install --upgrade -r requirements.txt
```

## 💡 Pro Tips

1. **Best Results**: Use CSV export from your bank (more accurate than OCR)

2. **Customize Categories**: Edit `categorizer.py` to add your own keywords

3. **Regular Analysis**: Upload monthly to track spending trends

4. **Export Data**: Save categorized data for future analysis in Excel

5. **Anomaly Threshold**: Adjust Z-Score threshold (lower = more sensitive)

## 📱 Project Structure

```
Where is my money going/
├── app.py                    # 🌐 Streamlit dashboard (START HERE)
├── money.py                  # 💻 CLI interface
├── ocr_extractor.py         # 📄 PDF/Image text extraction
├── transaction_parser.py    # 🔧 Parse raw text to structured data
├── categorizer.py           # 🏷️ Auto-categorize transactions
├── analyzer.py              # 📊 Analysis & anomaly detection
├── visualizer.py            # 📈 Create charts
├── requirements.txt         # 📦 Dependencies
└── sample_data/            # 📁 Sample CSV for testing
```

## 🎓 What You'll Learn

By using/modifying this project, you'll gain experience with:

- ✅ **OCR & Text Extraction** (Tesseract, pdf2image)
- ✅ **Data Cleaning** (pandas, regex)
- ✅ **Pattern Recognition** (keyword matching, categorization)
- ✅ **Data Visualization** (matplotlib, plotly, seaborn)
- ✅ **Statistical Analysis** (anomaly detection, trends)
- ✅ **Web Dashboards** (Streamlit)
- ✅ **File I/O** (CSV, Excel, PDF)

## 🚀 Next Steps

1. **Try with real data** from your bank
2. **Customize categories** in `categorizer.py`
3. **Add new analysis** in `analyzer.py`
4. **Create custom visualizations** in `visualizer.py`
5. **Share insights** by exporting reports

## 📚 Additional Resources

- **Sample CSV**: `sample_data/sample_transactions.csv`
- **Installation Guide**: `INSTALLATION.md`
- **Full README**: `README.md`

---

**Questions?** Check the module docstrings or run:
```bash
python money.py --help
```

**Ready to start?** Run:
```bash
streamlit run app.py
```

Happy expense tracking! 💰📊
