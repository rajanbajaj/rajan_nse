from datetime import date, timedelta
from pandas import DataFrame
from rajan_nse.Session import Session
from rajan_nse.helpers import *

class Strategies:
    def __init__(self):
        self.session = Session("https://www.nseindia.com")
        
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
    def promoterBuyBackStocks(self, delta = 90, to_date = date.today(), save_to_file = False):
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