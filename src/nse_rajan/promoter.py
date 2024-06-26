from datetime import date, timedelta
from pandas import DataFrame
from Session import Session
from helpers import *

if __name__ == "__main__":
    session = Session("https://www.nseindia.com")
    
    delta = 90
    to_date = date.today()
    from_date = to_date - timedelta(days=delta)
    to_date_formated = to_date.strftime("%d-%m-%Y")
    from_date_formated = from_date.replace(day=to_date.day).strftime("%d-%m-%Y")

    data = filterBasedOnPromoterBuyBackStrategy(session, to_date_formated, from_date_formated)
    DataFrame.to_csv(DataFrame(data), 'data/final-'+ to_date_formated +'.csv')
