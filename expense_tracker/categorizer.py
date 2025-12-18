"""
Categorization engine for automatically categorizing transactions
"""

import re
from typing import List, Dict
from .models import Transaction, ExpenseCategory


class ExpenseCategorizer:
    """Automatically categorizes expenses based on keywords and patterns"""
    
    def __init__(self):
        self.categories = self._initialize_categories()
    
    def _initialize_categories(self) -> Dict[str, ExpenseCategory]:
        """Initialize default expense categories with keywords"""
        categories = {
            'Groceries': ExpenseCategory(
                name='Groceries',
                keywords=['grocery', 'supermarket', 'walmart', 'target', 'costco', 'whole foods',
                         'trader joe', 'safeway', 'kroger', 'albertsons', 'food mart']
            ),
            'Restaurants': ExpenseCategory(
                name='Restaurants',
                keywords=['restaurant', 'cafe', 'coffee', 'starbucks', 'mcdonald', 'burger',
                         'pizza', 'dining', 'food delivery', 'uber eats', 'doordash', 'grubhub']
            ),
            'Transportation': ExpenseCategory(
                name='Transportation',
                keywords=['gas', 'fuel', 'uber', 'lyft', 'taxi', 'parking', 'metro', 'transit',
                         'subway', 'train', 'bus', 'toll', 'chevron', 'shell', 'exxon', 'bp']
            ),
            'Utilities': ExpenseCategory(
                name='Utilities',
                keywords=['electric', 'electricity', 'power', 'gas company', 'water', 'sewage',
                         'internet', 'phone', 'mobile', 'cable', 'utility']
            ),
            'Entertainment': ExpenseCategory(
                name='Entertainment',
                keywords=['movie', 'cinema', 'theater', 'theatre', 'netflix', 'spotify', 'hulu',
                         'disney', 'amazon prime', 'gaming', 'concert', 'music', 'entertainment']
            ),
            'Shopping': ExpenseCategory(
                name='Shopping',
                keywords=['amazon', 'ebay', 'store', 'shop', 'retail', 'clothing', 'apparel',
                         'fashion', 'mall', 'department']
            ),
            'Healthcare': ExpenseCategory(
                name='Healthcare',
                keywords=['pharmacy', 'doctor', 'hospital', 'medical', 'health', 'clinic',
                         'dental', 'dentist', 'cvs', 'walgreens', 'rite aid']
            ),
            'Insurance': ExpenseCategory(
                name='Insurance',
                keywords=['insurance', 'premium', 'policy']
            ),
            'Housing': ExpenseCategory(
                name='Housing',
                keywords=['rent', 'mortgage', 'lease', 'property', 'hoa', 'homeowner']
            ),
            'Education': ExpenseCategory(
                name='Education',
                keywords=['tuition', 'school', 'university', 'college', 'education', 'course',
                         'book', 'textbook', 'student']
            ),
            'Fitness': ExpenseCategory(
                name='Fitness',
                keywords=['gym', 'fitness', 'yoga', 'sport', 'athletic', 'exercise']
            ),
            'Travel': ExpenseCategory(
                name='Travel',
                keywords=['hotel', 'airbnb', 'airline', 'flight', 'airport', 'booking',
                         'travel', 'vacation', 'resort']
            ),
            'Subscriptions': ExpenseCategory(
                name='Subscriptions',
                keywords=['subscription', 'membership', 'monthly', 'annual fee']
            )
        }
        return categories
    
    def categorize_transaction(self, transaction: Transaction) -> str:
        """
        Categorize a single transaction based on its description
        
        Args:
            transaction: Transaction object to categorize
            
        Returns:
            Category name
        """
        description_lower = transaction.description.lower()
        
        # Check each category's keywords
        for category_name, category in self.categories.items():
            for keyword in category.keywords:
                if keyword in description_lower:
                    return category_name
        
        # Default category if no match found
        return 'Other'
    
    def categorize_transactions(self, transactions: List[Transaction]) -> List[Transaction]:
        """
        Categorize a list of transactions
        
        Args:
            transactions: List of Transaction objects
            
        Returns:
            List of categorized transactions
        """
        for transaction in transactions:
            category = self.categorize_transaction(transaction)
            transaction.category = category
            
            # Update category statistics
            if category in self.categories:
                self.categories[category].add_transaction(transaction.amount)
        
        return transactions
    
    def get_category_summary(self) -> Dict[str, Dict]:
        """
        Get summary statistics for all categories
        
        Returns:
            Dictionary with category statistics
        """
        summary = {}
        for name, category in self.categories.items():
            if category.transaction_count > 0:
                summary[name] = {
                    'total_amount': round(category.total_amount, 2),
                    'transaction_count': category.transaction_count,
                    'average_amount': round(category.average_amount(), 2)
                }
        return summary
    
    def add_custom_category(self, name: str, keywords: List[str]):
        """
        Add a custom category with keywords
        
        Args:
            name: Category name
            keywords: List of keywords for the category
        """
        self.categories[name] = ExpenseCategory(name=name, keywords=keywords)
