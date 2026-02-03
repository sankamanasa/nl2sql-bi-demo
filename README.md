# 🧠 LLM-Powered Business Intelligence (NL2SQL)

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

&gt; **Natural Language to SQL system for financial analytics** - Ask questions about stock data in plain English, get insights instantly.

## 🎯 Project Overview

This project demonstrates how Large Language Models (LLMs) can democratize data access by converting natural language questions into executable SQL queries. Built with real stock market data (AAPL, MSFT, NVDA), it showcases the future of self-service business intelligence.

### Key Features

- 🗣️ **Natural Language Interface** - Ask questions like *"What's Apple's average closing price?"*
- 🤖 **Intelligent SQL Generation** - Pattern recognition + LLM-ready architecture
- 📊 **Auto-Visualization** - Charts generated based on query intent
- 📈 **Real Financial Data** - 1 year of daily stock prices from Yahoo Finance

## 🚀 Quick Start

### Prerequisites

# Clone the repository
git clone https://github.com/YOUR_USERNAME/nl2sql-bi-demo.git
cd nl2sql-bi-demo

# Install dependencies
pip install -r requirements.txt

Usage

from src.nl2sql import NL2SQLDemo

# Initialize demo
demo = NL2SQLDemo('data/stock_database.db')

# Ask natural language questions
result = demo.ask("Show me moving averages for Apple")
result = demo.ask("Which stock is most volatile?")

📈 Sample Queries

| Natural Language Query          | Generated SQL                                             |
| ------------------------------- | --------------------------------------------------------- |
| "Average price of Apple stock"  | SELECT AVG(close) FROM stock_prices WHERE ticker='AAPL' |
| "Show me 7-day moving averages" | Window functions with `ROWS BETWEEN                      |
| "Which stock is most volatile?" | AVG((high-low)/close*100)                               |


🛠️ Technologies
Python 3.8+, SQLite, Pandas, Matplotlib, Jupyter

📝 License
MIT License