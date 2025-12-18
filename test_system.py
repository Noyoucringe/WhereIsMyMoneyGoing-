"""
Test Script for "Where Is My Money Going?" Application
Run this to verify all modules are working correctly
"""

import sys
from pathlib import Path

def test_imports():
    """Test if all modules can be imported"""
    print("🧪 Testing module imports...")
    
    try:
        from ocr_extractor import OCRExtractor
        print("  ✅ ocr_extractor")
    except Exception as e:
        print(f"  ❌ ocr_extractor: {e}")
        return False
    
    try:
        from transaction_parser import TransactionParser
        print("  ✅ transaction_parser")
    except Exception as e:
        print(f"  ❌ transaction_parser: {e}")
        return False
    
    try:
        from categorizer import TransactionCategorizer
        print("  ✅ categorizer")
    except Exception as e:
        print(f"  ❌ categorizer: {e}")
        return False
    
    try:
        from analyzer import SpendingAnalyzer
        print("  ✅ analyzer")
    except Exception as e:
        print(f"  ❌ analyzer: {e}")
        return False
    
    try:
        from visualizer import SpendingVisualizer
        print("  ✅ visualizer")
    except Exception as e:
        print(f"  ❌ visualizer: {e}")
        return False
    
    return True


def test_dependencies():
    """Test if all required packages are installed"""
    print("\n🧪 Testing dependencies...")
    
    packages = [
        'pandas', 'numpy', 'matplotlib', 'seaborn', 'plotly',
        'streamlit', 'sklearn', 'scipy', 'PIL', 'pytesseract'
    ]
    
    all_installed = True
    
    for package in packages:
        try:
            if package == 'PIL':
                import PIL
            elif package == 'sklearn':
                import sklearn
            else:
                __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} (not installed)")
            all_installed = False
    
    return all_installed


def test_sample_workflow():
    """Test the complete workflow with sample data"""
    print("\n🧪 Testing sample workflow...")
    
    try:
        import pandas as pd
        from transaction_parser import TransactionParser
        from categorizer import TransactionCategorizer
        from analyzer import SpendingAnalyzer
        
        # Create sample data
        sample_data = {
            'date': ['2024-01-15', '2024-01-16', '2024-01-17'],
            'merchant': ['Starbucks Coffee', 'Shell Gas Station', 'Netflix'],
            'amount': [5.75, 52.30, 15.99]
        }
        
        df = pd.DataFrame(sample_data)
        df['date'] = pd.to_datetime(df['date'])
        
        print("  ✅ Created sample dataframe")
        
        # Categorize
        categorizer = TransactionCategorizer()
        df = categorizer.categorize_transactions(df)
        print("  ✅ Categorized transactions")
        
        # Analyze
        analyzer = SpendingAnalyzer(df)
        insights = analyzer.get_insights()
        print("  ✅ Generated insights")
        
        # Basic validation
        assert len(df) == 3, "DataFrame should have 3 transactions"
        assert 'category' in df.columns, "Category column should exist"
        assert insights['basic_stats']['total_transactions'] == 3, "Should count 3 transactions"
        
        print("  ✅ All validations passed")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def test_sample_csv():
    """Test loading the sample CSV file"""
    print("\n🧪 Testing sample CSV...")
    
    try:
        import pandas as pd
        from transaction_parser import TransactionParser
        
        csv_path = Path('sample_data/sample_transactions.csv')
        
        if not csv_path.exists():
            print(f"  ⚠️ Sample CSV not found at: {csv_path}")
            return False
        
        parser = TransactionParser()
        df = parser.parse_csv_statement(str(csv_path))
        
        print(f"  ✅ Loaded {len(df)} transactions from sample CSV")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def test_visualizations():
    """Test if visualization libraries work"""
    print("\n🧪 Testing visualization capabilities...")
    
    try:
        import matplotlib.pyplot as plt
        import seaborn as sns
        import plotly.express as px
        
        print("  ✅ Matplotlib")
        print("  ✅ Seaborn")
        print("  ✅ Plotly")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def main():
    """Run all tests"""
    print("="*60)
    print("💰 Where Is My Money Going? - System Test")
    print("="*60)
    
    results = {
        'Imports': test_imports(),
        'Dependencies': test_dependencies(),
        'Sample Workflow': test_sample_workflow(),
        'Sample CSV': test_sample_csv(),
        'Visualizations': test_visualizations(),
    }
    
    print("\n" + "="*60)
    print("📊 TEST RESULTS")
    print("="*60)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:.<40} {status}")
    
    all_passed = all(results.values())
    
    print("="*60)
    
    if all_passed:
        print("\n🎉 All tests passed! System is ready to use.")
        print("\n🚀 To launch the dashboard, run:")
        print("   streamlit run app.py")
    else:
        print("\n⚠️ Some tests failed. Please check the errors above.")
        print("\n📖 For installation help, see:")
        print("   INSTALLATION.md")
        print("\n💡 Common issues:")
        print("   - Missing packages: pip install -r requirements.txt")
        print("   - Tesseract not found: install from https://github.com/UB-Mannheim/tesseract/wiki")
    
    print()
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
