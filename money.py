"""
💰 Where Is My Money Going?
Main Entry Point

This module provides a command-line interface for the expense tracking application.
For the web dashboard, use: streamlit run app.py
"""

import sys
import argparse
from pathlib import Path

# Import modules
from ocr_extractor import OCRExtractor
from transaction_parser import TransactionParser
from categorizer import TransactionCategorizer
from analyzer import SpendingAnalyzer
from visualizer import SpendingVisualizer


def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(
        description='💰 Where Is My Money Going? - Expense Tracking and Analysis',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze a bank statement PDF
  python money.py --pdf statement.pdf
  
  # Analyze a CSV file
  python money.py --csv transactions.csv
  
  # Launch web dashboard
  python money.py --dashboard
  
  # Process image and save results
  python money.py --image statement.jpg --output results.csv
        """
    )
    
    # Input options
    input_group = parser.add_mutually_exclusive_group(required=False)
    input_group.add_argument('--pdf', type=str, help='Path to PDF bank statement')
    input_group.add_argument('--image', type=str, help='Path to image of bank statement')
    input_group.add_argument('--csv', type=str, help='Path to CSV file with transactions')
    input_group.add_argument('--dashboard', action='store_true', help='Launch Streamlit dashboard')
    
    # Options
    parser.add_argument('--output', type=str, help='Output file path (CSV or Excel)')
    parser.add_argument('--tesseract', type=str, help='Path to Tesseract executable')
    parser.add_argument('--visualize', action='store_true', help='Generate and save visualizations')
    parser.add_argument('--report', action='store_true', help='Generate text report')
    
    args = parser.parse_args()
    
    # If no arguments, show help and launch dashboard
    if len(sys.argv) == 1:
        parser.print_help()
        print("\n" + "="*60)
        print("Launching Streamlit dashboard...")
        print("="*60 + "\n")
        import subprocess
        subprocess.run(['streamlit', 'run', 'app.py'])
        return
    
    # Launch dashboard
    if args.dashboard:
        print("🚀 Launching Streamlit dashboard...")
        import subprocess
        subprocess.run(['streamlit', 'run', 'app.py'])
        return
    
    # Process input file
    df = None
    
    if args.pdf:
        print(f"📄 Processing PDF: {args.pdf}")
        ocr = OCRExtractor(args.tesseract)
        text = ocr.extract_from_pdf(args.pdf)
        
        parser_obj = TransactionParser()
        df = parser_obj.parse_transactions(text)
        print(f"✅ Extracted {len(df)} transactions")
    
    elif args.image:
        print(f"🖼️ Processing image: {args.image}")
        ocr = OCRExtractor(args.tesseract)
        text = ocr.extract_from_image(args.image)
        
        parser_obj = TransactionParser()
        df = parser_obj.parse_transactions(text)
        print(f"✅ Extracted {len(df)} transactions")
    
    elif args.csv:
        print(f"📊 Loading CSV: {args.csv}")
        parser_obj = TransactionParser()
        df = parser_obj.parse_csv_statement(args.csv)
        print(f"✅ Loaded {len(df)} transactions")
    
    else:
        parser.print_help()
        return
    
    if df is None or len(df) == 0:
        print("❌ No transactions found")
        return
    
    # Categorize transactions
    print("\n🏷️ Categorizing transactions...")
    categorizer = TransactionCategorizer()
    df = categorizer.categorize_transactions(df)
    
    # Analyze
    print("\n📊 Analyzing spending patterns...")
    analyzer = SpendingAnalyzer(df)
    insights = analyzer.get_insights()
    
    # Print summary
    print("\n" + "="*60)
    print("💰 SPENDING SUMMARY")
    print("="*60)
    print(f"Total Transactions: {insights['basic_stats']['total_transactions']:,}")
    print(f"Total Spent: ${insights['basic_stats']['total_spent']:,.2f}")
    print(f"Average Transaction: ${insights['basic_stats']['average_transaction']:,.2f}")
    print(f"Median Transaction: ${insights['basic_stats']['median_transaction']:,.2f}")
    print(f"Largest Transaction: ${insights['basic_stats']['largest_transaction']:,.2f}")
    print(f"Smallest Transaction: ${insights['basic_stats']['smallest_transaction']:,.2f}")
    
    if 'top_category' in insights:
        print(f"\nTop Category: {insights['top_category']} (${insights['top_category_amount']:,.2f})")
    
    if 'top_merchant' in insights:
        print(f"Top Merchant: {insights['top_merchant']} (${insights['top_merchant_amount']:,.2f})")
    
    print(f"\n⚠️ Anomalies Detected: {insights['anomaly_count']}")
    print(f"🔄 Potential Duplicates: {insights['potential_duplicates']}")
    print("="*60 + "\n")
    
    # Category breakdown
    if 'category' in df.columns:
        print("📋 CATEGORY BREAKDOWN")
        print("="*60)
        summary = categorizer.get_category_summary(df)
        print(summary.to_string())
        print()
    
    # Save output
    if args.output:
        output_path = Path(args.output)
        
        if output_path.suffix == '.csv':
            df.to_csv(output_path, index=False)
            print(f"💾 Saved to: {output_path}")
        elif output_path.suffix in ['.xlsx', '.xls']:
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Transactions', index=False)
                if 'category' in df.columns:
                    summary.to_excel(writer, sheet_name='Category Summary')
            print(f"💾 Saved to: {output_path}")
        else:
            print(f"⚠️ Unsupported output format: {output_path.suffix}")
    
    # Generate visualizations
    if args.visualize:
        print("\n📈 Generating visualizations...")
        visualizer = SpendingVisualizer(df)
        
        output_dir = Path('visualizations')
        output_dir.mkdir(exist_ok=True)
        
        # Create dashboard
        fig = visualizer.create_dashboard()
        dashboard_path = output_dir / 'dashboard.png'
        fig.savefig(dashboard_path, dpi=300, bbox_inches='tight')
        print(f"💾 Dashboard saved to: {dashboard_path}")
    
    # Generate report
    if args.report:
        report_path = Path('spending_report.txt')
        
        report = f"""
{'='*60}
💰 SPENDING REPORT
{'='*60}

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
        
        if 'category' in df.columns:
            report += "\n\nCATEGORY BREAKDOWN\n------------------\n"
            report += summary.to_string()
        
        with open(report_path, 'w') as f:
            f.write(report)
        
        print(f"\n📄 Report saved to: {report_path}")
    
    print("\n✅ Done!\n")


if __name__ == "__main__":
    main()
