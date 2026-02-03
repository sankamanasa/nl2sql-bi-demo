
"""
NL2SQL Demo - Natural Language to SQL for Financial Analytics
"""

import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from typing import Tuple


class NL2SQLDemo:
    """
    Natural Language to SQL converter for stock market data analysis.
    """
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.query_history = []
        
    def generate_sql(self, natural_query: str) -> Tuple[str, str]:
        """Convert natural language question to SQL query."""
        q = natural_query.lower()
        
        # Moving averages
        if 'moving average' in q or 'trend' in q:
            ticker = self._extract_ticker(q)
            sql = f"""
                SELECT date, close,
                    AVG(close) OVER (ORDER BY date ROWS 6 PRECEDING) as ma_7,
                    AVG(close) OVER (ORDER BY date ROWS 29 PRECEDING) as ma_30
                FROM stock_prices 
                WHERE ticker = '{ticker}' 
                ORDER BY date
            """.strip()
            return sql, f"7-day and 30-day moving averages for {ticker}"
        
        # Daily returns
        if 'return' in q or 'daily change' in q:
            sql = """
                SELECT ticker, date, close,
                    ROUND((close - LAG(close) OVER (PARTITION BY ticker ORDER BY date)) / 
                          LAG(close) OVER (PARTITION BY ticker ORDER BY date) * 100, 2) as return_pct
                FROM stock_prices 
                ORDER BY date DESC 
                LIMIT 30
            """.strip()
            return sql, "Daily returns for all stocks"
        
        # Risk metrics
        if 'risk' in q or 'drawdown' in q or 'worst' in q:
            sql = """
                WITH daily_returns AS (
                    SELECT ticker, 
                        (close - LAG(close) OVER (PARTITION BY ticker ORDER BY date)) / 
                        LAG(close) OVER (PARTITION BY ticker ORDER BY date) as ret
                    FROM stock_prices
                )
                SELECT ticker,
                    ROUND(MIN(ret)*100, 2) as worst_day_pct,
                    ROUND(AVG(CASE WHEN ret<0 THEN ret END)*100, 2) as avg_loss_pct,
                    ROUND(COUNT(CASE WHEN ret<0 THEN 1 END)*100.0/COUNT(*), 1) as down_days_pct
                FROM daily_returns 
                WHERE ret IS NOT NULL 
                GROUP BY ticker
            """.strip()
            return sql, "Risk metrics: worst day, avg loss, down day frequency"
        
        # Volatility
        if 'volatile' in q or 'volatility' in q:
            sql = """
                SELECT ticker, 
                    ROUND(AVG((high-low)/close*100), 2) as avg_volatility_pct
                FROM stock_prices 
                GROUP BY ticker 
                ORDER BY avg_volatility_pct DESC
            """.strip()
            return sql, "Average daily volatility by stock"
        
        # Average price
        if 'average' in q or 'avg' in q:
            ticker = self._extract_ticker(q)
            if ticker:
                sql = f"SELECT AVG(close) as avg_price FROM stock_prices WHERE ticker = '{ticker}'"
                return sql, f"Average closing price for {ticker}"
            else:
                sql = "SELECT ticker, AVG(close) as avg_price FROM stock_prices GROUP BY ticker"
                return sql, "Average closing price for all stocks"
        
        # Recent data
        if 'latest' in q or 'recent' in q:
            return "SELECT * FROM stock_prices ORDER BY date DESC LIMIT 10", "Most recent 10 trading days"
        
        # Default fallback
        return "SELECT * FROM stock_prices LIMIT 5", "Sample data"
    
    def _extract_ticker(self, query: str) -> str:
        """Extract stock ticker from natural language query."""
        q = query.lower()
        if 'apple' in q or 'aapl' in q:
            return 'AAPL'
        elif 'microsoft' in q or 'msft' in q:
            return 'MSFT'
        elif 'nvidia' in q or 'nvda' in q:
            return 'NVDA'
        return 'AAPL'
    
    def execute(self, sql: str) -> pd.DataFrame:
        """Execute SQL query and return results as DataFrame."""
        conn = sqlite3.connect(self.db_path)
        try:
            result = pd.read_sql(sql, conn)
            return result
        finally:
            conn.close()
    
    def ask(self, question: str, show_viz: bool = True) -> pd.DataFrame:
        """Main interface: Ask a natural language question, get results."""
        print(f"\n🗣️  QUESTION: {question}")
        print("-" * 70)
        
        sql, explanation = self.generate_sql(question)
        print(f"🤖 GENERATED SQL:\n{sql}")
        print(f"\n💡 Explanation: {explanation}")
        print("-" * 70)
        
        result = self.execute(sql)
        print(f"📊 RESULTS ({len(result)} rows):")
        print(result.to_string(index=False))
        
        self.query_history.append({
            'question': question,
            'sql': sql,
            'rows': len(result)
        })
        
        if show_viz and len(result) > 0:
            self.visualize(question, result)
        
        return result
    
    def visualize(self, question: str, result: pd.DataFrame) -> None:
        """Auto-generate appropriate visualization based on query results."""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        if 'date' in result.columns and len(result) > 5:
            
            result['date'] = pd.to_datetime(result['date'], utc=True).dt.tz_localize(None)
              
            if 'ma_7' in result.columns:
                ax.plot(result['date'], result['close'], label='Close', alpha=0.7, color='gray')
                ax.plot(result['date'], result['ma_7'], label='7-day MA', linewidth=2)
                ax.plot(result['date'], result['ma_30'], label='30-day MA', linewidth=2)
                ax.set_title('Moving Average Analysis', fontsize=14, fontweight='bold')
                ax.legend()
            
            elif 'return_pct' in result.columns:
                colors = ['green' if x > 0 else 'red' for x in result['return_pct']]
                ax.bar(range(len(result)), result['return_pct'], color=colors, alpha=0.7)
                ax.set_title('Daily Returns (%)', fontsize=14, fontweight='bold')
                ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
            
            else:
                for ticker in result['ticker'].unique() if 'ticker' in result.columns else ['Price']:
                    data = result[result['ticker'] == ticker] if 'ticker' in result.columns else result
                    ax.plot(data['date'], data['close'], label=ticker, linewidth=2)
                ax.set_title('Stock Price Trends', fontsize=14, fontweight='bold')
                ax.legend()
            
            ax.set_xlabel('Date')
            ax.set_ylabel('Price ($)')
            ax.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
        
        elif 'ticker' in result.columns and len(result) <= 5:
            metrics = [c for c in result.columns if c != 'ticker']
            if metrics:
                result.plot(x='ticker', kind='bar', ax=ax)
                ax.set_title('Stock Comparison', fontsize=14, fontweight='bold')
                ax.legend()
                ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig('images/latest_viz.png', dpi=150, bbox_inches='tight')
        plt.show()
        print("\n📈 Visualization saved to images/latest_viz.png")


if __name__ == "__main__":
    demo = NL2SQLDemo('data/stock_database.db')
    demo.ask("What is the average price of Apple stock?")