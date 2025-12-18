# 💰 Where Is My Money Going?

A comprehensive expense tracking application that analyzes bank statements using OCR, categorizes spending, detects anomalies, and provides interactive visualizations.

## Features

- **📄 OCR Processing**: Extract transactions from PDFs and images
- **🧹 Data Cleaning**: Parse and structure messy transaction data
- **🏷️ Smart Categorization**: Automatically categorize expenses
- **📊 Visualization**: Interactive charts and dashboards
- **🔍 Anomaly Detection**: Identify unusual spending patterns
- **💾 Export**: Save insights to CSV/Excel

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Install Tesseract OCR:
   - **Windows**: Download from https://github.com/UB-Mannheim/tesseract/wiki
   - **macOS**: `brew install tesseract`
   - **Linux**: `sudo apt-get install tesseract-ocr`

## Usage

### Run the Streamlit Dashboard
```bash
streamlit run app.py
```

### Use Individual Modules
```python
from ocr_extractor import extract_from_pdf, extract_from_image
from transaction_parser import parse_transactions
from categorizer import categorize_transactions
from analyzer import analyze_spending, detect_anomalies
from visualizer import create_spending_charts

# Extract text from bank statement
text = extract_from_pdf("statement.pdf")

# Parse transactions
transactions = parse_transactions(text)

# Categorize and analyze
categorized = categorize_transactions(transactions)
insights = analyze_spending(categorized)
```

## Project Structure

```
Where is my money going/
├── requirements.txt          # Python dependencies
├── README.md                # This file
├── app.py                   # Streamlit dashboard
├── ocr_extractor.py         # OCR and text extraction
├── transaction_parser.py    # Transaction parsing logic
├── categorizer.py           # Expense categorization
├── analyzer.py              # Analysis and anomaly detection
├── visualizer.py            # Chart generation
└── sample_data/             # Sample bank statements
```

## Skills Demonstrated

- OCR and text extraction
- Data cleaning and regex parsing
- Machine learning (categorization)
- Statistical analysis
- Data visualization
- Web dashboard development
- Anomaly detection
