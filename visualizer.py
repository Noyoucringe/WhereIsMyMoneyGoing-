"""
Visualizer Module
Creates charts and visualizations for spending analysis
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from typing import Optional, Tuple
import io


# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)


class SpendingVisualizer:
    """Create visualizations for spending data"""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize visualizer with transaction data
        
        Args:
            df: DataFrame with transaction data
        """
        self.df = df.copy()
        
        # Ensure date is datetime
        if 'date' in self.df.columns:
            self.df['date'] = pd.to_datetime(self.df['date'])
    
    def create_pie_chart(self, column: str = 'category', 
                        title: str = 'Spending by Category',
                        interactive: bool = True):
        """
        Create pie chart for spending distribution
        
        Args:
            column: Column to aggregate by
            title: Chart title
            interactive: If True, create plotly chart; else matplotlib
            
        Returns:
            Plotly figure or matplotlib figure
        """
        if column not in self.df.columns:
            raise ValueError(f"Column '{column}' not found in dataframe")
        
        # Aggregate spending by column
        spending = self.df.groupby(column)['amount'].sum().sort_values(ascending=False)
        
        if interactive:
            # Create interactive plotly pie chart
            fig = px.pie(
                values=spending.values,
                names=spending.index,
                title=title,
                hole=0.3,  # Donut chart
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            return fig
        else:
            # Create matplotlib pie chart
            fig, ax = plt.subplots(figsize=(10, 8))
            colors = sns.color_palette('husl', len(spending))
            
            ax.pie(spending.values, labels=spending.index, autopct='%1.1f%%',
                   startangle=90, colors=colors)
            ax.set_title(title, fontsize=16, fontweight='bold')
            
            return fig
    
    def create_spending_over_time(self, period: str = 'M',
                                   title: str = 'Spending Over Time',
                                   interactive: bool = True):
        """
        Create line chart for spending over time
        
        Args:
            period: Time period ('D' for daily, 'W' for weekly, 'M' for monthly)
            title: Chart title
            interactive: If True, create plotly chart; else matplotlib
            
        Returns:
            Plotly figure or matplotlib figure
        """
        if 'date' not in self.df.columns:
            raise ValueError("DataFrame must have 'date' column")
        
        # Aggregate by period
        spending = self.df.groupby(pd.Grouper(key='date', freq=period))['amount'].sum()
        spending = spending.reset_index()
        
        if interactive:
            # Create interactive plotly line chart
            fig = px.line(
                spending,
                x='date',
                y='amount',
                title=title,
                labels={'date': 'Date', 'amount': 'Amount ($)'}
            )
            fig.update_traces(mode='lines+markers')
            fig.update_layout(hovermode='x unified')
            return fig
        else:
            # Create matplotlib line chart
            fig, ax = plt.subplots(figsize=(14, 6))
            ax.plot(spending['date'], spending['amount'], marker='o', linewidth=2)
            ax.set_xlabel('Date', fontsize=12)
            ax.set_ylabel('Amount ($)', fontsize=12)
            ax.set_title(title, fontsize=16, fontweight='bold')
            ax.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            return fig
    
    def create_category_bar_chart(self, top_n: int = 10,
                                   title: str = 'Top Spending Categories',
                                   interactive: bool = True):
        """
        Create bar chart for category spending
        
        Args:
            top_n: Number of top categories to show
            title: Chart title
            interactive: If True, create plotly chart; else matplotlib
            
        Returns:
            Plotly figure or matplotlib figure
        """
        if 'category' not in self.df.columns:
            raise ValueError("DataFrame must have 'category' column")
        
        # Aggregate by category
        spending = self.df.groupby('category')['amount'].sum().sort_values(ascending=False).head(top_n)
        
        if interactive:
            # Create interactive plotly bar chart
            fig = px.bar(
                x=spending.index,
                y=spending.values,
                title=title,
                labels={'x': 'Category', 'y': 'Amount ($)'},
                color=spending.values,
                color_continuous_scale='Viridis'
            )
            fig.update_layout(showlegend=False)
            return fig
        else:
            # Create matplotlib bar chart
            fig, ax = plt.subplots(figsize=(12, 6))
            colors = sns.color_palette('viridis', len(spending))
            ax.bar(spending.index, spending.values, color=colors)
            ax.set_xlabel('Category', fontsize=12)
            ax.set_ylabel('Amount ($)', fontsize=12)
            ax.set_title(title, fontsize=16, fontweight='bold')
            plt.xticks(rotation=45, ha='right')
            ax.grid(True, alpha=0.3, axis='y')
            plt.tight_layout()
            
            return fig
    
    def create_monthly_comparison(self, title: str = 'Monthly Spending Comparison',
                                   interactive: bool = True):
        """
        Create bar chart comparing monthly spending
        
        Args:
            title: Chart title
            interactive: If True, create plotly chart; else matplotlib
            
        Returns:
            Plotly figure or matplotlib figure
        """
        if 'date' not in self.df.columns:
            raise ValueError("DataFrame must have 'date' column")
        
        # Extract month and year
        self.df['month'] = self.df['date'].dt.to_period('M')
        
        # Aggregate by month
        monthly = self.df.groupby('month')['amount'].sum().reset_index()
        monthly['month'] = monthly['month'].astype(str)
        
        if interactive:
            # Create interactive plotly bar chart
            fig = px.bar(
                monthly,
                x='month',
                y='amount',
                title=title,
                labels={'month': 'Month', 'amount': 'Amount ($)'},
                color='amount',
                color_continuous_scale='Blues'
            )
            return fig
        else:
            # Create matplotlib bar chart
            fig, ax = plt.subplots(figsize=(14, 6))
            ax.bar(monthly['month'], monthly['amount'], color='steelblue')
            ax.set_xlabel('Month', fontsize=12)
            ax.set_ylabel('Amount ($)', fontsize=12)
            ax.set_title(title, fontsize=16, fontweight='bold')
            plt.xticks(rotation=45)
            ax.grid(True, alpha=0.3, axis='y')
            plt.tight_layout()
            
            return fig
    
    def create_top_merchants_chart(self, top_n: int = 10,
                                    title: str = 'Top Merchants by Spending',
                                    interactive: bool = True):
        """
        Create horizontal bar chart for top merchants
        
        Args:
            top_n: Number of top merchants to show
            title: Chart title
            interactive: If True, create plotly chart; else matplotlib
            
        Returns:
            Plotly figure or matplotlib figure
        """
        if 'merchant' not in self.df.columns:
            raise ValueError("DataFrame must have 'merchant' column")
        
        # Aggregate by merchant
        merchants = self.df.groupby('merchant')['amount'].sum().sort_values(ascending=False).head(top_n)
        
        if interactive:
            # Create interactive plotly horizontal bar chart
            fig = px.bar(
                x=merchants.values,
                y=merchants.index,
                orientation='h',
                title=title,
                labels={'x': 'Amount ($)', 'y': 'Merchant'},
                color=merchants.values,
                color_continuous_scale='Oranges'
            )
            fig.update_layout(yaxis={'categoryorder': 'total ascending'})
            return fig
        else:
            # Create matplotlib horizontal bar chart
            fig, ax = plt.subplots(figsize=(10, 8))
            colors = sns.color_palette('YlOrRd', len(merchants))
            ax.barh(merchants.index, merchants.values, color=colors)
            ax.set_xlabel('Amount ($)', fontsize=12)
            ax.set_ylabel('Merchant', fontsize=12)
            ax.set_title(title, fontsize=16, fontweight='bold')
            ax.grid(True, alpha=0.3, axis='x')
            plt.tight_layout()
            
            return fig
    
    def create_spending_heatmap(self, title: str = 'Spending Heatmap',
                                interactive: bool = True):
        """
        Create heatmap showing spending by category over months
        
        Args:
            title: Chart title
            interactive: If True, create plotly chart; else matplotlib
            
        Returns:
            Plotly figure or matplotlib figure
        """
        if 'category' not in self.df.columns or 'date' not in self.df.columns:
            raise ValueError("DataFrame must have 'category' and 'date' columns")
        
        # Create pivot table
        self.df['month'] = self.df['date'].dt.to_period('M')
        pivot = self.df.pivot_table(
            values='amount',
            index='category',
            columns='month',
            aggfunc='sum',
            fill_value=0
        )
        
        # Convert period to string for plotting
        pivot.columns = pivot.columns.astype(str)
        
        if interactive:
            # Create interactive plotly heatmap
            fig = px.imshow(
                pivot,
                title=title,
                labels=dict(x='Month', y='Category', color='Amount ($)'),
                aspect='auto',
                color_continuous_scale='YlOrRd'
            )
            return fig
        else:
            # Create matplotlib heatmap
            fig, ax = plt.subplots(figsize=(14, 8))
            sns.heatmap(pivot, annot=True, fmt='.0f', cmap='YlOrRd', ax=ax, cbar_kws={'label': 'Amount ($)'})
            ax.set_title(title, fontsize=16, fontweight='bold')
            plt.tight_layout()
            
            return fig
    
    def create_dashboard(self, output_path: Optional[str] = None):
        """
        Create comprehensive dashboard with multiple charts
        
        Args:
            output_path: Path to save dashboard image (optional)
            
        Returns:
            Matplotlib figure with subplots
        """
        fig = plt.figure(figsize=(18, 12))
        gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
        
        # 1. Pie chart - Spending by category
        if 'category' in self.df.columns:
            ax1 = fig.add_subplot(gs[0, 0])
            spending = self.df.groupby('category')['amount'].sum().sort_values(ascending=False).head(8)
            colors = sns.color_palette('Set2', len(spending))
            ax1.pie(spending.values, labels=spending.index, autopct='%1.1f%%', colors=colors)
            ax1.set_title('Spending by Category', fontweight='bold', fontsize=12)
        
        # 2. Line chart - Spending over time
        if 'date' in self.df.columns:
            ax2 = fig.add_subplot(gs[0, 1])
            monthly = self.df.groupby(pd.Grouper(key='date', freq='M'))['amount'].sum()
            ax2.plot(monthly.index, monthly.values, marker='o', linewidth=2, color='steelblue')
            ax2.set_title('Monthly Spending Trend', fontweight='bold', fontsize=12)
            ax2.set_xlabel('Date')
            ax2.set_ylabel('Amount ($)')
            ax2.grid(True, alpha=0.3)
            plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
        
        # 3. Bar chart - Top categories
        if 'category' in self.df.columns:
            ax3 = fig.add_subplot(gs[1, 0])
            top_cats = self.df.groupby('category')['amount'].sum().sort_values(ascending=False).head(6)
            ax3.bar(range(len(top_cats)), top_cats.values, color=sns.color_palette('viridis', len(top_cats)))
            ax3.set_xticks(range(len(top_cats)))
            ax3.set_xticklabels(top_cats.index, rotation=45, ha='right')
            ax3.set_title('Top Spending Categories', fontweight='bold', fontsize=12)
            ax3.set_ylabel('Amount ($)')
            ax3.grid(True, alpha=0.3, axis='y')
        
        # 4. Horizontal bar - Top merchants
        if 'merchant' in self.df.columns:
            ax4 = fig.add_subplot(gs[1, 1])
            top_merchants = self.df.groupby('merchant')['amount'].sum().sort_values(ascending=True).tail(6)
            ax4.barh(range(len(top_merchants)), top_merchants.values, color='coral')
            ax4.set_yticks(range(len(top_merchants)))
            ax4.set_yticklabels(top_merchants.index)
            ax4.set_title('Top Merchants', fontweight='bold', fontsize=12)
            ax4.set_xlabel('Amount ($)')
            ax4.grid(True, alpha=0.3, axis='x')
        
        # 5. Statistics text box
        ax5 = fig.add_subplot(gs[2, :])
        ax5.axis('off')
        
        stats_text = f"""
        📊 SPENDING SUMMARY
        ═══════════════════════════════════════════════════════════════
        
        Total Transactions: {len(self.df):,}
        Total Spent: ${self.df['amount'].sum():,.2f}
        Average Transaction: ${self.df['amount'].mean():,.2f}
        Largest Transaction: ${self.df['amount'].max():,.2f}
        Smallest Transaction: ${self.df['amount'].min():,.2f}
        """
        
        if 'category' in self.df.columns:
            top_cat = self.df.groupby('category')['amount'].sum().idxmax()
            top_cat_amt = self.df.groupby('category')['amount'].sum().max()
            stats_text += f"\nTop Category: {top_cat} (${top_cat_amt:,.2f})"
        
        if 'merchant' in self.df.columns:
            top_merch = self.df.groupby('merchant')['amount'].sum().idxmax()
            top_merch_amt = self.df.groupby('merchant')['amount'].sum().max()
            stats_text += f"\nTop Merchant: {top_merch} (${top_merch_amt:,.2f})"
        
        ax5.text(0.1, 0.5, stats_text, fontsize=11, family='monospace',
                verticalalignment='center', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
        
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
        
        return fig


def create_spending_charts(df: pd.DataFrame, interactive: bool = True) -> dict:
    """
    Create all standard spending charts
    
    Args:
        df: DataFrame with transaction data
        interactive: If True, create plotly charts; else matplotlib
        
    Returns:
        Dictionary of chart figures
    """
    visualizer = SpendingVisualizer(df)
    
    charts = {}
    
    if 'category' in df.columns:
        charts['pie_chart'] = visualizer.create_pie_chart(interactive=interactive)
        charts['category_bar'] = visualizer.create_category_bar_chart(interactive=interactive)
    
    if 'date' in df.columns:
        charts['time_series'] = visualizer.create_spending_over_time(interactive=interactive)
        charts['monthly_comparison'] = visualizer.create_monthly_comparison(interactive=interactive)
    
    if 'merchant' in df.columns:
        charts['top_merchants'] = visualizer.create_top_merchants_chart(interactive=interactive)
    
    return charts


if __name__ == "__main__":
    # Test the module
    print("Spending Visualizer Module")
    print("=" * 50)
    print("\nUsage:")
    print("  from visualizer import create_spending_charts")
    print("  charts = create_spending_charts(df, interactive=True)")
