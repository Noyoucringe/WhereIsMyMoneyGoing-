"""
Command-line interface for the expense tracker
"""

import argparse
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import List

from .ocr import BankStatementOCR
from .models import Transaction
from .categorizer import ExpenseCategorizer
from .anomaly_detector import AnomalyDetector
from .visualizer import ExpenseVisualizer


class ExpenseTrackerCLI:
    """Command-line interface for expense tracking"""
    
    def __init__(self):
        self.ocr = BankStatementOCR()
        self.categorizer = ExpenseCategorizer()
        self.anomaly_detector = AnomalyDetector()
        self.visualizer = ExpenseVisualizer()
        self.transactions = []
    
    def process_statement(self, file_path: str):
        """Process a bank statement file"""
        print(f"Processing statement: {file_path}")
        
        try:
            raw_transactions = self.ocr.process_statement(file_path)
            
            if not raw_transactions:
                print("No transactions found in the statement.")
                return
            
            # Convert to Transaction objects
            for raw_trans in raw_transactions:
                if raw_trans['date']:
                    transaction = Transaction(
                        date=raw_trans['date'],
                        description=raw_trans['description'],
                        amount=raw_trans['amount']
                    )
                    self.transactions.append(transaction)
            
            print(f"Extracted {len(raw_transactions)} transactions")
            
        except Exception as e:
            print(f"Error processing statement: {e}")
            import traceback
            traceback.print_exc()
    
    def categorize(self):
        """Categorize all transactions"""
        if not self.transactions:
            print("No transactions to categorize. Process a statement first.")
            return
        
        print("\nCategorizing transactions...")
        self.categorizer.categorize_transactions(self.transactions)
        
        summary = self.categorizer.get_category_summary()
        print("\nCategory Summary:")
        print("-" * 60)
        for category, stats in sorted(summary.items(), key=lambda x: x[1]['total_amount'], reverse=True):
            print(f"{category:20s}: ${stats['total_amount']:10.2f} ({stats['transaction_count']} transactions)")
    
    def detect_anomalies(self):
        """Detect anomalies in transactions"""
        if not self.transactions:
            print("No transactions to analyze. Process a statement first.")
            return
        
        print("\nDetecting anomalies...")
        results = self.anomaly_detector.detect_all_anomalies(self.transactions)
        
        summary = self.anomaly_detector.get_anomaly_summary(self.transactions)
        
        print(f"\nAnomaly Detection Results:")
        print("-" * 60)
        print(f"Total Transactions: {summary['total_transactions']}")
        print(f"Anomalies Found: {summary['anomaly_count']} ({summary['anomaly_percentage']}%)")
        print(f"Total Anomaly Amount: ${summary['total_anomaly_amount']:.2f}")
        
        if summary['anomalies']:
            print("\nTop Anomalies:")
            for i, anomaly in enumerate(summary['anomalies'][:5], 1):
                print(f"{i}. {anomaly['date']} - {anomaly['description']}: ${abs(anomaly['amount']):.2f}")
    
    def visualize(self, output_dir: str = "output"):
        """Create visualizations"""
        if not self.transactions:
            print("No transactions to visualize. Process a statement first.")
            return
        
        Path(output_dir).mkdir(exist_ok=True)
        
        print(f"\nCreating visualizations in {output_dir}/...")
        
        try:
            # Create individual plots
            self.visualizer.plot_category_pie_chart(
                self.transactions,
                f"{output_dir}/category_pie.html"
            )
            print(f"✓ Created category pie chart")
            
            self.visualizer.plot_spending_timeline(
                self.transactions,
                f"{output_dir}/timeline.html"
            )
            print(f"✓ Created spending timeline")
            
            self.visualizer.plot_category_bars(
                self.transactions,
                f"{output_dir}/category_bars.html"
            )
            print(f"✓ Created category bar charts")
            
            self.visualizer.plot_monthly_trends(
                self.transactions,
                f"{output_dir}/monthly_trends.html"
            )
            print(f"✓ Created monthly trends")
            
            self.visualizer.plot_heatmap(
                self.transactions,
                f"{output_dir}/heatmap.html"
            )
            print(f"✓ Created spending heatmap")
            
            # Create dashboard
            self.visualizer.create_dashboard(
                self.transactions,
                f"{output_dir}/dashboard.html"
            )
            print(f"✓ Created comprehensive dashboard")
            
            print(f"\n✓ All visualizations saved to {output_dir}/")
            
        except Exception as e:
            print(f"Error creating visualizations: {e}")
            import traceback
            traceback.print_exc()
    
    def save_transactions(self, file_path: str):
        """Save transactions to JSON file"""
        if not self.transactions:
            print("No transactions to save.")
            return
        
        data = [t.to_dict() for t in self.transactions]
        
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Saved {len(self.transactions)} transactions to {file_path}")
    
    def load_transactions(self, file_path: str):
        """Load transactions from JSON file"""
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        self.transactions = [Transaction.from_dict(t) for t in data]
        print(f"Loaded {len(self.transactions)} transactions from {file_path}")
    
    def list_transactions(self, limit: int = 10):
        """List recent transactions"""
        if not self.transactions:
            print("No transactions to display.")
            return
        
        print(f"\nShowing {min(limit, len(self.transactions))} most recent transactions:")
        print("-" * 80)
        print(f"{'Date':<12} {'Description':<30} {'Amount':>10} {'Category':<15} {'Anomaly':<8}")
        print("-" * 80)
        
        sorted_trans = sorted(self.transactions, key=lambda x: x.date, reverse=True)
        
        for trans in sorted_trans[:limit]:
            anomaly_flag = "⚠️ " if trans.is_anomaly else ""
            print(f"{trans.date.strftime('%Y-%m-%d'):<12} "
                  f"{trans.description[:28]:<30} "
                  f"${trans.amount:>9.2f} "
                  f"{trans.category:<15} "
                  f"{anomaly_flag:<8}")
    
    def run(self, args):
        """Run the CLI with parsed arguments"""
        if args.command == 'process':
            self.process_statement(args.file)
            
            # Auto-categorize after processing
            if self.transactions:
                self.categorize()
            
            # Save if output specified
            if args.output:
                self.save_transactions(args.output)
        
        elif args.command == 'analyze':
            if args.load:
                self.load_transactions(args.load)
            
            self.categorize()
            self.detect_anomalies()
            
            if args.visualize:
                self.visualize(args.output_dir)
        
        elif args.command == 'visualize':
            if args.load:
                self.load_transactions(args.load)
            
            if not self.transactions:
                print("Error: No transactions loaded. Use --load to specify a transaction file.")
                return
            
            self.visualize(args.output_dir)
        
        elif args.command == 'list':
            if args.load:
                self.load_transactions(args.load)
            
            self.list_transactions(args.limit)


def main():
    """Main entry point for the CLI"""
    parser = argparse.ArgumentParser(
        description='Expense Tracker - Analyze bank statements with OCR, categorization, and anomaly detection'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Process command
    process_parser = subparsers.add_parser('process', help='Process a bank statement file')
    process_parser.add_argument('file', help='Path to bank statement (image or PDF)')
    process_parser.add_argument('-o', '--output', help='Save transactions to JSON file')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze transactions')
    analyze_parser.add_argument('-l', '--load', help='Load transactions from JSON file')
    analyze_parser.add_argument('-v', '--visualize', action='store_true', help='Create visualizations')
    analyze_parser.add_argument('-d', '--output-dir', default='output', help='Output directory for visualizations')
    
    # Visualize command
    visualize_parser = subparsers.add_parser('visualize', help='Create visualizations')
    visualize_parser.add_argument('-l', '--load', required=True, help='Load transactions from JSON file')
    visualize_parser.add_argument('-d', '--output-dir', default='output', help='Output directory for visualizations')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List transactions')
    list_parser.add_argument('-l', '--load', required=True, help='Load transactions from JSON file')
    list_parser.add_argument('-n', '--limit', type=int, default=10, help='Number of transactions to show')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    cli = ExpenseTrackerCLI()
    cli.run(args)


if __name__ == '__main__':
    main()
