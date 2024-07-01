from rajan_nse.Session import Session
from datetime import date, timedelta
import numpy as np

class CandleStickPatterns:
    def __init__(self) -> None:
        self.session = Session("https://www.nseindia.com")
        pass

    def sma(self, data, delta=200):
        try:
            sum = 0
            for tmp in data:
                sum += tmp['CH_CLOSING_PRICE']
            return sum / len(data['data'])
        except:
            return -1

    def rsi(self, data, period = 14):
        assert len(data) >= 14, "Insufficient data: Need at least 14 rows"

        prices = [day['CH_CLOSING_PRICE'] for day in data[:14]]

        # Calculate price changes
        price_changes = np.diff(prices)
        
        # Separate gains and losses
        gains = np.maximum(price_changes, 0)
        losses = np.abs(np.minimum(price_changes, 0))
        
        # # Calculate the average gains and losses
        avg_gain = self.sma(gains, period)
        avg_loss = self.sma(losses, period)
        
        # # Calculate the Relative Strength (RS)
        rs = avg_gain / avg_loss
        
        # # Calculate the RSI
        rsi = 100 - (100 / (1 + rs))
        
        # # Adjust the length of RSI to match the input prices length
        # # The first (period-1) RSI values are NaN since we don't have enough data points to calculate them
        # rsi = np.concatenate((np.full(period-1, np.nan), rsi))
        
        return rsi
        
    def hammerPattern(self, symbol):
        # https://www.nseindia.com/api/historical/cm/equity?symbol=BAJFINANCE&series=["EQ"]&from=30-06-2024&to=01-07-2024
        # get quote details

        to_date = date.today()
        from_date = to_date - timedelta(days=200)
        to_date_formated = to_date.strftime("%d-%m-%Y")
        from_date_formated = from_date.strftime("%d-%m-%Y")

        data = self.session.makeRequest(
            url = "https://www.nseindia.com/api/historical/cm/equity",
            params = {
                'symbol': symbol,
                # 'series': '\["EQ"\]',
                'from': from_date_formated,
                'to': to_date_formated,
            }
        )

        daily_high = data['data'][0]['CH_TRADE_HIGH_PRICE']
        daily_low = data['data'][0]['CH_TRADE_LOW_PRICE']
        daily_open = data['data'][0]['CH_OPENING_PRICE']
        daily_close = data['data'][0]['CH_CLOSING_PRICE']
        previous_daily_high = data['data'][1]['CH_TRADE_HIGH_PRICE']
        condition1 = daily_high > daily_low
        condition2 = (daily_open-daily_close) <= (daily_high-daily_low) * 0.32
        condition3 = daily_open >= daily_close
        condition4 = (daily_high - daily_close) <= (daily_high - daily_low) * 0.4
        condition5 = (daily_close - daily_open) <= (daily_high-daily_low) * 0.32
        condition6 = daily_open <= daily_close
        condition7 = (daily_high - daily_open) <= (daily_high - daily_low) * 0.4
        condition8 = daily_close > 10
        condition9 = daily_high <= previous_daily_high
        condition10 = daily_close >= self.sma(data['data'])
        condition11 = self.rsi(data['data'], 14) > 30

        return (
            condition1 and 
            (
                (
                    condition2 and 
                    condition3 and 
                    condition4
                ) or 
                (
                    condition5 and 
                    condition6 and 
                    condition7
                )
            ) and
            condition8 and
            condition9 and
            condition10 and
            condition11
        )
