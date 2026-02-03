from src.nl2sql import NL2SQLDemo

demo = NL2SQLDemo('data/stock_database.db')

print("="*60)
print("🧠 NL2SQL BI DEMO")
print("="*60)

print("\n1️⃣ Average Price Query:")
demo.ask("What is the average price of Apple stock?",show_viz=False)

print("\n2️⃣ Moving Averages Query:")
demo.ask("Show me the 7-day and 30-day moving averages for Apple", show_viz=False)

print("\n3️⃣ Volatility Query:")
demo.ask("Which stock is most volatile?")

print("\n4️⃣ Risk Metrics Query:")
demo.ask("Show me risk metrics for all stocks")

print("\n5️⃣ Daily Returns Query:")
demo.ask("What are the daily returns for the last 30 days?")

print("\n" + "="*60)
print("✅ Demo complete! Check images/ folder for charts.")
print("="*60)