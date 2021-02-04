import functions as f
import yfinance as yf
import classes as classes
import pandas as pd
from datetime import datetime
import lxml
from lxml import html
import requests
import numpy as np

table = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
sandp_raw = df = table[0]
sandp_symbols = sandp_raw["Symbol"]

company_data_output = {"Company name": [], "Return on capital": [], "Earnings yield": []}

for i in range(1, 100):
    symbol = f.convert_to_string(sandp_symbols.iloc[i])



    ticker = yf.Ticker(symbol)

    name = ticker.info["longName"]
    # contains total assets and total liabilities
    df_balance_sheet = f.get_df(symbol, 'balance-sheet')
    # contains Gross Profits
    df_financials = f.get_df(symbol, 'financials')
    # getting company stock price and eps
    containsColumns = ("Gross Profit" in df_financials.columns and "Total Assets" in df_balance_sheet.columns
                 and "Total Liabilities Net Minority Interest" in df_balance_sheet)

    if containsColumns:
        gross_profit_df = df_financials["Gross Profit"].head(1)

        total_assets_df = df_balance_sheet["Total Assets"].head(1)
        total_liabilities_df = df_balance_sheet["Total Liabilities Net Minority Interest"].head(1)

        gross_profit_as_xml = gross_profit_df.iloc[0]
        total_assets_as_xml = total_assets_df.iloc[0]
        total_liabilities_as_xml = total_liabilities_df.iloc[0]

        gross_profit = f.convert_to_float([str(s) for s in gross_profit_as_xml]) * 1000
        total_assets = f.convert_to_float([str(s) for s in total_assets_as_xml]) * 1000
        total_liabilities = f.convert_to_float([str(s) for s in total_liabilities_as_xml]) * 1000
        stock_price = ticker.info["regularMarketPreviousClose"]
        eps = ticker.info["trailingEps"]

        companyObject = classes.Company(name=name, symbol=symbol, assets=total_assets, eps=eps,
                                        gross_profit=gross_profit, stock_price=stock_price,
                                        liabilities=total_liabilities)

        roc = f.get_return_on_capital(companyObject)

        ey = f.get_earnings_yield(companyObject)

        company_data_output["Company name"].insert(len(company_data_output["Company name"]), name)
        company_data_output["Return on capital"].insert(len(company_data_output["Return on capital"]), roc)
        company_data_output["Earnings yield"].insert(len(company_data_output["Earnings yield"]), ey)

        print(f"Company name: {name}")
        print(f'Gross profit: {gross_profit}')
        print(f"Total assets: {total_assets}")
        print(f"Total liabilities: {total_liabilities}")
        print(f'return on capital: {roc}')
        print(f'earnings yield: {ey}')
        print(f'EPS: {eps}')
        print(f'Stock price: {stock_price}')




    # get stock info
    ''''''

print(company_data_output)

companies_df = pd.DataFrame(data=company_data_output)

print(companies_df)

writer = pd.ExcelWriter('S&P 500 Companies.xlsx')

companies_df.to_excel(writer)

writer.save()

print("Sucess!")


