import yfinance as yf
import pandas as pd
from datetime import datetime
import lxml
from lxml import html
import requests
import numpy as np


def get_df(symbol, typeOfDf):

    url = 'https://finance.yahoo.com/quote/' + symbol + '/'+typeOfDf+'?p=' + symbol

    # Set up the request headers that we're going to use, to simulate
    # a request by the Chrome browser. Simulating a request from a browser
    # is generally good practice when building a scraper
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'max-age=0',
        'Pragma': 'no-cache',
        'Referrer': 'https://google.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
    }

    # Fetch the page that we're going to parse, using the request headers
    # defined above
    page = requests.get(url, headers)

    # Parse the page with LXML, so that we can start doing some XPATH queries
    # to extract the data that we want
    tree = html.fromstring(page.content)

    # Smoke test that we fetched the page by fetching and displaying the H1 element
    tree.xpath("//h1/text()")

    table_rows = tree.xpath("//div[contains(@class, 'D(tbr)')]")

    # Ensure that some table rows are found; if none are found, then it's possible
    # that Yahoo Finance has changed their page layout, or have detected
    # that you're scraping the page.
    assert len(table_rows) > 0

    parsed_rows = []

    for table_row in table_rows:
        parsed_row = []
        el = table_row.xpath("./div")

        none_count = 0

        for rs in el:
            try:
                (text,) = rs.xpath('.//span/text()[1]')
                parsed_row.append(text)
            except ValueError:
                parsed_row.append(np.NaN)
                none_count += 1

        if (none_count < 4):
            parsed_rows.append(parsed_row)

    df = pd.DataFrame(parsed_rows)
    df

    df = pd.DataFrame(parsed_rows)
    df = df.set_index(0)  # Set the index to the first column: 'Period Ending'.
    df = df.transpose()  # Transpose the DataFrame, so that our header contains the account names

    # Rename the "Breakdown" column to "Date"
    cols = list(df.columns)
    cols[0] = 'Date'
    df = df.set_axis(cols, axis='columns', inplace=False)

    return df

# converts a list of characters to a string without any commas

def convert_to_float(s):
    # initialization of string to ""
    new = ""

    # traverse in the string
    for x in s:
        if x == ',':
            continue
        new += x

        # return string
    return float(new)

def convert_to_string(s):
    # initialization of string to ""
    new = ""

    # traverse in the string
    for x in s:
        new += x

        # return string
    return new



def get_return_on_capital(companyObject):
    return companyObject.gross_profit/(companyObject.assets-companyObject.liabilities)


def get_earnings_yield(companyObject):
    return companyObject.eps/companyObject.stock_price