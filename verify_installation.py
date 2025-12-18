#!/usr/bin/env python
"""
Verification script to test if the expense tracker is properly installed and working
"""

import sys


def check_imports():
    """Check if all required modules can be imported"""
    print("Checking imports...")
    
    try:
        import pytesseract
        print("  ✓ pytesseract")
    except ImportError as e:
        print(f"  ✗ pytesseract: {e}")
        return False
    
    try:
        from PIL import Image
        print("  ✓ Pillow")
    except ImportError as e:
        print(f"  ✗ Pillow: {e}")
        return False
    
    try:
        import pandas
        print("  ✓ pandas")
    except ImportError as e:
        print(f"  ✗ pandas: {e}")
        return False
    
    try:
        import numpy
        print("  ✓ numpy")
    except ImportError as e:
        print(f"  ✗ numpy: {e}")
        return False
    
    try:
        from sklearn.ensemble import IsolationForest
        print("  ✓ scikit-learn")
    except ImportError as e:
        print(f"  ✗ scikit-learn: {e}")
        return False
    
    try:
        import matplotlib
        print("  ✓ matplotlib")
    except ImportError as e:
        print(f"  ✗ matplotlib: {e}")
        return False
    
    try:
        import plotly
        print("  ✓ plotly")
    except ImportError as e:
        print(f"  ✗ plotly: {e}")
        return False
    
    try:
        import cv2
        print("  ✓ opencv-python")
    except ImportError as e:
        print(f"  ✗ opencv-python: {e}")
        return False
    
    return True


def check_modules():
    """Check if expense tracker modules work"""
    print("\nChecking expense tracker modules...")
    
    try:
        from expense_tracker.models import Transaction, ExpenseCategory
        print("  ✓ models")
    except ImportError as e:
        print(f"  ✗ models: {e}")
        return False
    
    try:
        from expense_tracker.categorizer import ExpenseCategorizer
        print("  ✓ categorizer")
    except ImportError as e:
        print(f"  ✗ categorizer: {e}")
        return False
    
    try:
        from expense_tracker.anomaly_detector import AnomalyDetector
        print("  ✓ anomaly_detector")
    except ImportError as e:
        print(f"  ✗ anomaly_detector: {e}")
        return False
    
    try:
        from expense_tracker.visualizer import ExpenseVisualizer
        print("  ✓ visualizer")
    except ImportError as e:
        print(f"  ✗ visualizer: {e}")
        return False
    
    try:
        from expense_tracker.ocr import BankStatementOCR
        print("  ✓ ocr")
    except ImportError as e:
        print(f"  ✗ ocr: {e}")
        return False
    
    return True


def test_basic_functionality():
    """Test basic functionality"""
    print("\nTesting basic functionality...")
    
    from datetime import datetime
    from expense_tracker.models import Transaction
    from expense_tracker.categorizer import ExpenseCategorizer
    
    try:
        # Create test transaction
        trans = Transaction(
            date=datetime(2024, 1, 1),
            description="Test Store",
            amount=50.00
        )
        print("  ✓ Transaction creation")
        
        # Test categorizer
        categorizer = ExpenseCategorizer()
        category = categorizer.categorize_transaction(trans)
        print(f"  ✓ Categorization (category: {category})")
        
        return True
    except Exception as e:
        print(f"  ✗ Basic functionality test failed: {e}")
        return False


def main():
    """Run all verification checks"""
    print("=" * 70)
    print("EXPENSE TRACKER VERIFICATION")
    print("=" * 70)
    
    all_passed = True
    
    # Check imports
    if not check_imports():
        all_passed = False
        print("\n⚠️  Some dependencies are missing. Run: pip install -r requirements.txt")
    
    # Check modules
    if not check_modules():
        all_passed = False
        print("\n⚠️  Some expense tracker modules failed to load.")
    
    # Test functionality
    if not test_basic_functionality():
        all_passed = False
    
    print("\n" + "=" * 70)
    if all_passed:
        print("✓ ALL CHECKS PASSED")
        print("=" * 70)
        print("\nExpense Tracker is properly installed and working!")
        print("\nNext steps:")
        print("  1. Run the demo: python demo.py")
        print("  2. Process a bank statement: expense-tracker process statement.pdf")
        print("  3. Read the documentation: README.md")
        return 0
    else:
        print("✗ SOME CHECKS FAILED")
        print("=" * 70)
        print("\nPlease fix the issues above and try again.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
