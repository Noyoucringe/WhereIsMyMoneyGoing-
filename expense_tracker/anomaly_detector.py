"""
Anomaly detection for identifying unusual spending patterns
"""

import numpy as np
from typing import List, Dict, Tuple
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta
from .models import Transaction


class AnomalyDetector:
    """Detects anomalies in spending patterns using multiple methods"""
    
    def __init__(self, contamination: float = 0.1):
        """
        Initialize anomaly detector
        
        Args:
            contamination: Expected proportion of anomalies (0.0 to 0.5)
        """
        self.contamination = contamination
        self.scaler = StandardScaler()
        self.isolation_forest = IsolationForest(
            contamination=contamination,
            random_state=42
        )
        self.baseline_stats = {}
    
    def calculate_baseline_stats(self, transactions: List[Transaction]):
        """
        Calculate baseline statistics for each category
        
        Args:
            transactions: List of Transaction objects
        """
        category_data = {}
        
        for transaction in transactions:
            category = transaction.category
            amount = abs(transaction.amount)
            
            if category not in category_data:
                category_data[category] = []
            category_data[category].append(amount)
        
        # Calculate mean and std for each category
        for category, amounts in category_data.items():
            amounts_array = np.array(amounts)
            self.baseline_stats[category] = {
                'mean': np.mean(amounts_array),
                'std': np.std(amounts_array),
                'median': np.median(amounts_array),
                'q1': np.percentile(amounts_array, 25),
                'q3': np.percentile(amounts_array, 75)
            }
    
    def detect_statistical_anomalies(self, transactions: List[Transaction]) -> List[Transaction]:
        """
        Detect anomalies using statistical methods (z-score and IQR)
        
        Args:
            transactions: List of Transaction objects
            
        Returns:
            List of transactions marked as anomalies
        """
        if not self.baseline_stats:
            self.calculate_baseline_stats(transactions)
        
        anomalies = []
        
        for transaction in transactions:
            category = transaction.category
            amount = abs(transaction.amount)
            
            if category not in self.baseline_stats:
                continue
            
            stats = self.baseline_stats[category]
            
            # Z-score method
            if stats['std'] > 0:
                z_score = abs((amount - stats['mean']) / stats['std'])
                if z_score > 3:  # 3 sigma rule
                    transaction.is_anomaly = True
                    anomalies.append(transaction)
                    continue
            
            # IQR method
            iqr = stats['q3'] - stats['q1']
            lower_bound = stats['q1'] - 1.5 * iqr
            upper_bound = stats['q3'] + 1.5 * iqr
            
            if amount < lower_bound or amount > upper_bound:
                transaction.is_anomaly = True
                anomalies.append(transaction)
        
        return anomalies
    
    def detect_ml_anomalies(self, transactions: List[Transaction]) -> List[Transaction]:
        """
        Detect anomalies using machine learning (Isolation Forest)
        
        Args:
            transactions: List of Transaction objects
            
        Returns:
            List of transactions marked as anomalies
        """
        if len(transactions) < 10:
            # Not enough data for ML
            return []
        
        # Prepare features: amount, day of week, day of month
        features = []
        for transaction in transactions:
            amount = abs(transaction.amount)
            day_of_week = transaction.date.weekday()
            day_of_month = transaction.date.day
            
            # Category encoding (simple: use hash)
            category_hash = hash(transaction.category) % 100
            
            features.append([amount, day_of_week, day_of_month, category_hash])
        
        features_array = np.array(features)
        
        # Scale features
        features_scaled = self.scaler.fit_transform(features_array)
        
        # Predict anomalies (-1 for anomaly, 1 for normal)
        predictions = self.isolation_forest.fit_predict(features_scaled)
        
        anomalies = []
        for i, prediction in enumerate(predictions):
            if prediction == -1:
                transactions[i].is_anomaly = True
                anomalies.append(transactions[i])
        
        return anomalies
    
    def detect_frequency_anomalies(self, transactions: List[Transaction]) -> List[Transaction]:
        """
        Detect anomalies based on unusual transaction frequency
        
        Args:
            transactions: List of Transaction objects
            
        Returns:
            List of transactions that are part of unusual patterns
        """
        # Group by merchant/description
        merchant_transactions = {}
        
        for transaction in transactions:
            desc = transaction.description
            if desc not in merchant_transactions:
                merchant_transactions[desc] = []
            merchant_transactions[desc].append(transaction)
        
        anomalies = []
        
        for desc, trans_list in merchant_transactions.items():
            if len(trans_list) < 2:
                continue
            
            # Sort by date
            trans_list.sort(key=lambda x: x.date)
            
            # Calculate time differences
            time_diffs = []
            for i in range(1, len(trans_list)):
                diff = (trans_list[i].date - trans_list[i-1].date).days
                time_diffs.append(diff)
            
            if not time_diffs:
                continue
            
            # Check for unusual frequency (transactions too close together)
            avg_diff = np.mean(time_diffs)
            for i, diff in enumerate(time_diffs):
                if diff < avg_diff / 3 and diff < 2:  # Transactions within 2 days and much faster than average
                    # Mark both transactions as potential anomalies
                    if not trans_list[i].is_anomaly:
                        trans_list[i].is_anomaly = True
                        anomalies.append(trans_list[i])
                    if not trans_list[i+1].is_anomaly:
                        trans_list[i+1].is_anomaly = True
                        anomalies.append(trans_list[i+1])
        
        return anomalies
    
    def detect_all_anomalies(self, transactions: List[Transaction]) -> Dict[str, List[Transaction]]:
        """
        Run all anomaly detection methods
        
        Args:
            transactions: List of Transaction objects
            
        Returns:
            Dictionary with anomalies from each method
        """
        # Reset anomaly flags
        for transaction in transactions:
            transaction.is_anomaly = False
        
        # Run detection methods on original list (they modify in place)
        statistical_anomalies = self.detect_statistical_anomalies(transactions)
        ml_anomalies = self.detect_ml_anomalies(transactions)
        frequency_anomalies = self.detect_frequency_anomalies(transactions)
        
        results = {
            'statistical': statistical_anomalies,
            'ml_based': ml_anomalies,
            'frequency': frequency_anomalies
        }
        
        return results
    
    def get_anomaly_summary(self, transactions: List[Transaction]) -> Dict:
        """
        Get summary of anomalies
        
        Args:
            transactions: List of Transaction objects
            
        Returns:
            Summary dictionary
        """
        anomalies = [t for t in transactions if t.is_anomaly]
        
        total_anomaly_amount = sum(abs(t.amount) for t in anomalies)
        
        return {
            'total_transactions': len(transactions),
            'anomaly_count': len(anomalies),
            'anomaly_percentage': round(len(anomalies) / len(transactions) * 100, 2) if transactions else 0,
            'total_anomaly_amount': round(total_anomaly_amount, 2),
            'anomalies': [
                {
                    'date': t.date.strftime('%Y-%m-%d'),
                    'description': t.description,
                    'amount': t.amount,
                    'category': t.category
                }
                for t in sorted(anomalies, key=lambda x: abs(x.amount), reverse=True)[:10]
            ]
        }
