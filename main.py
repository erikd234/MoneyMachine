import functions as f
import yfinance as yf
import classes as classes
import pandas as pd
from datetime import datetime
import lxml
from lxml import html
import requests
import numpy as np



symbol = 'AAPL'

aapl = yf.Ticker(symbol)

name = aapl.info["longName"]
# contains total assets and total liabilities
df_balance_sheet = f.get_df(symbol, 'balance-sheet')
# contains Gross Profits
df_financials = f.get_df(symbol, 'financials')
# getting company stock price and eps

gross_profit_df = df_financials["Gross Profit"].head(1)
total_assets_df = df_balance_sheet["Total Assets"].head(1)
total_liabilities_df = df_balance_sheet["Total Liabilities Net Minority Interest"].head(1)

gross_profit_as_xml = gross_profit_df.iloc[0]
total_assets_as_xml = total_assets_df.iloc[0]
total_liabilities_as_xml = total_liabilities_df.iloc[0]

gross_profit = f.convert([str(s) for s in gross_profit_as_xml]) * 1000
total_assets = f.convert([str(s) for s in total_assets_as_xml]) * 1000
total_liabilities = f.convert([str(s) for s in total_liabilities_as_xml]) * 1000

print(f'Gross profit: {gross_profit}')
print(f"Total assets: {total_assets}")
print(f"Total liabilities: {total_liabilities}")

stock_price = aapl.info["regularMarketPreviousClose"]
eps = aapl.info["trailingEps"]
# get stock info
print(f'EPS: {eps}')
print(f'Stock price: {stock_price}')

Apple = classes.Company(name=name, symbol=symbol, assets=total_assets, eps=eps,
                        gross_profit=gross_profit, stock_price=stock_price, liabilities=total_liabilities)

roc = f.get_return_on_capital(Apple)

ey = f.get_earnings_yield(Apple)

print(f'return on capital: {roc}')
print(f'earnings yield: {ey}')















'''

writer = pd.ExcelWriter('balance-sheet.xlsx')

df_balance_sheet.to_excel(writer)

writer.save()

writer = pd.ExcelWriter('financials.xlsx')

df_financials.to_excel(writer)

writer.save()
print("Sucess!")


aapl = yf.Ticker("AAPL")

# get stock info
print(aapl.info)'''