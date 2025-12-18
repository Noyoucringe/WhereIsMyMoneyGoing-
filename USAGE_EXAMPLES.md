# Usage Examples

This document provides detailed examples of how to use the Expense Tracker application.

## Example 1: Processing a Bank Statement

```bash
# Process a PDF bank statement
expense-tracker process bank_statement.pdf --output transactions.json

# Process an image (JPG, PNG)
expense-tracker process statement_screenshot.png --output transactions.json
```

## Example 2: Analyzing Transactions

```bash
# Load and analyze transactions
expense-tracker analyze --load transactions.json

# Analyze and create visualizations
expense-tracker analyze --load transactions.json --visualize --output-dir my_charts
```

## Example 3: Creating Visualizations

```bash
# Create all visualizations
expense-tracker visualize --load transactions.json --output-dir charts

# Open the dashboard in your browser
open charts/dashboard.html
```

## Example 4: Listing Transactions

```bash
# Show last 10 transactions (default)
expense-tracker list --load transactions.json

# Show last 50 transactions
expense-tracker list --load transactions.json --limit 50
```

## Example 5: Python API Usage

### Basic Usage

```python
from expense_tracker.models import Transaction
from expense_tracker.categorizer import ExpenseCategorizer
from expense_tracker.anomaly_detector import AnomalyDetector
from expense_tracker.visualizer import ExpenseVisualizer
from datetime import datetime

# Create sample transactions
transactions = [
    Transaction(datetime(2024, 1, 1), "Walmart Supercenter", 125.50),
    Transaction(datetime(2024, 1, 2), "Shell Gas Station", 45.00),
    Transaction(datetime(2024, 1, 3), "Starbucks Coffee", 5.50),
    Transaction(datetime(2024, 1, 4), "Amazon Purchase", 89.99),
]

# Categorize transactions
categorizer = ExpenseCategorizer()
categorized = categorizer.categorize_transactions(transactions)

# Print categorized transactions
for trans in categorized:
    print(f"{trans.date}: {trans.description} - ${trans.amount} [{trans.category}]")

# Get category summary
summary = categorizer.get_category_summary()
print("\nCategory Summary:")
for category, stats in summary.items():
    print(f"{category}: ${stats['total_amount']:.2f} ({stats['transaction_count']} transactions)")
```

### OCR Processing

```python
from expense_tracker.ocr import BankStatementOCR

# Initialize OCR processor
ocr = BankStatementOCR()

# Process a PDF statement
transactions = ocr.process_statement('bank_statement.pdf')

# Process an image
transactions = ocr.process_statement('statement_screenshot.png')

# View extracted transactions
for trans in transactions:
    print(f"{trans['date']}: {trans['description']} - ${trans['amount']}")
```

### Anomaly Detection

```python
from expense_tracker.anomaly_detector import AnomalyDetector

# Initialize detector
detector = AnomalyDetector(contamination=0.1)

# Detect anomalies
results = detector.detect_all_anomalies(transactions)

# Get anomaly summary
summary = detector.get_anomaly_summary(transactions)
print(f"Found {summary['anomaly_count']} anomalies out of {summary['total_transactions']} transactions")

# List anomalies
for trans in transactions:
    if trans.is_anomaly:
        print(f"⚠️  {trans.date}: {trans.description} - ${trans.amount}")
```

### Custom Categories

```python
from expense_tracker.categorizer import ExpenseCategorizer

categorizer = ExpenseCategorizer()

# Add custom category
categorizer.add_custom_category(
    name='Pet Care',
    keywords=['petco', 'petsmart', 'vet', 'veterinary', 'pet store']
)

# Categorize with custom categories
categorized = categorizer.categorize_transactions(transactions)
```

### Creating Visualizations

```python
from expense_tracker.visualizer import ExpenseVisualizer

visualizer = ExpenseVisualizer()

# Create individual visualizations
visualizer.plot_category_pie_chart(transactions, 'category_pie.html')
visualizer.plot_spending_timeline(transactions, 'timeline.html')
visualizer.plot_monthly_trends(transactions, 'monthly_trends.html')
visualizer.plot_heatmap(transactions, 'heatmap.html')

# Create comprehensive dashboard
visualizer.create_dashboard(transactions, 'dashboard.html')
```

## Example 6: Working with Transaction Data

### Saving and Loading Transactions

```python
import json
from expense_tracker.models import Transaction

# Save transactions to JSON
transactions_data = [t.to_dict() for t in transactions]
with open('my_transactions.json', 'w') as f:
    json.dump(transactions_data, f, indent=2)

# Load transactions from JSON
with open('my_transactions.json', 'r') as f:
    data = json.load(f)
transactions = [Transaction.from_dict(t) for t in data]
```

### Filtering Transactions

```python
from datetime import datetime, timedelta

# Filter by date range
start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 1, 31)
january_trans = [t for t in transactions if start_date <= t.date <= end_date]

# Filter by category
grocery_trans = [t for t in transactions if t.category == 'Groceries']

# Filter anomalies
anomalies = [t for t in transactions if t.is_anomaly]

# Filter by amount
large_purchases = [t for t in transactions if t.amount > 100]
```

### Calculating Statistics

```python
import pandas as pd

# Convert to DataFrame for advanced analysis
df = pd.DataFrame([t.to_dict() for t in transactions])
df['date'] = pd.to_datetime(df['date'])

# Calculate monthly totals
monthly_totals = df.groupby(df['date'].dt.to_period('M'))['amount'].sum()

# Calculate average by category
category_avg = df.groupby('category')['amount'].mean()

# Find top merchants
top_merchants = df.groupby('description')['amount'].sum().nlargest(10)
```

## Example 7: Running the Demo

```bash
# Run the comprehensive demo
python demo.py

# This will:
# 1. Generate 100+ sample transactions
# 2. Automatically categorize them
# 3. Detect anomalies
# 4. Create interactive visualizations
# 5. Save everything to the output/ directory
```

## Example 8: Integration Example

Here's a complete workflow example:

```python
from expense_tracker.ocr import BankStatementOCR
from expense_tracker.categorizer import ExpenseCategorizer
from expense_tracker.anomaly_detector import AnomalyDetector
from expense_tracker.visualizer import ExpenseVisualizer
from expense_tracker.models import Transaction
import json

# Step 1: Process bank statement
print("Processing bank statement...")
ocr = BankStatementOCR()
raw_transactions = ocr.process_statement('statement.pdf')

# Convert to Transaction objects
transactions = []
for raw in raw_transactions:
    if raw['date']:
        trans = Transaction(
            date=raw['date'],
            description=raw['description'],
            amount=raw['amount']
        )
        transactions.append(trans)

print(f"Extracted {len(transactions)} transactions")

# Step 2: Categorize
print("\nCategorizing transactions...")
categorizer = ExpenseCategorizer()
categorizer.categorize_transactions(transactions)

summary = categorizer.get_category_summary()
print("Category Summary:")
for category, stats in summary.items():
    print(f"  {category}: ${stats['total_amount']:.2f}")

# Step 3: Detect anomalies
print("\nDetecting anomalies...")
detector = AnomalyDetector()
detector.detect_all_anomalies(transactions)

anomaly_summary = detector.get_anomaly_summary(transactions)
print(f"Found {anomaly_summary['anomaly_count']} anomalies")

# Step 4: Create visualizations
print("\nCreating visualizations...")
visualizer = ExpenseVisualizer()
visualizer.create_dashboard(transactions, 'dashboard.html')
print("Dashboard created!")

# Step 5: Save results
print("\nSaving results...")
data = [t.to_dict() for t in transactions]
with open('analyzed_transactions.json', 'w') as f:
    json.dump(data, f, indent=2)
print("Done!")
```

## Tips and Best Practices

1. **OCR Quality**: For best OCR results, ensure bank statements are:
   - High resolution (300 DPI or higher)
   - Clear and not blurry
   - Well-lit if scanned from paper
   - In a standard format

2. **Custom Categories**: Add custom categories for your specific needs:
   ```python
   categorizer.add_custom_category('Crypto', ['coinbase', 'binance', 'crypto'])
   ```

3. **Anomaly Sensitivity**: Adjust the contamination parameter:
   ```python
   # More sensitive (finds more anomalies)
   detector = AnomalyDetector(contamination=0.15)
   
   # Less sensitive (finds fewer anomalies)
   detector = AnomalyDetector(contamination=0.05)
   ```

4. **Visualization Formats**: All visualizations are saved as interactive HTML files that can be opened in any web browser.

5. **Data Privacy**: Keep your transaction data secure:
   - Don't commit transaction files to version control
   - Store them in secure locations
   - Use encryption for sensitive data
