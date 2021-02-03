
class Company:
    def __init__(self, name, symbol, assets, eps, gross_profit, stock_price, total_liabilities):
        self.name = name
        self.symbol = symbol
        self.gross_profit = gross_profit
        self.assets = assets
        self.total_liabilities = total_liabilities
        self.eps = eps
        self.stock_price = stock_price


Apple = Company("Apple", symbol="AAPL", assets="1000000", eps="3.9", gross_profit='1000203123123', stock_price="124", total_liabilities="8000000")

print(Apple.total_liabilities)

print(Apple.name)