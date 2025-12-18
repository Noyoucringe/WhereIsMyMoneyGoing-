"""
Data models for expense tracking
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class Transaction:
    """Represents a single financial transaction"""
    date: datetime
    description: str
    amount: float
    category: str = "Uncategorized"
    is_anomaly: bool = False
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'date': self.date.isoformat() if isinstance(self.date, datetime) else self.date,
            'description': self.description,
            'amount': self.amount,
            'category': self.category,
            'is_anomaly': self.is_anomaly
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create from dictionary"""
        if isinstance(data['date'], str):
            data['date'] = datetime.fromisoformat(data['date'])
        return cls(**data)


@dataclass
class ExpenseCategory:
    """Represents an expense category"""
    name: str
    keywords: List[str] = field(default_factory=list)
    total_amount: float = 0.0
    transaction_count: int = 0
    
    def add_transaction(self, amount: float):
        """Add a transaction to this category"""
        self.total_amount += abs(amount)
        self.transaction_count += 1
    
    def average_amount(self) -> float:
        """Calculate average transaction amount"""
        if self.transaction_count == 0:
            return 0.0
        return self.total_amount / self.transaction_count
