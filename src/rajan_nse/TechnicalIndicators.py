import numpy as np
from datetime import date, timedelta
from rajan_nse.NseData import NseData
from rajan_nse.Session import Session

class TechnicalIndicators:
    def __init__(self) -> None:
        self.session = Session("https://www.nseindia.com")
        self.nseData = NseData()
        pass

    def sma(self, symbol=None, period=200, data=None):
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
    """
    def cmf(self, symbol, period = 21):
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
        # data = {high:, low:, price:}
        data = self.nseData.fiftyTwoWeekHighLow(symbol, live)
        return (abs(data['high'] - data['price']) / data['high']) * 100 <= delta
    
    # delta is percentage range of price from 52 weeks low
    def near52WeekLow(self, symbol, live=False, delta=5):
        # data = {high:, low:, price:}
        data = self.nseData.fiftyTwoWeekHighLow(symbol, live)
        return (abs(data['low'] - data['price']) / data['low']) * 100 <= delta
