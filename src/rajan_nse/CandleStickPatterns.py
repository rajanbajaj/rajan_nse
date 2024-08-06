import numpy as np
from rajan_nse.Session import Session
from rajan_nse.TechnicalIndicators import TechnicalIndicators
from rajan_nse.NseData import NseData

class CandleStickPatterns:
    def __init__(self) -> None:
        """This class is used to identify candlestick patterns."""
        self.session = Session("https://www.nseindia.com")
        self.technicalIndicators = TechnicalIndicators()
        self.nseData = NseData()
        pass

    def dojiPattern(self, symbol, live=True, delta = 200):
        """This function is used to identify doji pattern in the given stock symbol and returns a boolean.
        
        Keywork arguments:
        symbol -- The stock symbol for which the doji pattern is to be identified.
        live -- A boolean value indicating whether the data is to be fetched from live market or historical data.
        delta -- The time delta in days for which the data is to be fetched.
        """
        if live:
            current_data = self.nseData.getCurrentData(symbol)

            day_open = current_data['priceInfo']['open']
            day_close = current_data['priceInfo']['lastPrice']
            
            # parity of 0.05 adjusted in day closing and lastPrice
            condition1 = day_open / day_close >= 0.995
            condition2 = day_open / day_close <= 1.005
        else:
            data = self.nseData.getHistoricalData(symbol)
            day_open = data['data'][0]['CH_OPENING_PRICE']
            day_close = data['data'][0]['CH_CLOSING_PRICE']
            condition1 = day_open / day_close >= 0.9995
            condition2 = day_open / day_close <= 1.0005
        
        return (
            condition1 and 
            condition2
        )

    def hammerPattern(self, symbol, live=True, delta = 200):
        """This function is used to identify hammer pattern in the given stock symbol and returns a boolean.

        Keywork arguments:
        symbol -- The stock symbol for which the doji pattern is to be identified.
        live -- A boolean value indicating whether the data is to be fetched from live market or historical data.
        delta -- The time delta in days for which the data is to be fetched.
        """
        data = self.nseData.getHistoricalData(symbol)

        if live:
            current_data = self.nseData.getCurrentData(symbol)

            day_high = current_data['priceInfo']['intraDayHighLow']['max']
            day_low = current_data['priceInfo']['intraDayHighLow']['min']
            day_open = current_data['priceInfo']['open']
            day_close = current_data['priceInfo']['lastPrice']
            prev_day_high = data['data'][0]['CH_TRADE_HIGH_PRICE']
        else:
            day_high = data['data'][0]['CH_TRADE_HIGH_PRICE']
            day_low = data['data'][0]['CH_TRADE_LOW_PRICE']
            day_open = data['data'][0]['CH_OPENING_PRICE']
            day_close = data['data'][0]['CH_CLOSING_PRICE']
            prev_day_high = data['data'][1]['CH_TRADE_HIGH_PRICE']
        
        condition1 = day_high > day_low
        condition2 = (day_open-day_close) <= (day_high-day_low) * 0.32
        condition3 = day_open >= day_close
        condition4 = (day_high - day_close) <= (day_high - day_low) * 0.4
        condition5 = (day_close - day_open) <= (day_high-day_low) * 0.32
        condition6 = day_open <= day_close
        condition7 = (day_high - day_open) <= (day_high - day_low) * 0.4
        condition8 = day_close > 10
        condition9 = day_high <= prev_day_high
        condition10 = day_close >= self.technicalIndicators.sma(symbol)
        condition11 = self.technicalIndicators.rsi(symbol, 14) > 30

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

    def bullishEngullfingPattern(self, symbol, live=True, delta = 200):
        """This function is used to identify bullish engullfing pattern in the given stock symbol and returns a boolean.

        Keywork arguments:
        symbol -- The stock symbol for which the doji pattern is to be identified.
        live -- A boolean value indicating whether the data is to be fetched from live market or historical data.
        delta -- The time delta in days for which the data is to be fetched.
        """
        data = self.nseData.getHistoricalData(symbol)

        if live:
            current_data = self.nseData.getCurrentData(symbol)
            
            day_high = current_data['priceInfo']['intraDayHighLow']['max']
            day_low = current_data['priceInfo']['intraDayHighLow']['min']
            day_open = current_data['priceInfo']['open']
            day_close = current_data['priceInfo']['lastPrice']
            prev_day_high = data['data'][0]['CH_TRADE_HIGH_PRICE']
            prev_day_low = data['data'][0]['CH_TRADE_LOW_PRICE']
            prev_day_open = data['data'][0]['CH_OPENING_PRICE']
            prev_day_close = data['data'][0]['CH_CLOSING_PRICE']
            two_prev_day_close = data['data'][1]['CH_CLOSING_PRICE'] 
            three_prev_day_close = data['data'][2]['CH_CLOSING_PRICE']
            pass
        else:
            day_high = data['data'][0]['CH_TRADE_HIGH_PRICE']
            day_low = data['data'][0]['CH_TRADE_LOW_PRICE']
            day_open = data['data'][0]['CH_OPENING_PRICE']
            day_close = data['data'][0]['CH_CLOSING_PRICE']
            prev_day_high = data['data'][1]['CH_TRADE_HIGH_PRICE']
            prev_day_low = data['data'][1]['CH_TRADE_LOW_PRICE']
            prev_day_open = data['data'][1]['CH_OPENING_PRICE']
            prev_day_close = data['data'][1]['CH_CLOSING_PRICE']
            two_prev_day_close = data['data'][2]['CH_CLOSING_PRICE'] 
            three_prev_day_close = data['data'][3]['CH_CLOSING_PRICE']
        
        condition1 = prev_day_close < prev_day_open # prev day candel is red
        condition2 = day_close > day_open # current day candle is green
        condition3 = day_close >= prev_day_open and day_open <= prev_day_close # engulf
        condition4 = two_prev_day_close > prev_day_close
        condition5 = three_prev_day_close > two_prev_day_close
    
        return (
            condition1 and
            condition2 and
            condition3 and 
            condition4 and
            condition5
        )
    
    def fallingWedgePattern(self, symbol, live=False, period = 200):
        """This function is used to identify falling wedge pattern in the given stock symbol and returns a boolean.

        Keywork arguments:
        symbol -- The stock symbol for which the doji pattern is to be identified.
        live -- A boolean value indicating whether the data is to be fetched from live market or historical data.
        delta -- The time delta in days for which the data is to be fetched.
        """
        return self.wedgePattern(symbol, live, period) == 'FW'
    
    def risingWedgePattern(self, symbol, live=False, period = 200):
        """This function is used to identify rising wedge pattern in the given stock symbol and returns a boolean.

        Keywork arguments:
        symbol -- The stock symbol for which the doji pattern is to be identified.
        live -- A boolean value indicating whether the data is to be fetched from live market or historical data.
        delta -- The time delta in days for which the data is to be fetched.
        """
        return self.wedgePattern(symbol, live, period) == 'RW'

    def wedgePattern(self, symbol, live=False, period = 200):
        """This function is used to identify wedge pattern in the given stock symbol and returns a string indicating the type.
        
        Keywork arguments:
        symbol -- The stock symbol for which the doji pattern is to be identified.
        live -- A boolean value indicating whether the data is to be fetched from live market or historical data.
        delta -- The time delta in days for which the data is to be fetched.
        """
        # Calculate the slope of the upper trend line
        df = self.technicalIndicators.trendLine(symbol, period)
        x_values = np.arange(len(df))
        upper_trend_line = df['UPPER_TREND_LINE'].values
        lower_trend_line = df['LOWER_TREND_LINE'].values

        # Use np.polyfit to find the slope (coefficient) of the linear fit
        slope_peaks, intercept_peaks = np.polyfit(x_values, upper_trend_line, 1)
        slope_troughs, intercept_troughs = np.polyfit(x_values, lower_trend_line, 1)
        
        # Determine if it is a Falling Wedge or Rising Wedge
        if slope_peaks < 0 and slope_troughs < 0:
            if abs(slope_peaks) > abs(slope_troughs):
                pattern = "FW"
            else:
                pattern = "Uncertain - both lines slope downward but upper line is not steeper than lower line"
        elif slope_peaks > 0 and slope_troughs > 0:
            if abs(slope_troughs) > abs(slope_peaks):
                pattern = "RW"
            else:
                pattern = "Uncertain - both lines slope upward but lower line is not steeper than upper line"
        else:
            pattern = "No clear wedge pattern"
        return pattern