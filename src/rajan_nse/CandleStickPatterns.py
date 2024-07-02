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

    def getCurrentData(self, symbol):
        # https://www.nseindia.com/api/quote-equity?symbol=X
        data = self.session.makeRequest(
            url = "https://www.nseindia.com/api/quote-equity",
            params = {
                'symbol': symbol,
            }
        )

        # data = {"info":{"symbol":"X","companyName":"X Limited","industry":"COMPUTERS - SOFTWARE","activeSeries":["EQ"],"debtSeries":[],"isFNOSec":true,"isCASec":false,"isSLBSec":true,"isDebtSec":false,"isSuspended":false,"tempSuspendedSeries":[],"isETFSec":false,"isDelisted":false,"isin":"INE075A01022","isMunicipalBond":false,"isTop10":false,"identifier":"XEQN"},"metadata":{"series":"EQ","symbol":"X","isin":"INE075A01022","status":"Listed","listingDate":"08-Nov-1995","industry":"Computers - Software & Consulting","lastUpdateTime":"02-Jul-2024 15:24:00","pdSectorPe":24.77,"pdSymbolPe":24.77,"pdSectorInd":"NIFTY IT                                          "},"securityInfo":{"boardStatus":"Main","tradingStatus":"Active","tradingSegment":"Normal Market","sessionNo":"-","slb":"Yes","classOfShare":"Equity","derivatives":"Yes","surveillance":{"surv":null,"desc":null},"faceValue":2,"issuedSize":5230164205},"sddDetails":{"SDDAuditor":"-","SDDStatus":"-"},"priceInfo":{"lastPrice":537.55,"change":10.199999999999932,"pChange":1.9341992983786729,"previousClose":527.35,"open":529.3,"close":0,"vwap":538.33,"lowerCP":"474.65","upperCP":"580.05","pPriceBand":"No Band","basePrice":527.35,"intraDayHighLow":{"min":528.3,"max":545,"value":537.55},"weekHighLow":{"min":375.05,"minDate":"26-Oct-2023","max":545.9,"maxDate":"19-Feb-2024","value":537.55},"iNavValue":null,"checkINAV":false},"industryInfo":{"macro":"Information Technology","sector":"Information Technology","industry":"IT - Software","basicIndustry":"Computers - Software & Consulting"},"preOpenMarket":{"preopen":[{"price":474.65,"buyQty":0,"sellQty":604},{"price":480,"buyQty":0,"sellQty":500},{"price":501,"buyQty":0,"sellQty":7161},{"price":503.6,"buyQty":0,"sellQty":10},{"price":529.3,"buyQty":0,"sellQty":0,"iep":true},{"price":551.05,"buyQty":306,"sellQty":0},{"price":551.1,"buyQty":8,"sellQty":0},{"price":580,"buyQty":20,"sellQty":0},{"price":580.05,"buyQty":205,"sellQty":0}],"ato":{"buy":24235,"sell":2858},"IEP":529.3,"totalTradedVolume":98656,"finalPrice":529.3,"finalQuantity":98656,"lastUpdateTime":"02-Jul-2024 09:08:03","totalBuyQuantity":79562,"totalSellQuantity":304045,"atoBuyQty":24235,"atoSellQty":2858,"Change":1.9499999999999318,"perChange":0.3697733952782652,"prevClose":527.35}}
        return data

    def getHistoricalData(self, symbol, delt = 200):
        # https://www.nseindia.com/api/historical/cm/equity?symbol=BAJFINANCE&series=["EQ"]&from=30-06-2024&to=01-07-2024
        # get quote historical details

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

        #data['data'] = [{CH_TRADE_HIGH_PRICE, CH_TRADE_LOW_PRICE, CH_OPENING_PRICE, CH_CLOSING_PRICE, CH_TRADE_HIGH_PRICE}, {}, ...] 
        return data

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

    def bullishEngullfingPattern(self, symbol, live=True):
        data = self.getHistoricalData(symbol)

        if live:
            current_data = self.getCurrentData(symbol)
            
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