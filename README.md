# WhereIsMyMoneyGoing - Expense Tracker 💰

A comprehensive expense tracking application that analyzes bank statements using OCR, categorizes spending, detects anomalies, and provides interactive visualizations.

## Features ✨

- **📄 OCR Processing**: Extract transactions from bank statement images and PDFs using advanced OCR
- **🏷️ Automatic Categorization**: Intelligently categorize expenses into 13+ categories (Groceries, Restaurants, Transportation, etc.)
- **🔍 Anomaly Detection**: Detect unusual spending patterns using multiple methods:
  - Statistical analysis (Z-score, IQR)
  - Machine learning (Isolation Forest)
  - Frequency-based detection
- **📊 Interactive Visualizations**: Beautiful, interactive charts and dashboards:
  - Category pie charts
  - Spending timelines
  - Monthly trend analysis
  - Heatmaps by day of week
  - Comprehensive dashboards

## Installation 🚀

### Prerequisites

- Python 3.8 or higher
- Tesseract OCR (for image processing)

#### Install Tesseract

**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr
```

**macOS:**
```bash
brew install tesseract
```

**Windows:**
Download installer from [GitHub releases](https://github.com/UB-Mannheim/tesseract/wiki)

### Install Package

```bash
# Clone the repository
git clone https://github.com/Noyoucringe/WhereIsMyMoneyGoing-.git
cd WhereIsMyMoneyGoing-

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

## Usage 📖

### Quick Start with Demo

Run the demo to see all features in action:

```bash
python demo.py
```

This will:
1. Generate 100+ sample transactions
2. Automatically categorize them
3. Detect anomalies
4. Create interactive visualizations in the `output/` directory

### Command Line Interface

#### Process a Bank Statement

```bash
expense-tracker process statement.pdf --output transactions.json
```

Supported formats: JPG, PNG, PDF

#### Analyze Transactions

```bash
expense-tracker analyze --load transactions.json --visualize
```

#### Create Visualizations

```bash
expense-tracker visualize --load transactions.json --output-dir my_charts
```

#### List Transactions

```bash
expense-tracker list --load transactions.json --limit 20
```

### Python API

```python
from expense_tracker.ocr import BankStatementOCR
from expense_tracker.categorizer import ExpenseCategorizer
from expense_tracker.anomaly_detector import AnomalyDetector
from expense_tracker.visualizer import ExpenseVisualizer

# Process bank statement
ocr = BankStatementOCR()
transactions = ocr.process_statement('statement.pdf')

# Categorize expenses
categorizer = ExpenseCategorizer()
categorized = categorizer.categorize_transactions(transactions)

# Detect anomalies
detector = AnomalyDetector()
anomalies = detector.detect_all_anomalies(transactions)

# Create visualizations
visualizer = ExpenseVisualizer()
visualizer.create_dashboard(transactions, 'dashboard.html')
```

## Project Structure 📁

```
WhereIsMyMoneyGoing-/
├── expense_tracker/
│   ├── __init__.py
│   ├── ocr.py                 # OCR processing
│   ├── models.py              # Data models
│   ├── categorizer.py         # Expense categorization
│   ├── anomaly_detector.py    # Anomaly detection
│   ├── visualizer.py          # Visualization engine
│   └── cli.py                 # Command-line interface
├── tests/
│   ├── __init__.py
│   └── test_expense_tracker.py
├── demo.py                    # Demo script
├── requirements.txt           # Dependencies
├── setup.py                   # Package setup
└── README.md
```

## Categories 🏷️

The application automatically categorizes transactions into:

- 🛒 **Groceries**: Supermarkets, food stores
- 🍽️ **Restaurants**: Dining, cafes, food delivery
- 🚗 **Transportation**: Gas, rideshare, public transit
- 💡 **Utilities**: Electric, water, internet, phone
- 🎬 **Entertainment**: Streaming, movies, concerts
- 🛍️ **Shopping**: Retail, online shopping
- 🏥 **Healthcare**: Pharmacy, medical, dental
- 🏠 **Housing**: Rent, mortgage, HOA
- 📚 **Education**: Tuition, books, courses
- 💪 **Fitness**: Gym, sports, yoga
- ✈️ **Travel**: Hotels, flights, vacation
- 📱 **Subscriptions**: Monthly services
- 🔒 **Insurance**: Health, auto, home

## Anomaly Detection Methods 🔍

### 1. Statistical Analysis
- Z-score method (3-sigma rule)
- Interquartile Range (IQR) method
- Per-category baseline statistics

### 2. Machine Learning
- Isolation Forest algorithm
- Multi-feature analysis (amount, date, category)
- Automatic outlier detection

### 3. Frequency-Based
- Unusual transaction frequency detection
- Duplicate transaction patterns
- Time-series analysis

## Testing 🧪

Run the test suite:

```bash
python -m pytest tests/
```

Or run tests directly:

```bash
python tests/test_expense_tracker.py
```

## Dependencies 📦

- **pytesseract**: OCR engine wrapper
- **Pillow**: Image processing
- **opencv-python**: Advanced image preprocessing
- **pdf2image**: PDF to image conversion
- **pandas**: Data manipulation
- **numpy**: Numerical computations
- **scikit-learn**: Machine learning algorithms
- **matplotlib**: Static plotting
- **seaborn**: Statistical visualizations
- **plotly**: Interactive visualizations

## Examples 📸

### Dashboard View
The application creates comprehensive HTML dashboards with:
- Category breakdown (pie chart)
- Spending timeline with anomaly markers
- Monthly trends
- Top transactions

### Anomaly Detection
Automatically flags:
- Unusually large purchases
- Duplicate/fraudulent transactions
- Out-of-pattern spending
- Frequency anomalies

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

## License 📄

This project is open source and available under the MIT License.

## Acknowledgments 🙏

- Tesseract OCR for text extraction
- Plotly for beautiful visualizations
- scikit-learn for ML algorithms

## Future Enhancements 🚀

- [ ] Web interface
- [ ] Budget tracking and alerts
- [ ] Recurring transaction detection
- [ ] Export to multiple formats (Excel, CSV)
- [ ] Mobile app integration
- [ ] Bank API integration
- [ ] Multi-currency support
- [ ] Custom rule engine

---

**Made with ❤️ for better financial insights**
