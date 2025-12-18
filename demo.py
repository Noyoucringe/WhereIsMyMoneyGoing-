"""
Demo script to showcase expense tracker functionality
"""

from datetime import datetime, timedelta
import random
from expense_tracker.models import Transaction
from expense_tracker.categorizer import ExpenseCategorizer
from expense_tracker.anomaly_detector import AnomalyDetector
from expense_tracker.visualizer import ExpenseVisualizer


def generate_sample_transactions(num_transactions=100):
    """Generate sample transactions for demonstration"""
    
    merchants = {
        'Groceries': ['Walmart Supercenter', 'Whole Foods Market', 'Trader Joes', 'Safeway', 'Kroger'],
        'Restaurants': ['Starbucks Coffee', 'McDonalds', 'Chipotle', 'Pizza Hut', 'Local Restaurant'],
        'Transportation': ['Shell Gas Station', 'Uber Trip', 'Metro Transit', 'Parking Garage', 'Chevron'],
        'Utilities': ['Electric Company', 'Internet Service', 'Water Utility', 'Gas Company', 'Phone Bill'],
        'Entertainment': ['Netflix Subscription', 'Movie Theater', 'Spotify Premium', 'Concert Tickets', 'Gaming Store'],
        'Shopping': ['Amazon Purchase', 'Target Store', 'Best Buy', 'Fashion Boutique', 'Online Store'],
        'Healthcare': ['CVS Pharmacy', 'Doctor Visit', 'Dental Clinic', 'Walgreens', 'Medical Center'],
        'Fitness': ['Gym Membership', 'Yoga Studio', 'Sports Equipment', 'Athletic Store', 'Fitness Class']
    }
    
    # Amount ranges for each category
    amount_ranges = {
        'Groceries': (30, 150),
        'Restaurants': (10, 60),
        'Transportation': (20, 80),
        'Utilities': (50, 200),
        'Entertainment': (10, 100),
        'Shopping': (20, 300),
        'Healthcare': (25, 150),
        'Fitness': (30, 100)
    }
    
    transactions = []
    start_date = datetime.now() - timedelta(days=90)
    
    for i in range(num_transactions):
        # Pick random category
        category = random.choice(list(merchants.keys()))
        merchant = random.choice(merchants[category])
        
        # Generate random amount within category range
        min_amt, max_amt = amount_ranges[category]
        amount = round(random.uniform(min_amt, max_amt), 2)
        
        # Generate random date within last 90 days
        days_ago = random.randint(0, 90)
        date = start_date + timedelta(days=days_ago)
        
        transaction = Transaction(
            date=date,
            description=merchant,
            amount=amount,
            category='Uncategorized'
        )
        
        transactions.append(transaction)
    
    # Add some anomalies
    # 1. Unusually large purchase
    anomaly1 = Transaction(
        date=datetime.now() - timedelta(days=5),
        description='Luxury Electronics Store',
        amount=2500.00,
        category='Uncategorized'
    )
    transactions.append(anomaly1)
    
    # 2. Multiple identical transactions on same day (fraud pattern)
    fraud_date = datetime.now() - timedelta(days=10)
    for _ in range(3):
        fraud_trans = Transaction(
            date=fraud_date,
            description='Unknown Online Merchant',
            amount=99.99,
            category='Uncategorized'
        )
        transactions.append(fraud_trans)
    
    # 3. Unusually high utility bill
    anomaly2 = Transaction(
        date=datetime.now() - timedelta(days=15),
        description='Electric Company',
        amount=850.00,
        category='Uncategorized'
    )
    transactions.append(anomaly2)
    
    return sorted(transactions, key=lambda x: x.date)


def main():
    """Run the demo"""
    print("=" * 80)
    print("EXPENSE TRACKER DEMO")
    print("=" * 80)
    
    # Generate sample data
    print("\n1. Generating sample transactions...")
    transactions = generate_sample_transactions(100)
    print(f"   ✓ Generated {len(transactions)} sample transactions")
    
    # Categorize transactions
    print("\n2. Categorizing transactions...")
    categorizer = ExpenseCategorizer()
    categorizer.categorize_transactions(transactions)
    
    summary = categorizer.get_category_summary()
    print("\n   Category Summary:")
    print("   " + "-" * 76)
    for category, stats in sorted(summary.items(), key=lambda x: x[1]['total_amount'], reverse=True):
        print(f"   {category:20s}: ${stats['total_amount']:10.2f} "
              f"({stats['transaction_count']} transactions, avg: ${stats['average_amount']:.2f})")
    
    # Detect anomalies
    print("\n3. Detecting anomalies...")
    detector = AnomalyDetector(contamination=0.05)
    results = detector.detect_all_anomalies(transactions)
    
    anomaly_summary = detector.get_anomaly_summary(transactions)
    print(f"\n   Anomaly Detection Results:")
    print("   " + "-" * 76)
    print(f"   Total Transactions: {anomaly_summary['total_transactions']}")
    print(f"   Anomalies Found: {anomaly_summary['anomaly_count']} ({anomaly_summary['anomaly_percentage']}%)")
    print(f"   Total Anomaly Amount: ${anomaly_summary['total_anomaly_amount']:.2f}")
    
    if anomaly_summary['anomalies']:
        print("\n   Top Anomalies Detected:")
        for i, anomaly in enumerate(anomaly_summary['anomalies'][:5], 1):
            print(f"   {i}. {anomaly['date']} - {anomaly['description']}: ${abs(anomaly['amount']):.2f} [{anomaly['category']}]")
    
    # Create visualizations
    print("\n4. Creating visualizations...")
    visualizer = ExpenseVisualizer()
    
    try:
        import os
        os.makedirs('output', exist_ok=True)
        
        visualizer.create_dashboard(transactions, 'output/dashboard.html')
        print("   ✓ Created interactive dashboard: output/dashboard.html")
        
        visualizer.plot_category_pie_chart(transactions, 'output/category_pie.html')
        print("   ✓ Created category pie chart: output/category_pie.html")
        
        visualizer.plot_spending_timeline(transactions, 'output/timeline.html')
        print("   ✓ Created spending timeline: output/timeline.html")
        
        visualizer.plot_monthly_trends(transactions, 'output/monthly_trends.html')
        print("   ✓ Created monthly trends: output/monthly_trends.html")
        
        visualizer.plot_heatmap(transactions, 'output/heatmap.html')
        print("   ✓ Created spending heatmap: output/heatmap.html")
        
    except Exception as e:
        print(f"   ⚠️  Error creating visualizations: {e}")
    
    # Summary
    print("\n" + "=" * 80)
    print("DEMO COMPLETE")
    print("=" * 80)
    print("\nKey Features Demonstrated:")
    print("  ✓ Automatic expense categorization")
    print("  ✓ Multi-method anomaly detection (statistical, ML, frequency-based)")
    print("  ✓ Interactive visualizations with Plotly")
    print("  ✓ Comprehensive spending analysis")
    print("\nCheck the 'output' directory for interactive HTML visualizations!")
    print("=" * 80)


if __name__ == '__main__':
    main()
