from Strategies import Strategies
from pandas import DataFrame

if __name__ == "__main__":
    strategies = Strategies()
    data = strategies.promoterBuyBackStocks()
    DataFrame.to_csv(DataFrame(data), 'final.csv')
