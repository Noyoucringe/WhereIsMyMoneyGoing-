"""
Visualization module for creating interactive charts and graphs
"""

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from typing import List, Dict
from datetime import datetime
from .models import Transaction


class ExpenseVisualizer:
    """Creates interactive visualizations for expense data"""
    
    def __init__(self):
        # Set style for matplotlib
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (12, 6)
    
    def create_dataframe(self, transactions: List[Transaction]) -> pd.DataFrame:
        """
        Convert transactions to pandas DataFrame
        
        Args:
            transactions: List of Transaction objects
            
        Returns:
            pandas DataFrame
        """
        data = []
        for t in transactions:
            data.append({
                'date': t.date,
                'description': t.description,
                'amount': abs(t.amount),
                'category': t.category,
                'is_anomaly': t.is_anomaly
            })
        
        df = pd.DataFrame(data)
        if not df.empty:
            df['date'] = pd.to_datetime(df['date'])
            df['month'] = df['date'].dt.to_period('M')
            df['day_of_week'] = df['date'].dt.day_name()
        
        return df
    
    def plot_category_pie_chart(self, transactions: List[Transaction], output_path: str = None):
        """
        Create pie chart of expenses by category
        
        Args:
            transactions: List of Transaction objects
            output_path: Optional path to save the plot
        """
        df = self.create_dataframe(transactions)
        
        if df.empty:
            print("No transactions to visualize")
            return
        
        category_totals = df.groupby('category')['amount'].sum().sort_values(ascending=False)
        
        fig = go.Figure(data=[go.Pie(
            labels=category_totals.index,
            values=category_totals.values,
            hole=0.3,
            textinfo='label+percent',
            textposition='auto'
        )])
        
        fig.update_layout(
            title='Expenses by Category',
            showlegend=True,
            height=600
        )
        
        if output_path:
            fig.write_html(output_path)
        else:
            fig.show()
        
        return fig
    
    def plot_spending_timeline(self, transactions: List[Transaction], output_path: str = None):
        """
        Create timeline of spending over time
        
        Args:
            transactions: List of Transaction objects
            output_path: Optional path to save the plot
        """
        df = self.create_dataframe(transactions)
        
        if df.empty:
            print("No transactions to visualize")
            return
        
        daily_spending = df.groupby('date')['amount'].sum().reset_index()
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=daily_spending['date'],
            y=daily_spending['amount'],
            mode='lines+markers',
            name='Daily Spending',
            line=dict(color='#1f77b4', width=2),
            marker=dict(size=6)
        ))
        
        # Add anomalies if present
        anomalies = df[df['is_anomaly'] == True]
        if not anomalies.empty:
            fig.add_trace(go.Scatter(
                x=anomalies['date'],
                y=anomalies['amount'],
                mode='markers',
                name='Anomalies',
                marker=dict(
                    size=12,
                    color='red',
                    symbol='x',
                    line=dict(width=2)
                )
            ))
        
        fig.update_layout(
            title='Spending Timeline',
            xaxis_title='Date',
            yaxis_title='Amount ($)',
            hovermode='x unified',
            height=500
        )
        
        if output_path:
            fig.write_html(output_path)
        else:
            fig.show()
        
        return fig
    
    def plot_category_bars(self, transactions: List[Transaction], output_path: str = None):
        """
        Create bar chart of expenses by category
        
        Args:
            transactions: List of Transaction objects
            output_path: Optional path to save the plot
        """
        df = self.create_dataframe(transactions)
        
        if df.empty:
            print("No transactions to visualize")
            return
        
        category_stats = df.groupby('category').agg({
            'amount': ['sum', 'mean', 'count']
        }).reset_index()
        
        category_stats.columns = ['category', 'total', 'average', 'count']
        category_stats = category_stats.sort_values('total', ascending=False)
        
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Total Spending by Category', 'Average Transaction by Category')
        )
        
        fig.add_trace(
            go.Bar(
                x=category_stats['category'],
                y=category_stats['total'],
                name='Total',
                marker_color='#1f77b4'
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Bar(
                x=category_stats['category'],
                y=category_stats['average'],
                name='Average',
                marker_color='#ff7f0e'
            ),
            row=1, col=2
        )
        
        fig.update_xaxes(tickangle=-45)
        fig.update_layout(
            title_text='Category Analysis',
            showlegend=False,
            height=500
        )
        
        if output_path:
            fig.write_html(output_path)
        else:
            fig.show()
        
        return fig
    
    def plot_monthly_trends(self, transactions: List[Transaction], output_path: str = None):
        """
        Create monthly spending trends
        
        Args:
            transactions: List of Transaction objects
            output_path: Optional path to save the plot
        """
        df = self.create_dataframe(transactions)
        
        if df.empty:
            print("No transactions to visualize")
            return
        
        monthly_by_category = df.groupby(['month', 'category'])['amount'].sum().reset_index()
        monthly_by_category['month'] = monthly_by_category['month'].astype(str)
        
        fig = px.bar(
            monthly_by_category,
            x='month',
            y='amount',
            color='category',
            title='Monthly Spending by Category',
            labels={'amount': 'Amount ($)', 'month': 'Month'},
            barmode='stack'
        )
        
        fig.update_layout(
            xaxis_title='Month',
            yaxis_title='Amount ($)',
            height=500
        )
        
        if output_path:
            fig.write_html(output_path)
        else:
            fig.show()
        
        return fig
    
    def plot_heatmap(self, transactions: List[Transaction], output_path: str = None):
        """
        Create heatmap of spending by day of week and category
        
        Args:
            transactions: List of Transaction objects
            output_path: Optional path to save the plot
        """
        df = self.create_dataframe(transactions)
        
        if df.empty:
            print("No transactions to visualize")
            return
        
        # Create pivot table
        heatmap_data = df.pivot_table(
            values='amount',
            index='day_of_week',
            columns='category',
            aggfunc='sum',
            fill_value=0
        )
        
        # Reorder days of week
        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        heatmap_data = heatmap_data.reindex([day for day in days_order if day in heatmap_data.index])
        
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_data.values,
            x=heatmap_data.columns,
            y=heatmap_data.index,
            colorscale='YlOrRd',
            text=heatmap_data.values,
            texttemplate='$%{text:.0f}',
            textfont={"size": 10}
        ))
        
        fig.update_layout(
            title='Spending Heatmap by Day of Week and Category',
            xaxis_title='Category',
            yaxis_title='Day of Week',
            height=500
        )
        
        if output_path:
            fig.write_html(output_path)
        else:
            fig.show()
        
        return fig
    
    def create_dashboard(self, transactions: List[Transaction], output_path: str = 'dashboard.html'):
        """
        Create comprehensive dashboard with all visualizations
        
        Args:
            transactions: List of Transaction objects
            output_path: Path to save the HTML dashboard
        """
        df = self.create_dataframe(transactions)
        
        if df.empty:
            print("No transactions to visualize")
            return
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                'Expenses by Category',
                'Spending Timeline',
                'Monthly Trends',
                'Top 10 Transactions'
            ),
            specs=[
                [{'type': 'pie'}, {'type': 'scatter'}],
                [{'type': 'bar'}, {'type': 'bar'}]
            ]
        )
        
        # 1. Pie chart
        category_totals = df.groupby('category')['amount'].sum().sort_values(ascending=False)
        fig.add_trace(
            go.Pie(labels=category_totals.index, values=category_totals.values, hole=0.3),
            row=1, col=1
        )
        
        # 2. Timeline
        daily_spending = df.groupby('date')['amount'].sum().reset_index()
        fig.add_trace(
            go.Scatter(x=daily_spending['date'], y=daily_spending['amount'], mode='lines+markers'),
            row=1, col=2
        )
        
        # 3. Monthly trends
        monthly_totals = df.groupby('month')['amount'].sum().reset_index()
        monthly_totals['month'] = monthly_totals['month'].astype(str)
        fig.add_trace(
            go.Bar(x=monthly_totals['month'], y=monthly_totals['amount']),
            row=2, col=1
        )
        
        # 4. Top transactions
        top_transactions = df.nlargest(10, 'amount')
        fig.add_trace(
            go.Bar(
                x=top_transactions['amount'],
                y=top_transactions['description'],
                orientation='h'
            ),
            row=2, col=2
        )
        
        fig.update_layout(
            title_text='Expense Tracking Dashboard',
            showlegend=False,
            height=800
        )
        
        fig.write_html(output_path)
        print(f"Dashboard saved to {output_path}")
        
        return fig
