"""
Transaction Categorizer Module
Automatically categorizes transactions into spending categories
"""

import pandas as pd
import re
from typing import Dict, List, Optional


class TransactionCategorizer:
    """Categorize transactions based on merchant names and patterns"""
    
    # Category keywords - expanded for better accuracy
    CATEGORY_KEYWORDS = {
        'Food & Dining': [
            'restaurant', 'cafe', 'coffee', 'starbucks', 'pizza', 'burger',
            'mcdonald', 'subway', 'chipotle', 'domino', 'taco', 'kfc',
            'wendy', 'dunkin', 'bakery', 'diner', 'grill', 'kitchen',
            'bar', 'pub', 'bistro', 'food', 'dining', 'eatery', 'doordash',
            'ubereats', 'grubhub', 'zomato', 'swiggy', 'delivery'
        ],
        'Groceries': [
            'supermarket', 'grocery', 'walmart', 'target', 'costco',
            'safeway', 'kroger', 'albertsons', 'whole foods', 'trader joe',
            'aldi', 'market', 'fresh', 'organic', 'produce', 'mart'
        ],
        'Transportation': [
            'gas', 'fuel', 'shell', 'chevron', 'exxon', 'bp', 'mobil',
            'uber', 'lyft', 'taxi', 'cab', 'transit', 'metro', 'bus',
            'train', 'parking', 'toll', 'transportation', 'airline',
            'flight', 'airport'
        ],
        'Shopping': [
            'amazon', 'ebay', 'etsy', 'shop', 'store', 'mall', 'retail',
            'clothing', 'apparel', 'fashion', 'shoes', 'accessories',
            'electronics', 'best buy', 'apple store', 'outlet', 'boutique'
        ],
        'Entertainment': [
            'movie', 'cinema', 'theater', 'netflix', 'hulu', 'spotify',
            'disney', 'hbo', 'prime video', 'youtube', 'gaming', 'steam',
            'playstation', 'xbox', 'concert', 'event', 'tickets', 'ticketmaster'
        ],
        'Utilities': [
            'electric', 'electricity', 'power', 'gas company', 'water',
            'sewer', 'internet', 'phone', 'verizon', 'at&t', 't-mobile',
            'sprint', 'comcast', 'spectrum', 'utility', 'bill'
        ],
        'Healthcare': [
            'pharmacy', 'cvs', 'walgreens', 'doctor', 'hospital', 'clinic',
            'medical', 'dental', 'dentist', 'health', 'wellness', 'urgent care',
            'lab', 'prescription', 'medicine', 'drug'
        ],
        'Rent/Housing': [
            'rent', 'lease', 'apartment', 'property', 'landlord', 'housing',
            'mortgage', 'hoa', 'home', 'real estate', 'realty'
        ],
        'Insurance': [
            'insurance', 'premium', 'policy', 'geico', 'progressive',
            'state farm', 'allstate', 'coverage'
        ],
        'Education': [
            'school', 'university', 'college', 'tuition', 'book', 'course',
            'education', 'learning', 'academy', 'institute', 'udemy',
            'coursera', 'textbook'
        ],
        'Subscriptions': [
            'subscription', 'monthly', 'membership', 'annual', 'renew',
            'gym', 'fitness', 'planet fitness', '24 hour', 'crunch',
            'adobe', 'microsoft', 'office 365', 'dropbox', 'icloud'
        ],
        'Personal Care': [
            'salon', 'spa', 'barber', 'haircut', 'beauty', 'cosmetic',
            'makeup', 'skincare', 'massage', 'nail', 'grooming'
        ],
        'Financial': [
            'bank', 'atm', 'fee', 'charge', 'interest', 'transfer',
            'payment', 'withdrawal', 'deposit'
        ],
        'Charity': [
            'donation', 'charity', 'foundation', 'nonprofit', 'church',
            'temple', 'mosque', 'giving', 'fundraiser'
        ],
        'Travel': [
            'hotel', 'motel', 'resort', 'booking', 'airbnb', 'hostel',
            'marriott', 'hilton', 'hyatt', 'expedia', 'travel', 'vacation'
        ],
        'Pet Care': [
            'pet', 'vet', 'veterinary', 'petsmart', 'petco', 'grooming',
            'animal', 'dog', 'cat'
        ],
    }
    
    def __init__(self, custom_categories: Optional[Dict[str, List[str]]] = None):
        """
        Initialize categorizer
        
        Args:
            custom_categories: Optional custom category keywords to add/override
        """
        self.categories = self.CATEGORY_KEYWORDS.copy()
        
        if custom_categories:
            self.categories.update(custom_categories)
        
        # Compile regex patterns for efficiency
        self._compile_patterns()
    
    def _compile_patterns(self):
        """Compile regex patterns for each category"""
        self.category_patterns = {}
        
        for category, keywords in self.categories.items():
            # Create regex pattern that matches any keyword
            pattern = '|'.join(re.escape(kw) for kw in keywords)
            self.category_patterns[category] = re.compile(pattern, re.IGNORECASE)
    
    def categorize_transaction(self, merchant: str, description: str = '') -> str:
        """
        Categorize a single transaction
        
        Args:
            merchant: Merchant name
            description: Transaction description
            
        Returns:
            Category name
        """
        text = f"{merchant} {description}".lower()
        
        # Check each category
        for category, pattern in self.category_patterns.items():
            if pattern.search(text):
                return category
        
        return 'Other'
    
    def categorize_transactions(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Categorize all transactions in a dataframe
        
        Args:
            df: DataFrame with 'merchant' column
            
        Returns:
            DataFrame with added 'category' column
        """
        if 'merchant' not in df.columns:
            raise ValueError("DataFrame must have 'merchant' column")
        
        # Add description if not present
        if 'description' not in df.columns:
            df['description'] = ''
        
        # Categorize each transaction
        df['category'] = df.apply(
            lambda row: self.categorize_transaction(
                str(row['merchant']), 
                str(row.get('description', ''))
            ),
            axis=1
        )
        
        return df
    
    def get_category_summary(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Get spending summary by category
        
        Args:
            df: DataFrame with 'category' and 'amount' columns
            
        Returns:
            Summary DataFrame
        """
        if 'category' not in df.columns:
            df = self.categorize_transactions(df)
        
        summary = df.groupby('category').agg({
            'amount': ['sum', 'count', 'mean']
        }).round(2)
        
        summary.columns = ['Total Spent', 'Transaction Count', 'Average Amount']
        summary = summary.sort_values('Total Spent', ascending=False)
        
        return summary
    
    def get_monthly_category_breakdown(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Get spending by category for each month
        
        Args:
            df: DataFrame with 'date', 'category', and 'amount' columns
            
        Returns:
            Pivot table with months as rows and categories as columns
        """
        if 'category' not in df.columns:
            df = self.categorize_transactions(df)
        
        if 'date' not in df.columns:
            raise ValueError("DataFrame must have 'date' column")
        
        # Ensure date is datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # Extract month
        df['month'] = df['date'].dt.to_period('M')
        
        # Create pivot table
        pivot = df.pivot_table(
            values='amount',
            index='month',
            columns='category',
            aggfunc='sum',
            fill_value=0
        ).round(2)
        
        return pivot
    
    def add_custom_category(self, category_name: str, keywords: List[str]):
        """
        Add a new custom category
        
        Args:
            category_name: Name of the category
            keywords: List of keywords for this category
        """
        self.categories[category_name] = keywords
        self._compile_patterns()
    
    def update_category_keywords(self, category_name: str, keywords: List[str]):
        """
        Update keywords for an existing category
        
        Args:
            category_name: Name of the category
            keywords: List of keywords to add
        """
        if category_name in self.categories:
            self.categories[category_name].extend(keywords)
            self._compile_patterns()
        else:
            self.add_custom_category(category_name, keywords)


def categorize_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Categorize transactions in a dataframe
    
    Args:
        df: DataFrame with transaction data
        
    Returns:
        DataFrame with 'category' column added
    """
    categorizer = TransactionCategorizer()
    return categorizer.categorize_transactions(df)


def get_category_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Get spending summary by category
    
    Args:
        df: DataFrame with categorized transactions
        
    Returns:
        Summary DataFrame
    """
    categorizer = TransactionCategorizer()
    return categorizer.get_category_summary(df)


if __name__ == "__main__":
    # Test the module
    print("Transaction Categorizer Module")
    print("=" * 50)
    print("\nUsage:")
    print("  from categorizer import categorize_transactions")
    print("  df = categorize_transactions(transactions_df)")
    
    # Example test
    sample_data = {
        'date': ['2024-01-15', '2024-01-16', '2024-01-17'],
        'merchant': ['Starbucks', 'Shell Gas', 'Netflix'],
        'amount': [5.75, 52.30, 15.99]
    }
    
    df = pd.DataFrame(sample_data)
    df = categorize_transactions(df)
    
    print("\n\nSample categorization:")
    print(df[['merchant', 'amount', 'category']])
    
    print("\n\nCategory summary:")
    print(get_category_summary(df))
