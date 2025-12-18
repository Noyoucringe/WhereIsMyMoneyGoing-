# 💰 Where Is My Money Going - Installation Guide

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Tesseract OCR (for PDF/image processing)

## Step-by-Step Installation

### 1. Install Python Dependencies

Open PowerShell/Command Prompt in the project directory and run:

```bash
pip install -r requirements.txt
```

Or install packages individually:

```bash
pip install pandas numpy pytesseract Pillow pdf2image PyPDF2 matplotlib seaborn plotly streamlit scikit-learn scipy python-dateutil openpyxl
```

### 2. Install Tesseract OCR

#### Windows

1. Download Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki
2. Run the installer (e.g., `tesseract-ocr-w64-setup-5.3.1.20230401.exe`)
3. During installation, note the installation path (default: `C:\Program Files\Tesseract-OCR`)
4. Add Tesseract to your PATH or configure it in the app

#### macOS

```bash
brew install tesseract
```

#### Linux (Ubuntu/Debian)

```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

### 3. Install Poppler (for PDF to Image conversion)

#### Windows

1. Download Poppler from: http://blog.alivate.com.au/poppler-windows/
2. Extract to a folder (e.g., `C:\poppler`)
3. Add the `bin` folder to your PATH (e.g., `C:\poppler\bin`)

#### macOS

```bash
brew install poppler
```

#### Linux

```bash
sudo apt-get install poppler-utils
```

## Running the Application

### Option 1: Streamlit Dashboard (Recommended)

```bash
streamlit run app.py
```

The dashboard will open in your browser at `http://localhost:8501`

### Option 2: Use Individual Modules

```python
from ocr_extractor import extract_from_pdf
from transaction_parser import parse_transactions
from categorizer import categorize_transactions
from analyzer import analyze_spending
from visualizer import create_spending_charts

# Extract text
text = extract_from_pdf("statement.pdf")

# Parse transactions
df = parse_transactions(text)

# Categorize
df = categorize_transactions(df)

# Analyze
insights = analyze_spending(df)

# Visualize
charts = create_spending_charts(df)
```

## Configuration

### Setting Tesseract Path

If Tesseract is not in your PATH, you can specify it in the app:

1. Launch the Streamlit app
2. Go to "Advanced Settings" in the sidebar
3. Enter the path to tesseract.exe (Windows) or tesseract binary (Mac/Linux)

Example paths:
- Windows: `C:\Program Files\Tesseract-OCR\tesseract.exe`
- macOS: `/usr/local/bin/tesseract`
- Linux: `/usr/bin/tesseract`

## Testing the Installation

### Test with Sample Data

```bash
cd "c:\Where is my money going"
streamlit run app.py
```

In the sidebar:
1. Select "Use Sample Data"
2. Click "Load Sample Data"
3. Click "Categorize Transactions"

### Test with Sample CSV

Use the provided `sample_data/sample_transactions.csv` file:

1. Select "Upload CSV" in the sidebar
2. Upload `sample_data/sample_transactions.csv`
3. Click "Categorize Transactions"

## Troubleshooting

### Issue: "Tesseract not found"

**Solution**: 
- Ensure Tesseract is installed
- Add Tesseract to your PATH
- Or specify the path in Advanced Settings

### Issue: "pdf2image: Unable to get page count"

**Solution**: 
- Install Poppler utilities
- Add Poppler bin folder to PATH (Windows)

### Issue: Import errors

**Solution**: 
```bash
pip install --upgrade -r requirements.txt
```

### Issue: Permission denied on Windows

**Solution**: 
Run PowerShell as Administrator:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Quick Start Guide

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Install Tesseract OCR** (see instructions above)

3. **Run the app**:
   ```bash
   streamlit run app.py
   ```

4. **Upload your data** via the sidebar

5. **Categorize transactions** and explore insights!

## Additional Resources

- [Tesseract Documentation](https://tesseract-ocr.github.io/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Plotly Documentation](https://plotly.com/python/)

## Support

For issues or questions, refer to:
- README.md for usage instructions
- Module docstrings for API documentation
- Sample data in `sample_data/` folder

## Next Steps

After installation:
1. Try the sample data to familiarize yourself with the interface
2. Upload your own bank statement (CSV recommended for first try)
3. Explore the different analysis tabs
4. Export your categorized transactions

Enjoy tracking your expenses! 💰📊
