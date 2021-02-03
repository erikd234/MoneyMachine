import functions as f
import yfinance as yf
import pandas as pd
from datetime import datetime
import lxml
from lxml import html
import requests
import numpy as np



# user puts in the symbol for the company and the what data they
# want to web scrape from yahoo, either cash-flow, financials, or balance Sheet
# the program returns a data frame with the information.




# contains total assets and total liabilities
df_balance_sheet = f.get_df('AAPL', 'balance-sheet')
# contains Gross Profits
df_financials = f.get_df('AAPL', 'financials')

gross_profit_df = df_financials["Gross Profit"].head(1)
total_assets_df = df_balance_sheet["Total Assets"].head(1)
total_liabilities_df = df_balance_sheet["Total Liabilities Net Minority Interest"].head(1)



gross_profit_as_xml = gross_profit_df.iloc[0]
total_assets_as_xml = total_assets_df.iloc[0]
total_liabilities_as_xml = total_liabilities_df.iloc[0]

gross_profit = float(f.convert([str(s) for s in gross_profit_as_xml]))
total_assets = float(f.convert([str(s) for s in total_assets_as_xml]))
total_liabilities = float(f.convert([str(s) for s in total_liabilities_as_xml]))



print(type(gross_profit))
print(f'Gross profit: {gross_profit}')
print(f"Total assets: {total_assets}")
print(f"Total liabilities: {total_liabilities}")


aapl = yf.Ticker("AAPL")

# get stock info
print(f'EPS: {aapl.info["trailingEps"]}')
print(f'Stock price: {aapl.info["regularMarketPreviousClose"]}')



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