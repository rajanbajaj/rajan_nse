import numpy as np
import pandas as pd
from datetime import date
from rajan_nse.NseData import NseData
from rajan_nse.Session import Session
from rajan_nse.Visualization import Visualization
from sklearn.linear_model import LinearRegression

class TechnicalIndicators:
    def __init__(self) -> None:
        """This class contains methods to calculate values of stocks technical indicators."""
        self.session = Session("https://www.nseindia.com")
        self.nseData = NseData()
        self.visualize = Visualization()
        pass

    def sma(self, symbol=None, period=200, data=None):
        """This method is used to calculate simple moving average of stocks based on daily timeframe.

        Keyword arguments:
        symbol -- Stock symbol listed on NSE
        period -- The period for which SMA should be calculated (default = 200)
        data -- Historical data of a stock (default = None i.e. historical value will be fetched)

        Returns:
        integer value of calculated SMA
        -1 if there is an error in calculation
        """
        if data is None:
            data = self.nseData.getHistoricalData(symbol)['data']

        try:
            sum = 0
            data_length = len(data)
            if (period < data_length):
                for i in range(0, period):
                    sum += data[i]['CH_CLOSING_PRICE']
                return sum / period
            else:
                for tmp in data:
                    sum += tmp['CH_CLOSING_PRICE']
                return sum / len(data)
        except:
            return -1

    def rsi(self, symbol, period = 14):
        """This method is used to calculate relative strength index (rsi) of stocks based on daily timeframe.

        Keyword arguments:
        symbol -- Stock symbol listed on NSE
        period -- The period for which SMA should be calculated (default = 14)

        Returns:
        integer value of calculated RSI
        """
        data = self.nseData.getHistoricalData(symbol)['data']

        assert len(data) >= 14, "Insufficient data: Need at least 14 rows"

        prices = [day['CH_CLOSING_PRICE'] for day in data[:14]]

        # Calculate price changes
        price_changes = np.diff(prices)
        
        # Separate gains and losses
        gains = np.maximum(price_changes, 0)
        losses = np.abs(np.minimum(price_changes, 0))
        
        # # Calculate the average gains and losses
        avg_gain = self.sma(data=gains, period=period)
        avg_loss = self.sma(data=losses, period=period)
        
        # # Calculate the Relative Strength (RS)
        rs = avg_gain / avg_loss
        
        # # Calculate the RSI
        rsi = 100 - (100 / (1 + rs))
        
        # # Adjust the length of RSI to match the input prices length
        # # The first (period-1) RSI values are NaN since we don't have enough data points to calculate them
        # rsi = np.concatenate((np.full(period-1, np.nan), rsi))
        
        return rsi
    
    def cmf(self, symbol, period = 21):
        """
        Chaikin Money Flow (CMF) developed by Marc Chaikin is a volume-weighted
        average of accumulation and distribution over a specified period. The standard
        CMF period is 21 days. The principle behind the Chaikin Money Flow is the nearer
        the closing price is to the high, the more accumulation has taken place.
        Conversely, the nearer the closing price is to the low, the more distribution
        has taken place. If the price action consistently closes above the bar's midpoint
        on increasing volume, the Chaikin Money Flow will be positive. Conversely, if the
        price action consistently closes below the bar's midpoint on increasing volume, the
        Chaikin Money Flow will be a negative value.
        Calculations:
        CMF = n-day Sum of [(((C - L) - (H - C)) / (H - L)) x Vol] / n-day Sum of Vol
        Where: n = number of periods, typically 21 H = high L = low C = close Vol = volume

        Keyword Arguments:
        symbol -- Stock symbol listed on NSE
        period -- The period for which SMA should be calculated (default = 21)
        """
        data = self.nseData.getHistoricalData(symbol)['data']

        sum_a = 0
        sum_b = 0
        data_length = len(data)
        if (period < data_length):
            for i in range(0, period):
                sum_a += (((data[i]['CH_CLOSING_PRICE'] - data[i]['CH_TRADE_LOW_PRICE'] ) - (data[i]['CH_TRADE_HIGH_PRICE']  - data[i]['CH_CLOSING_PRICE'] )) / (data[i]['CH_TRADE_HIGH_PRICE']  - data[i]['CH_TRADE_LOW_PRICE'] )) * data[i]['CH_TOT_TRADED_QTY']
                sum_b += data[i]['CH_TOT_TRADED_QTY']
        else:
            for tmp in data:
                sum_a += (((tmp['CH_CLOSING_PRICE'] - tmp['CH_TRADE_LOW_PRICE'] ) - (tmp['CH_TRADE_HIGH_PRICE']  - tmp['CH_CLOSING_PRICE'] )) / (tmp['CH_TRADE_HIGH_PRICE']  - tmp['CH_TRADE_LOW_PRICE'] )) * tmp['CH_TOT_TRADED_QTY'] 
                sum_b += tmp['CH_TOT_TRADED_QTY']
        return sum_a / sum_b

    # delta is percentage range of price from 52 weeks high
    def near52WeekHigh(self, symbol, live=False, delta=5):
        """This method is used to return a boolean if the stock is near 52 Week high value for a NSE stock.

        Keyword arguments:
        symbol -- Stock symbol listed on NSE website
        live -- Boolean to get current running price value or previous day value
        delta -- The delta as percentage to check if stock is in +- that range of high(default = 5 percentage)
        """
        # data = {high:, low:, price:}
        data = self.nseData.fiftyTwoWeekHighLow(symbol, live)
        return (abs(data['high'] - data['price']) / data['high']) * 100 <= delta
    
    # delta is percentage range of price from 52 weeks low
    def near52WeekLow(self, symbol, live=False, delta=5):
        """This method is used to return a boolean if the stock is near 52 Week low value for a NSE stock.

        Keyword arguments:
        symbol -- Stock symbol listed on NSE website
        live -- Boolean to get current running price value or previous day value
        delta -- The delta as percentage to check if stock is in +- that range of low(default = 5 percentage)
        """
        # data = {high:, low:, price:}
        data = self.nseData.fiftyTwoWeekHighLow(symbol, live)
        return (abs(data['low'] - data['price']) / data['low']) * 100 <= delta

    def trendLine(self, symbol, delta=200, lower_percentile=40, upper_percentile=98, to_date = date.today()):
        """This method returns the series of price values that creates a trend line both upper and lower.

        Keyword arguments:
        symbol -- Stock symbol listed on NSE website
        delta -- Check trend for these number of historical days
        low_percentile -- Percentile value above which the traded qty. (volume) should be (default value = 40)
        upper_percentile -- Percentile value below which the traded qty. (volume) should be (default value = 98)
        to_date -- date till which the trend line should be

        Returns:
        returns a dataframe for lower trendline and upper trendline values list
        """
        df = pd.DataFrame(self.nseData.getHistoricalData(symbol, delta, to_date)['data'])
        df['CH_TIMESTAMP'] = pd.to_datetime(df['CH_TIMESTAMP'])
        df.set_index('CH_TIMESTAMP', inplace=True)
        df.sort_index(inplace=True)

        lower_bound = np.percentile(df['CH_TOT_TRADED_QTY'], lower_percentile)
        upper_bound = np.percentile(df['CH_TOT_TRADED_QTY'], upper_percentile)

        # Select data points outside the lower and upper bounds
        df = df[(df['CH_TOT_TRADED_QTY'] > lower_bound) & (df['CH_TOT_TRADED_QTY'] < upper_bound)]

        df['CH_TRADE_HIGH_PRICE_MAX'] = df['CH_TRADE_HIGH_PRICE'][(df['CH_TRADE_HIGH_PRICE'] == df['CH_TRADE_HIGH_PRICE'].rolling(window=1, center=True).max())]
        df['CH_TRADE_LOW_PRICE_MIN'] = df['CH_TRADE_LOW_PRICE'][(df['CH_TRADE_LOW_PRICE'] == df['CH_TRADE_LOW_PRICE'].rolling(window=1, center=True).min())]

        peaks = df.dropna(subset=['CH_TRADE_HIGH_PRICE_MAX'])
        troughs = df.dropna(subset=['CH_TRADE_LOW_PRICE_MIN'])
        
        # Upper trend line (peaks)
        X_peaks = np.array((peaks.index - peaks.index[0]).days).reshape(-1, 1)
        y_peaks = peaks['CH_TRADE_HIGH_PRICE_MAX'].values
        model_peaks = LinearRegression().fit(X_peaks, y_peaks)
        slope_peaks = model_peaks.coef_[0]
        intercept_peaks = model_peaks.intercept_

        # Lower trend line (troughs)
        X_troughs = np.array((troughs.index - troughs.index[0]).days).reshape(-1, 1)
        y_troughs = troughs['CH_TRADE_LOW_PRICE_MIN'].values
        model_troughs = LinearRegression().fit(X_troughs, y_troughs)
        slope_troughs = model_troughs.coef_[0]
        intercept_troughs = model_troughs.intercept_

        # Generate trend lines
        df['UPPER_TREND_LINE'] = intercept_peaks + slope_peaks * np.array((df.index - df.index[0]).days)
        df['LOWER_TREND_LINE'] = intercept_troughs + slope_troughs * np.array((df.index - df.index[0]).days)

        return df