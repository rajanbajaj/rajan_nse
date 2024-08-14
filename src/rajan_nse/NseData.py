from datetime import date, timedelta, datetime
from rajan_nse.Session import Session
from bs4 import BeautifulSoup
import json
import re

class NseData:
    def __init__(self) -> None:
        """This class is used to fetch data from NSE India wesite."""
        self.session = Session("https://www.nseindia.com")
        pass

    def getInsiderTradingDataWithSymbol(self, symbol, delta = 90):
        """
        Get insider trainind data for a given symbol.

        Keywork arguments:
        symbol -- The symbol of the stock.
        delta -- The number of days to fetch data for. Default is 90 days.

        Response structure:
        [
            {
                "symbol": "COMPANY",
                "company": "COMPANY",
                "anex": "7(2)",
                "acqName": "SHOBHA AGARWAL",
                "date": "14-Dec-2023 18:02",
                "pid": "1157172",
                "tkdAcqm": null,
                "buyValue": "0",
                "sellValue": "0",
                "buyQuantity": "0",
                "sellquantity": "0",
                "secType": "Equity Shares",
                "secAcq": "150000",
                "did": "489950",
                "tdpTransactionType": "Sell",
                "tdpDerivativeContractType": "-",
                "xbrl": "https://nsearchives.nseindia.com/corporate/xbrl/IT_1157172_997084_14122023060254_WEB.xml",
                "personCategory": "Immediate relative",
                "befAcqSharesNo": "731905",
                "befAcqSharesPer": "0.01",
                "secVal": "0",
                "securitiesTypePost": "Equity Shares",
                "afterAcqSharesNo": "581905",
                "afterAcqSharesPer": "0.01",
                "acqfromDt": "11-Dec-2023",
                "acqtoDt": "11-Dec-2023",
                "intimDt": "12-Dec-2023",
                "acqMode": "Gift",
                "derivativeType": "-",
                "exchange": "NA",
                "remarks": "-"
            },
            { ... }
        ]
        """
        to_date = date.today()
        from_date = to_date - timedelta(days=delta)
        to_date_formated = to_date.strftime("%d-%m-%Y")
        from_date_formated = from_date.strftime("%d-%m-%Y")

        data = self.session.makeRequest(
            url="https://www.nseindia.com/api/corporates-pit",
            params= {
                'index': 'equities',
                'from_date': from_date_formated,
                'to_date': to_date_formated,
                'symbol': symbol
            }
        )

        return data['data']

    def getCurrentData(self, symbol):
        """Get current market data for the symbol and return the json response

        Keyword arguments:
        symbol -- the symbol of the stock

        Request url: https://www.nseindia.com/api/quote-equity?symbol=X
        Response structure:
        {
            "info": {
                "symbol": "X",
                "companyName": "X Limited",
                "industry": "COMPUTERS - SOFTWARE",
                "activeSeries": [
                "EQ"
                ],
                "debtSeries": [],
                "isFNOSec": true,
                "isCASec": false,
                "isSLBSec": true,
                "isDebtSec": false,
                "isSuspended": false,
                "tempSuspendedSeries": [],
                "isETFSec": false,
                "isDelisted": false,
                "isin": "INE075A01022",
                "isMunicipalBond": false,
                "isTop10": false,
                "identifier": "XEQN"
            },
            "metadata": {
                "series": "EQ",
                "symbol": "X",
                "isin": "INE075A01022",
                "status": "Listed",
                "listingDate": "08-Nov-1995",
                "industry": "Computers - Software & Consulting",
                "lastUpdateTime": "02-Jul-2024 15:24:00",
                "pdSectorPe": 24.77,
                "pdSymbolPe": 24.77,
                "pdSectorInd": "NIFTY IT                                          "
            },
            "securityInfo": {
                "boardStatus": "Main",
                "tradingStatus": "Active",
                "tradingSegment": "Normal Market",
                "sessionNo": "-",
                "slb": "Yes",
                "classOfShare": "Equity",
                "derivatives": "Yes",
                "surveillance": {
                "surv": null,
                "desc": null
                },
                "faceValue": 2,
                "issuedSize": 5230164205
            },
            "sddDetails": {
                "SDDAuditor": "-",
                "SDDStatus": "-"
            },
            "priceInfo": {
                "lastPrice": 537.55,
                "change": 10.199999999999932,
                "pChange": 1.9341992983786729,
                "previousClose": 527.35,
                "open": 529.3,
                "close": 0,
                "vwap": 538.33,
                "lowerCP": "474.65",
                "upperCP": "580.05",
                "pPriceBand": "No Band",
                "basePrice": 527.35,
                "intraDayHighLow": {
                "min": 528.3,
                "max": 545,
                "value": 537.55
                },
                "weekHighLow": {
                "min": 375.05,
                "minDate": "26-Oct-2023",
                "max": 545.9,
                "maxDate": "19-Feb-2024",
                "value": 537.55
                },
                "iNavValue": null,
                "checkINAV": false
            },
            "industryInfo": {
                "macro": "Information Technology",
                "sector": "Information Technology",
                "industry": "IT - Software",
                "basicIndustry": "Computers - Software & Consulting"
            },
            "preOpenMarket": {
                "preopen": [
                {
                    "price": 474.65,
                    "buyQty": 0,
                    "sellQty": 604
                },
                {
                    "price": 480,
                    "buyQty": 0,
                    "sellQty": 500
                },
                {
                    "price": 501,
                    "buyQty": 0,
                    "sellQty": 7161
                },
                {
                    "price": 503.6,
                    "buyQty": 0,
                    "sellQty": 10
                },
                {
                    "price": 529.3,
                    "buyQty": 0,
                    "sellQty": 0,
                    "iep": true
                },
                {
                    "price": 551.05,
                    "buyQty": 306,
                    "sellQty": 0
                },
                {
                    "price": 551.1,
                    "buyQty": 8,
                    "sellQty": 0
                },
                {
                    "price": 580,
                    "buyQty": 20,
                    "sellQty": 0
                },
                {
                    "price": 580.05,
                    "buyQty": 205,
                    "sellQty": 0
                }
                ],
                "ato": {
                "buy": 24235,
                "sell": 2858
                },
                "IEP": 529.3,
                "totalTradedVolume": 98656,
                "finalPrice": 529.3,
                "finalQuantity": 98656,
                "lastUpdateTime": "02-Jul-2024 09:08:03",
                "totalBuyQuantity": 79562,
                "totalSellQuantity": 304045,
                "atoBuyQty": 24235,
                "atoSellQty": 2858,
                "Change": 1.9499999999999318,
                "perChange": 0.3697733952782652,
                "prevClose": 527.35
            }
        }
        """
        data = self.session.makeRequest(
            url = "https://www.nseindia.com/api/quote-equity",
            params = {
                'symbol': symbol,
            }
        )

        # data = {"info":{"symbol":"X","companyName":"X Limited","industry":"COMPUTERS - SOFTWARE","activeSeries":["EQ"],"debtSeries":[],"isFNOSec":true,"isCASec":false,"isSLBSec":true,"isDebtSec":false,"isSuspended":false,"tempSuspendedSeries":[],"isETFSec":false,"isDelisted":false,"isin":"INE075A01022","isMunicipalBond":false,"isTop10":false,"identifier":"XEQN"},"metadata":{"series":"EQ","symbol":"X","isin":"INE075A01022","status":"Listed","listingDate":"08-Nov-1995","industry":"Computers - Software & Consulting","lastUpdateTime":"02-Jul-2024 15:24:00","pdSectorPe":24.77,"pdSymbolPe":24.77,"pdSectorInd":"NIFTY IT                                          "},"securityInfo":{"boardStatus":"Main","tradingStatus":"Active","tradingSegment":"Normal Market","sessionNo":"-","slb":"Yes","classOfShare":"Equity","derivatives":"Yes","surveillance":{"surv":null,"desc":null},"faceValue":2,"issuedSize":5230164205},"sddDetails":{"SDDAuditor":"-","SDDStatus":"-"},"priceInfo":{"lastPrice":537.55,"change":10.199999999999932,"pChange":1.9341992983786729,"previousClose":527.35,"open":529.3,"close":0,"vwap":538.33,"lowerCP":"474.65","upperCP":"580.05","pPriceBand":"No Band","basePrice":527.35,"intraDayHighLow":{"min":528.3,"max":545,"value":537.55},"weekHighLow":{"min":375.05,"minDate":"26-Oct-2023","max":545.9,"maxDate":"19-Feb-2024","value":537.55},"iNavValue":null,"checkINAV":false},"industryInfo":{"macro":"Information Technology","sector":"Information Technology","industry":"IT - Software","basicIndustry":"Computers - Software & Consulting"},"preOpenMarket":{"preopen":[{"price":474.65,"buyQty":0,"sellQty":604},{"price":480,"buyQty":0,"sellQty":500},{"price":501,"buyQty":0,"sellQty":7161},{"price":503.6,"buyQty":0,"sellQty":10},{"price":529.3,"buyQty":0,"sellQty":0,"iep":true},{"price":551.05,"buyQty":306,"sellQty":0},{"price":551.1,"buyQty":8,"sellQty":0},{"price":580,"buyQty":20,"sellQty":0},{"price":580.05,"buyQty":205,"sellQty":0}],"ato":{"buy":24235,"sell":2858},"IEP":529.3,"totalTradedVolume":98656,"finalPrice":529.3,"finalQuantity":98656,"lastUpdateTime":"02-Jul-2024 09:08:03","totalBuyQuantity":79562,"totalSellQuantity":304045,"atoBuyQty":24235,"atoSellQty":2858,"Change":1.9499999999999318,"perChange":0.3697733952782652,"prevClose":527.35}}
        return data

    def getHistoricalData(self, symbol, delta = 200, to_date = date.today(), depth = 3):
        """Get historical data for a given symbol.

        Keyword arguments:
        symbol -- the symbol of the stock
        delta -- the number of days to get data for (default 200)
        to_date -- the date to get data up to (default today)
        depth -- the number of loop count to get data for (default 3, i.e 3*200 count)

        Request url: https://www.nseindia.com/api/historical/cm/equity?symbol=SYMBOL&series=["EQ"]&from=FROM&to=TO
        """
        from_date = to_date - timedelta(days=delta)
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

        try:
            for i in range(0, depth):
                last_date = data['data'][-1]['CH_TIMESTAMP']
                        # Convert to datetime object
                to_date = datetime.strptime(last_date, '%Y-%m-%d')

                # Convert datetime object to DD-MM-YY format string
                to_date_formated = to_date.strftime('%d-%m-%Y')
                from_date = to_date - timedelta(days=delta)
                from_date_formated = from_date.strftime("%d-%m-%Y")

                try:
                    tmp = self.session.makeRequest(
                        url = "https://www.nseindia.com/api/historical/cm/equity",
                        params = {
                            'symbol': symbol,
                            'from': from_date_formated,
                            'to': to_date_formated,
                        }
                    )
                    data['data'].extend(tmp['data'])
                except Exception as e:
                    print(e)
                    break
        except Exception as e:
                print(e)

        data['data'] = data['data'][:delta]

        #data['data'] = [{CH_TRADE_HIGH_PRICE, CH_TRADE_LOW_PRICE, CH_OPENING_PRICE, CH_CLOSING_PRICE, CH_TOT_TRADED_QTY}, {}, ...]
        return data

    def fiftyTwoWeekHighLow(self, symbol, live=True):
        """
        Get 52 Weeks High and Low values for given symbol

        Keyword arguments:
        symbol -- symbol of the stock
        live -- boolean value to get data from live or historical data

        Return structure:
        {
            'high': 100,
            'low': 15,

           'price': 55
        }
        """
        current_data = self.getCurrentData(symbol)
        if live:
            return {
                'high': current_data['priceInfo']['weekHighLow']['max'],
                'low': current_data['priceInfo']['weekHighLow']['min'],
                'price': current_data['priceInfo']['lastPrice']

            }
        else:
            historical_data = self.getHistoricalData(symbol, 20)
            return {
                'high': current_data['priceInfo']['weekHighLow']['max'],
                'low': current_data['priceInfo']['weekHighLow']['min'],
                'price': historical_data['data'][0]['CH_CLOSING_PRICE']
            }

    def getOISpurtsData(self):
        """Get OI spurts data"""
        data = self.session.makeRequest(
            url = "https://www.nseindia.com/api/live-analysis-oi-spurts-underlyings"
        )

        return data['data'];

    def getTopGainersLosers(self):
        """
        Get indexDataInfo data with following structure
        response structure:
        {
            'advance': {},
            'topGainers': {},
            'topLosers': {},
            'topVolume': {},
            'topValue': {}
        }
        """
        data = self.session.makeRequest(
            url = "https://www.nseindia.com/",
            responseType = "text"
        )
        #print(data)
        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(data, 'html.parser')

        # Find the script tag containing the specific text
        script_tags = soup.find_all('script')

        result = None
        # Substring to remove
        prefix = '      window.headerData = '

        for script in script_tags:
            if 'window.headerData =' in script.text:
                # Find the line starting with `window.headerData = { "advances"`
                lines = script.text.split('\n')
                for line in lines:
                    if line.strip().startswith('window.headerData = {"indexDataInfo"'):
                        result = json.loads(line[len(prefix):])
        result = result['indexDataInfo']
        top_gainers = result[0]['topGainers']
        top_losers = result[0]['topLosers']

        return result[0]
