"""
Tests for expense tracker functionality
"""

import unittest
from datetime import datetime
from expense_tracker.models import Transaction, ExpenseCategory
from expense_tracker.categorizer import ExpenseCategorizer
from expense_tracker.anomaly_detector import AnomalyDetector


class TestTransaction(unittest.TestCase):
    """Test Transaction model"""
    
    def test_transaction_creation(self):
        """Test creating a transaction"""
        trans = Transaction(
            date=datetime(2024, 1, 15),
            description="Test Store",
            amount=50.00
        )
        self.assertEqual(trans.description, "Test Store")
        self.assertEqual(trans.amount, 50.00)
        self.assertEqual(trans.category, "Uncategorized")
    
    def test_transaction_to_dict(self):
        """Test transaction serialization"""
        trans = Transaction(
            date=datetime(2024, 1, 15),
            description="Test Store",
            amount=50.00,
            category="Shopping"
        )
        data = trans.to_dict()
        self.assertIn('date', data)
        self.assertIn('description', data)
        self.assertIn('amount', data)
        self.assertIn('category', data)


class TestExpenseCategory(unittest.TestCase):
    """Test ExpenseCategory model"""
    
    def test_category_creation(self):
        """Test creating a category"""
        cat = ExpenseCategory(name="Test", keywords=["test", "sample"])
        self.assertEqual(cat.name, "Test")
        self.assertEqual(len(cat.keywords), 2)
    
    def test_add_transaction(self):
        """Test adding transactions to category"""
        cat = ExpenseCategory(name="Test")
        cat.add_transaction(50.00)
        cat.add_transaction(75.00)
        
        self.assertEqual(cat.transaction_count, 2)
        self.assertEqual(cat.total_amount, 125.00)
        self.assertEqual(cat.average_amount(), 62.50)


class TestExpenseCategorizer(unittest.TestCase):
    """Test ExpenseCategorizer"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.categorizer = ExpenseCategorizer()
        self.transactions = [
            Transaction(datetime(2024, 1, 1), "Walmart Supercenter", 100.00),
            Transaction(datetime(2024, 1, 2), "Starbucks Coffee", 5.50),
            Transaction(datetime(2024, 1, 3), "Shell Gas Station", 45.00),
            Transaction(datetime(2024, 1, 4), "Netflix Subscription", 15.99),
            Transaction(datetime(2024, 1, 5), "Amazon Purchase", 75.00),
        ]
    
    def test_categorize_groceries(self):
        """Test categorizing grocery transactions"""
        trans = self.transactions[0]
        category = self.categorizer.categorize_transaction(trans)
        self.assertEqual(category, "Groceries")
    
    def test_categorize_restaurants(self):
        """Test categorizing restaurant transactions"""
        trans = self.transactions[1]
        category = self.categorizer.categorize_transaction(trans)
        self.assertEqual(category, "Restaurants")
    
    def test_categorize_transportation(self):
        """Test categorizing transportation transactions"""
        trans = self.transactions[2]
        category = self.categorizer.categorize_transaction(trans)
        self.assertEqual(category, "Transportation")
    
    def test_categorize_entertainment(self):
        """Test categorizing entertainment transactions"""
        trans = self.transactions[3]
        category = self.categorizer.categorize_transaction(trans)
        self.assertEqual(category, "Entertainment")
    
    def test_categorize_shopping(self):
        """Test categorizing shopping transactions"""
        trans = self.transactions[4]
        category = self.categorizer.categorize_transaction(trans)
        self.assertEqual(category, "Shopping")
    
    def test_categorize_all_transactions(self):
        """Test categorizing multiple transactions"""
        categorized = self.categorizer.categorize_transactions(self.transactions)
        
        # All transactions should be categorized
        for trans in categorized:
            self.assertNotEqual(trans.category, "Uncategorized")
    
    def test_category_summary(self):
        """Test getting category summary"""
        self.categorizer.categorize_transactions(self.transactions)
        summary = self.categorizer.get_category_summary()
        
        self.assertIsInstance(summary, dict)
        self.assertGreater(len(summary), 0)


class TestAnomalyDetector(unittest.TestCase):
    """Test AnomalyDetector"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.detector = AnomalyDetector(contamination=0.1)
        
        # Create normal transactions
        self.normal_transactions = []
        for i in range(50):
            trans = Transaction(
                date=datetime(2024, 1, i % 28 + 1),
                description=f"Store {i}",
                amount=50.00 + (i % 20),  # Amounts between 50-70
                category="Shopping"
            )
            self.normal_transactions.append(trans)
        
        # Add anomalous transactions
        self.anomaly_transactions = [
            Transaction(datetime(2024, 1, 15), "Large Purchase", 1000.00, category="Shopping"),
            Transaction(datetime(2024, 1, 16), "Unusual Amount", 5.00, category="Shopping"),
            Transaction(datetime(2024, 1, 17), "Very High", 2000.00, category="Shopping"),
        ]
        
        self.all_transactions = self.normal_transactions + self.anomaly_transactions
    
    def test_calculate_baseline_stats(self):
        """Test calculating baseline statistics"""
        self.detector.calculate_baseline_stats(self.normal_transactions)
        
        self.assertIn("Shopping", self.detector.baseline_stats)
        stats = self.detector.baseline_stats["Shopping"]
        
        self.assertIn('mean', stats)
        self.assertIn('std', stats)
        self.assertIn('median', stats)
    
    def test_detect_statistical_anomalies(self):
        """Test statistical anomaly detection"""
        anomalies = self.detector.detect_statistical_anomalies(self.all_transactions)
        
        # Should detect some anomalies
        self.assertGreater(len(anomalies), 0)
        
        # Large amounts should be flagged
        large_amounts = [a for a in anomalies if a.amount > 500]
        self.assertGreater(len(large_amounts), 0)
    
    def test_anomaly_summary(self):
        """Test getting anomaly summary"""
        self.detector.detect_all_anomalies(self.all_transactions)
        summary = self.detector.get_anomaly_summary(self.all_transactions)
        
        self.assertIn('total_transactions', summary)
        self.assertIn('anomaly_count', summary)
        self.assertIn('anomaly_percentage', summary)
        self.assertIn('anomalies', summary)


def run_tests():
    """Run all tests"""
    unittest.main(argv=[''], exit=False, verbosity=2)


if __name__ == '__main__':
    run_tests()
