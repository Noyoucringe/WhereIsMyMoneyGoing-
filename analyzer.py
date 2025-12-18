"""
Analyzer Module
Performs spending analysis and anomaly detection
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from scipy import stats


class SpendingAnalyzer:
    """Analyze spending patterns and detect anomalies"""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize analyzer with transaction data
        
        Args:
            df: DataFrame with transaction data
        """
        self.df = df.copy()
        
        # Ensure date is datetime
        if 'date' in self.df.columns:
            self.df['date'] = pd.to_datetime(self.df['date'])
        
        # Ensure amount is numeric
        if 'amount' in self.df.columns:
            self.df['amount'] = pd.to_numeric(self.df['amount'], errors='coerce')
    
    def get_basic_stats(self) -> Dict:
        """
        Get basic spending statistics
        
        Returns:
            Dictionary with basic stats
        """
        stats = {
            'total_transactions': len(self.df),
            'total_spent': self.df['amount'].sum(),
            'average_transaction': self.df['amount'].mean(),
            'median_transaction': self.df['amount'].median(),
            'largest_transaction': self.df['amount'].max(),
            'smallest_transaction': self.df['amount'].min(),
            'std_deviation': self.df['amount'].std(),
        }
        
        if 'date' in self.df.columns:
            date_range = (self.df['date'].max() - self.df['date'].min()).days
            stats['date_range_days'] = date_range
            stats['transactions_per_day'] = len(self.df) / max(date_range, 1)
        
        return stats
    
    def get_spending_by_period(self, period: str = 'M') -> pd.DataFrame:
        """
        Get spending aggregated by time period
        
        Args:
            period: Time period ('D' for daily, 'W' for weekly, 'M' for monthly)
            
        Returns:
            DataFrame with period and total spending
        """
        if 'date' not in self.df.columns:
            raise ValueError("DataFrame must have 'date' column")
        
        # Group by period
        spending = self.df.groupby(pd.Grouper(key='date', freq=period)).agg({
            'amount': ['sum', 'count', 'mean']
        }).round(2)
        
        spending.columns = ['Total Spent', 'Transaction Count', 'Average Amount']
        spending = spending.reset_index()
        
        return spending
    
    def detect_anomalies(self, method: str = 'zscore', threshold: float = 3.0) -> pd.DataFrame:
        """
        Detect anomalous transactions
        
        Args:
            method: Detection method ('zscore', 'iqr', or 'isolation')
            threshold: Threshold for anomaly detection
            
        Returns:
            DataFrame with anomalous transactions
        """
        if method == 'zscore':
            return self._detect_zscore_anomalies(threshold)
        elif method == 'iqr':
            return self._detect_iqr_anomalies()
        elif method == 'isolation':
            return self._detect_isolation_forest_anomalies()
        else:
            raise ValueError(f"Unknown method: {method}")
    
    def _detect_zscore_anomalies(self, threshold: float = 3.0) -> pd.DataFrame:
        """
        Detect anomalies using Z-score method
        
        Args:
            threshold: Z-score threshold
            
        Returns:
            DataFrame with anomalous transactions
        """
        # Calculate Z-scores
        z_scores = np.abs(stats.zscore(self.df['amount']))
        
        # Find anomalies
        anomalies = self.df[z_scores > threshold].copy()
        anomalies['z_score'] = z_scores[z_scores > threshold]
        anomalies['reason'] = 'Unusually high amount (Z-score > ' + str(threshold) + ')'
        
        return anomalies.sort_values('amount', ascending=False)
    
    def _detect_iqr_anomalies(self) -> pd.DataFrame:
        """
        Detect anomalies using Interquartile Range (IQR) method
        
        Returns:
            DataFrame with anomalous transactions
        """
        Q1 = self.df['amount'].quantile(0.25)
        Q3 = self.df['amount'].quantile(0.75)
        IQR = Q3 - Q1
        
        # Define outlier boundaries
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        # Find anomalies
        anomalies = self.df[
            (self.df['amount'] < lower_bound) | 
            (self.df['amount'] > upper_bound)
        ].copy()
        
        anomalies['reason'] = anomalies['amount'].apply(
            lambda x: 'Unusually low' if x < lower_bound else 'Unusually high'
        )
        
        return anomalies.sort_values('amount', ascending=False)
    
    def _detect_isolation_forest_anomalies(self) -> pd.DataFrame:
        """
        Detect anomalies using Isolation Forest algorithm
        
        Returns:
            DataFrame with anomalous transactions
        """
        from sklearn.ensemble import IsolationForest
        
        # Prepare features
        X = self.df[['amount']].values
        
        # Train isolation forest
        iso_forest = IsolationForest(contamination=0.1, random_state=42)
        predictions = iso_forest.fit_predict(X)
        
        # Find anomalies (predictions == -1)
        anomalies = self.df[predictions == -1].copy()
        anomalies['reason'] = 'Detected by Isolation Forest'
        
        return anomalies.sort_values('amount', ascending=False)
    
    def find_duplicate_transactions(self, time_window: int = 1) -> pd.DataFrame:
        """
        Find potential duplicate transactions
        
        Args:
            time_window: Time window in days to check for duplicates
            
        Returns:
            DataFrame with potential duplicates
        """
        if 'date' not in self.df.columns:
            raise ValueError("DataFrame must have 'date' column")
        
        duplicates = []
        
        # Sort by date
        df_sorted = self.df.sort_values('date')
        
        for i, row in df_sorted.iterrows():
            # Find transactions with same amount within time window
            similar = df_sorted[
                (df_sorted['amount'] == row['amount']) &
                (df_sorted['date'] >= row['date']) &
                (df_sorted['date'] <= row['date'] + timedelta(days=time_window)) &
                (df_sorted.index != i)
            ]
            
            if len(similar) > 0:
                for j, sim_row in similar.iterrows():
                    duplicates.append({
                        'date1': row['date'],
                        'merchant1': row.get('merchant', ''),
                        'amount': row['amount'],
                        'date2': sim_row['date'],
                        'merchant2': sim_row.get('merchant', ''),
                        'days_apart': (sim_row['date'] - row['date']).days
                    })
        
        if duplicates:
            return pd.DataFrame(duplicates).drop_duplicates()
        else:
            return pd.DataFrame(columns=['date1', 'merchant1', 'amount', 'date2', 'merchant2', 'days_apart'])
    
    def get_top_merchants(self, n: int = 10) -> pd.DataFrame:
        """
        Get top merchants by spending
        
        Args:
            n: Number of top merchants to return
            
        Returns:
            DataFrame with top merchants
        """
        if 'merchant' not in self.df.columns:
            raise ValueError("DataFrame must have 'merchant' column")
        
        top_merchants = self.df.groupby('merchant').agg({
            'amount': ['sum', 'count', 'mean']
        }).round(2)
        
        top_merchants.columns = ['Total Spent', 'Transaction Count', 'Average Amount']
        top_merchants = top_merchants.sort_values('Total Spent', ascending=False).head(n)
        
        return top_merchants
    
    def get_spending_trends(self, window: int = 7) -> pd.DataFrame:
        """
        Calculate spending trends using moving average
        
        Args:
            window: Window size for moving average (days)
            
        Returns:
            DataFrame with trends
        """
        if 'date' not in self.df.columns:
            raise ValueError("DataFrame must have 'date' column")
        
        # Daily spending
        daily = self.df.groupby('date')['amount'].sum().reset_index()
        daily = daily.sort_values('date')
        
        # Calculate moving average
        daily['moving_avg'] = daily['amount'].rolling(window=window, min_periods=1).mean()
        
        # Calculate trend direction
        daily['trend'] = daily['moving_avg'].diff()
        
        return daily
    
    def compare_periods(self, period1_start: str, period1_end: str,
                       period2_start: str, period2_end: str) -> Dict:
        """
        Compare spending between two time periods
        
        Args:
            period1_start: Start date of first period
            period1_end: End date of first period
            period2_start: Start date of second period
            period2_end: End date of second period
            
        Returns:
            Dictionary with comparison statistics
        """
        if 'date' not in self.df.columns:
            raise ValueError("DataFrame must have 'date' column")
        
        # Convert to datetime
        p1_start = pd.to_datetime(period1_start)
        p1_end = pd.to_datetime(period1_end)
        p2_start = pd.to_datetime(period2_start)
        p2_end = pd.to_datetime(period2_end)
        
        # Filter data
        period1 = self.df[(self.df['date'] >= p1_start) & (self.df['date'] <= p1_end)]
        period2 = self.df[(self.df['date'] >= p2_start) & (self.df['date'] <= p2_end)]
        
        comparison = {
            'period1_total': period1['amount'].sum(),
            'period1_count': len(period1),
            'period1_average': period1['amount'].mean(),
            'period2_total': period2['amount'].sum(),
            'period2_count': len(period2),
            'period2_average': period2['amount'].mean(),
        }
        
        # Calculate differences
        comparison['total_difference'] = comparison['period2_total'] - comparison['period1_total']
        comparison['percentage_change'] = (
            (comparison['total_difference'] / comparison['period1_total'] * 100)
            if comparison['period1_total'] > 0 else 0
        )
        
        return comparison
    
    def get_insights(self) -> Dict[str, any]:
        """
        Generate comprehensive spending insights
        
        Returns:
            Dictionary with various insights
        """
        insights = {
            'basic_stats': self.get_basic_stats(),
        }
        
        # Category insights (if available)
        if 'category' in self.df.columns:
            category_summary = self.df.groupby('category')['amount'].agg(['sum', 'count', 'mean']).round(2)
            insights['top_category'] = category_summary['sum'].idxmax()
            insights['top_category_amount'] = category_summary['sum'].max()
            insights['category_breakdown'] = category_summary.to_dict()
        
        # Merchant insights
        if 'merchant' in self.df.columns:
            merchant_summary = self.df.groupby('merchant')['amount'].sum().sort_values(ascending=False)
            insights['top_merchant'] = merchant_summary.index[0] if len(merchant_summary) > 0 else None
            insights['top_merchant_amount'] = merchant_summary.iloc[0] if len(merchant_summary) > 0 else 0
        
        # Anomalies
        anomalies = self.detect_anomalies(method='zscore', threshold=2.5)
        insights['anomaly_count'] = len(anomalies)
        
        # Duplicates
        duplicates = self.find_duplicate_transactions()
        insights['potential_duplicates'] = len(duplicates)
        
        return insights


def analyze_spending(df: pd.DataFrame) -> Dict:
    """
    Analyze spending patterns
    
    Args:
        df: DataFrame with transaction data
        
    Returns:
        Dictionary with insights
    """
    analyzer = SpendingAnalyzer(df)
    return analyzer.get_insights()


def detect_anomalies(df: pd.DataFrame, method: str = 'zscore') -> pd.DataFrame:
    """
    Detect anomalous transactions
    
    Args:
        df: DataFrame with transaction data
        method: Detection method
        
    Returns:
        DataFrame with anomalies
    """
    analyzer = SpendingAnalyzer(df)
    return analyzer.detect_anomalies(method=method)


if __name__ == "__main__":
    # Test the module
    print("Spending Analyzer Module")
    print("=" * 50)
    print("\nUsage:")
    print("  from analyzer import analyze_spending, detect_anomalies")
    print("  insights = analyze_spending(df)")
    print("  anomalies = detect_anomalies(df)")
