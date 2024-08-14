from datetime import date, timedelta
from pandas import DataFrame
from rajan_nse.Session import Session
from rajan_nse.helpers import *
from rajan_nse.NseData import NseData

class Strategies:
    def __init__(self):
        """This class has strategies to filter NSE stocks to build a watchlist."""
        self.session = Session("https://www.nseindia.com")
        self.nseData = NseData()

    def promoterBuyBackStocks(self, delta = 90, to_date = date.today(), save_to_file = False):
        """
        This function will return the list of stocks which are
        filtered by promoter buy back strategy with following
        seven steps.
        1. Get the list of stocks which are intraday traded in last 90 days (3months)
        2. Filter out the stocks in which traded value is less than 1cr
        3. Filter out the stocks in which promoter holding is less than 50%
        4. Filter out the stocks based on sast data
        5/6/7. Individual stock analysis for promoter details
        """
        from_date = to_date - timedelta(days=delta)
        to_date_formated = to_date.strftime("%d-%m-%Y")
        from_date_formated = from_date.replace(day=to_date.day).strftime("%d-%m-%Y")
        data = filterBasedOnPromoterBuyBackStrategy(self.session, to_date_formated, from_date_formated)

        # save data to file
        try:
            if save_to_file:
                DataFrame.to_csv(DataFrame(data), 'final-'+ to_date_formated +'.csv')
        except Exception as e:
            # print(e)
            return

        return data

    def oiSpurtsFilteredGainerStocks(self):
        """
        This method get all the stocks based on the below filter

        Stocks that appear in daily top gainers or losers that has OI change > 4% by 9:20AM
        """
        top_gainers = self.nseData.getTopGainersLosers()['topGainers']['data']
        oi_spurts = self.nseData.getOISpurtsData()

        result = []
        for gainer in top_gainers:
            for oi_spurt in oi_spurts:
                if gainer['symbol'] == oi_spurt['symbol'] and oi_spurt['avgInOI'] > 4:
                    result.append(gainer['symbol'])

        return result
    
    def oiSpurtsFilteredLoserStocks(self):
        """
        This method get all the stocks based on the below filter

        Stocks that appear in daily top gainers or losers that has OI change > 4% by 9:20AM
        """
        top_losers = self.nseData.getTopGainersLosers()['topLosers']['data']
        oi_spurts = self.nseData.getOISpurtsData()

        result = []
        for gainer in top_losers:
            for oi_spurt in oi_spurts:
                if gainer['symbol'] == oi_spurt['symbol'] and oi_spurt['avgInOI'] > 4:
                    result.append(gainer['symbol'])

        return result
