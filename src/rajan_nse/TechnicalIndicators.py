import numpy as np

class TechnicalIndicators:
    def sma(self, data, period=200):
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