"""
Transaction Parser Module
Parses and cleans transaction data from bank statements
"""

import re
import pandas as pd
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import dateutil.parser


class TransactionParser:
    """Parse and clean transaction data from text"""
    
    # Common date formats in bank statements
    DATE_PATTERNS = [
        r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}',  # DD/MM/YYYY or MM/DD/YYYY
        r'\d{4}[/-]\d{1,2}[/-]\d{1,2}',     # YYYY/MM/DD
        r'\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{2,4}',  # DD Mon YYYY
        r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{2,4}',  # Mon DD, YYYY
    ]
    
    # Amount patterns (including currency symbols)
    AMOUNT_PATTERNS = [
        r'[\$€£¥₹]\s*\d{1,3}(?:,\d{3})*(?:\.\d{2})?',  # $1,234.56
        r'\d{1,3}(?:,\d{3})*(?:\.\d{2})?\s*(?:USD|EUR|GBP|INR|RS)',  # 1,234.56 USD
        r'\d{1,3}(?:,\d{3})*(?:\.\d{2})?',  # 1,234.56
    ]
    
    def __init__(self):
        """Initialize transaction parser"""
        self.date_regex = re.compile('|'.join(f'({p})' for p in self.DATE_PATTERNS))
        self.amount_regex = re.compile('|'.join(f'({p})' for p in self.AMOUNT_PATTERNS))
    
    def parse_transactions(self, text: str) -> pd.DataFrame:
        """
        Parse transactions from extracted text
        
        Args:
            text: Raw text from bank statement
            
        Returns:
            DataFrame with columns: date, merchant, amount, description
        """
        lines = text.split('\n')
        transactions = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Try to extract transaction information
            transaction = self._parse_line(line)
            if transaction:
                transactions.append(transaction)
        
        if not transactions:
            return pd.DataFrame(columns=['date', 'merchant', 'amount', 'description'])
        
        df = pd.DataFrame(transactions)
        df = self._clean_dataframe(df)
        
        return df
    
    def _parse_line(self, line: str) -> Optional[Dict]:
        """
        Parse a single line for transaction information
        
        Args:
            line: Text line
            
        Returns:
            Dictionary with transaction data or None
        """
        # Look for date
        date_match = self.date_regex.search(line)
        if not date_match:
            return None
        
        date_str = date_match.group()
        
        # Look for amount
        amount_match = self.amount_regex.search(line)
        if not amount_match:
            return None
        
        amount_str = amount_match.group()
        
        # Extract merchant/description (text between date and amount)
        date_end = date_match.end()
        amount_start = amount_match.start()
        
        merchant = line[date_end:amount_start].strip()
        description = line
        
        # Clean merchant name
        merchant = self._clean_merchant(merchant)
        
        return {
            'date': date_str,
            'merchant': merchant,
            'amount': amount_str,
            'description': description
        }
    
    def _clean_merchant(self, merchant: str) -> str:
        """Clean merchant name"""
        # Remove common prefixes/suffixes
        merchant = re.sub(r'^(POS|ATM|ONLINE|DEBIT|CREDIT)\s*', '', merchant, flags=re.IGNORECASE)
        merchant = re.sub(r'\s+(LLC|INC|CORP|LTD)\.?$', '', merchant, flags=re.IGNORECASE)
        
        # Remove extra whitespace
        merchant = ' '.join(merchant.split())
        
        return merchant
    
    def _clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and standardize the dataframe
        
        Args:
            df: Raw transaction dataframe
            
        Returns:
            Cleaned dataframe
        """
        # Parse dates
        df['date'] = df['date'].apply(self._parse_date)
        
        # Parse amounts
        df['amount'] = df['amount'].apply(self._parse_amount)
        
        # Sort by date
        df = df.sort_values('date', ascending=False)
        
        # Reset index
        df = df.reset_index(drop=True)
        
        # Remove duplicates
        df = df.drop_duplicates(subset=['date', 'merchant', 'amount'], keep='first')
        
        return df
    
    def _parse_date(self, date_str: str) -> datetime:
        """
        Parse date string to datetime object
        
        Args:
            date_str: Date string
            
        Returns:
            datetime object
        """
        try:
            # Try using dateutil parser (handles multiple formats)
            return dateutil.parser.parse(date_str, dayfirst=False)
        except:
            try:
                # Try with dayfirst=True for DD/MM/YYYY
                return dateutil.parser.parse(date_str, dayfirst=True)
            except:
                # Return today's date as fallback
                return datetime.now()
    
    def _parse_amount(self, amount_str: str) -> float:
        """
        Parse amount string to float
        
        Args:
            amount_str: Amount string
            
        Returns:
            Float amount
        """
        # Remove currency symbols and text
        amount_str = re.sub(r'[^\d,.-]', '', amount_str)
        
        # Remove commas
        amount_str = amount_str.replace(',', '')
        
        try:
            return float(amount_str)
        except:
            return 0.0
    
    def parse_csv_statement(self, csv_path: str) -> pd.DataFrame:
        """
        Parse transactions from CSV file
        
        Args:
            csv_path: Path to CSV file
            
        Returns:
            DataFrame with standardized columns
        """
        try:
            df = pd.read_csv(csv_path)
            
            # Try to identify columns
            df_cleaned = self._standardize_columns(df)
            
            return df_cleaned
        except Exception as e:
            raise Exception(f"Error parsing CSV: {str(e)}")
    
    def _standardize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Standardize column names from various bank formats
        
        Args:
            df: Raw dataframe
            
        Returns:
            Dataframe with standard columns
        """
        # Common column name mappings
        column_mappings = {
            'date': ['date', 'transaction date', 'posting date', 'trans date'],
            'merchant': ['merchant', 'description', 'desc', 'payee', 'vendor'],
            'amount': ['amount', 'debit', 'withdrawal', 'spent', 'charge'],
        }
        
        renamed_cols = {}
        
        for standard_name, variations in column_mappings.items():
            for col in df.columns:
                if col.lower().strip() in variations:
                    renamed_cols[col] = standard_name
                    break
        
        df = df.rename(columns=renamed_cols)
        
        # Ensure required columns exist
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
        
        if 'amount' in df.columns:
            df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
        
        # Keep only relevant columns
        keep_cols = [col for col in ['date', 'merchant', 'amount', 'description'] if col in df.columns]
        
        return df[keep_cols]


def parse_transactions(text: str) -> pd.DataFrame:
    """
    Parse transactions from text
    
    Args:
        text: Raw text from bank statement
        
    Returns:
        DataFrame with transaction data
    """
    parser = TransactionParser()
    return parser.parse_transactions(text)


def parse_csv_statement(csv_path: str) -> pd.DataFrame:
    """
    Parse transactions from CSV file
    
    Args:
        csv_path: Path to CSV file
        
    Returns:
        DataFrame with transaction data
    """
    parser = TransactionParser()
    return parser.parse_csv_statement(csv_path)


if __name__ == "__main__":
    # Test the module
    print("Transaction Parser Module")
    print("=" * 50)
    print("\nUsage:")
    print("  from transaction_parser import parse_transactions")
    print("  df = parse_transactions(extracted_text)")
    
    # Example test
    sample_text = """
    01/15/2024  Amazon.com              $45.99
    01/16/2024  Starbucks Coffee        $5.75
    01/17/2024  Shell Gas Station       $52.30
    """
    
    df = parse_transactions(sample_text)
    print("\n\nSample parsing result:")
    print(df)
