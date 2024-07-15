from datetime import date, timedelta
from pandas import DataFrame, to_numeric
from time import sleep
from tqdm import tqdm
from alive_progress import alive_bar
from rajan_nse.Session import Session

def isPromoterFilterPassed(session: Session, symbol):
    try:
        data = session.makeRequest(
            url = "https://www.nseindia.com/api/corp-info",
            params = {
                'market': 'equities',
                'corpType': 'promoterenc',
                'symbol': symbol
            }
        )
        return float(data[0]['per1']) > 50 and float(data[0]['per2']) == 0 and float(data[0]['per3']) == 0.00
    except:
        print('promoter', symbol, data)

def isSastRegulationFilterPassed(session: Session, symbol):
    try:
        data = session.makeRequest(
            url = "https://www.nseindia.com/api/corp-info",
            params = {
                'market': 'equities',
                'corpType': 'sast',
                'symbol': symbol
            }
        )
        sast_df = DataFrame(data)

        if sast_df.empty:
            return True

        sast_df['noOfShareSale'] = to_numeric(sast_df['noOfShareSale'])
        sast_df = sast_df['noOfShareSale'].replace('-', 0)
        return sast_df.sum() == 0
    except: 
        print('sast', symbol)

def findAvgPrice(session: Session, to_date_formated, from_date_formated, symbol):
    try:
        # https://www.nseindia.com/api/corporates-pit?index=equities&from_date=25-03-2024&to_date=25-06-2024&symbol=BAJFINANCE
        data = session.makeRequest(
            url = "https://www.nseindia.com/api/corporates-pit",
            params = {
                'index': 'equities',
                'from_date': from_date_formated,
                'to_date': to_date_formated,
                'symbol': symbol
            }
        )
        
        df = DataFrame(data["data"])
        filter = (df['personCategory'] == 'Promoters') | (df['personCategory'] == 'Promoter Group')
        df = df.where(filter)

        filter = df['secType'] == 'Equity Shares'
        df = df.where(filter)

        avg_price = -1
        if (df.where(df['tdpTransactionType'] == 'Sell').dropna().size == 0):
            filter = df['tdpTransactionType'] == 'Buy'
            df = df.where(filter)

            df['secVal'] = to_numeric(df['secVal'])
            df['secAcq'] = to_numeric(df['secAcq'])
            value = df['secVal'].sum()
            qty = df['secAcq'].sum()
            if qty != 0:
                avg_price = value / qty
        

        return avg_price
    except:
        print('average', symbol)
        return -1

def lastPrice(session: Session,symbol):
    # https://www.nseindia.com/api/quote-equity?symbol=360ONE
    # get quote details

    data = session.makeRequest(
        url = "https://www.nseindia.com/api/quote-equity",
        params = {
            'symbol': symbol,
        }
    )
    price_info = data['priceInfo']
    industry_info = data['industryInfo']
    pre_open_info = data['preOpenMarket']
    last_price = price_info['lastPrice']

    return last_price 

def getInsiderTradingData(session: Session, to_date_formated, from_date_formated): 
    data = session.makeRequest(
        url="https://www.nseindia.com/api/corporates-pit",
        params= {
            'index': 'equities',
            'from_date': from_date_formated,
            'to_date': to_date_formated
        }
    )

    df = DataFrame(data["data"])
    return df

def filterStocksBasedOnValueThreshold(session: Session, to_date_formated, from_date_formated, threshold=10000000): 

    df = getInsiderTradingData(session, to_date_formated=to_date_formated, from_date_formated=from_date_formated)
    df = df[['symbol', 'secVal']]
    df['symbol'] = df['symbol'].replace(' ', '')
    df['secVal'] = df['secVal'].replace('-', 0)
    df['secVal'] = to_numeric(df['secVal'])

    df = df.groupby('symbol').sum()
    df.sort_values('secVal', inplace=True)

    filter = df["secVal"] > threshold
    df.where(filter, inplace=True)

    df.sort_values('secVal', inplace=True)
    df = df.dropna()

    filtered_stock_symbols = df['secVal'].keys()
    df['secVal'].to_csv('stocks_' + to_date_formated + '.tmp.csv')
    return filtered_stock_symbols

def filterStocksBasedOnPromoterAndSast(session: Session, to_date_formated, from_date_formated):
    # pledge details
    # https://www.nseindia.com/api/corp-info?symbol=360ONE&corpType=promoterenc&market=equities
    #
    # check sast regulation data
    # https://www.nseindia.com/api/corp-info?symbol=360ONE&corpType=sast&market=equities
    stocks = []
    failed = []
    filtered_stock_symbols = filterStocksBasedOnValueThreshold(session, to_date_formated, from_date_formated)
    with alive_bar(filtered_stock_symbols.size, force_tty=True) as bar:
        for symbol in filtered_stock_symbols:
            if(isPromoterFilterPassed(session, symbol) and isSastRegulationFilterPassed(session, symbol)):
                stocks.append(symbol)
            bar()
    return stocks

def filterBasedOnPromoterBuyBackStrategy(session: Session, to_date_formated, from_date_formated ,allowed_diff = 0.05):
    final = []
    stocks = filterStocksBasedOnPromoterAndSast(session, to_date_formated, from_date_formated)
    with alive_bar(len(stocks), force_tty=True) as bar:
        for symbol in stocks:
            avg_price = findAvgPrice(session, to_date_formated, from_date_formated, symbol)
            last_price = lastPrice(session, symbol)
            diff = (last_price - avg_price) / abs(avg_price)
            if avg_price != -1 and diff < allowed_diff:
                final.append([symbol, avg_price, last_price])
            bar()
    return final
