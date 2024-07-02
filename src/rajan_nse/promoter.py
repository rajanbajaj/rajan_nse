from Strategies import Strategies
from pandas import DataFrame
from rajan_nse.CandleStickPatterns import CandleStickPatterns
if __name__ == "__main__":
    # strategies = Strategies()

    # data = strategies.promoterBuyBackStocks()
    # DataFrame.to_csv(DataFrame(data), 'final.csv')
    
    
    # data = strategies.insderTradingData("UDS", 200)
    # if not data.empty:
    #     print(data[["date", "symbol", "secVal", "secAcq", "tdpTransactionType", "secType", "personCategory"]])

    # candleStickPatterns = CandleStickPatterns()
    # result = candleStickPatterns.hammerPattern('BRITANNIA')
    # print(result)

    candleStickPatterns = CandleStickPatterns()
    result = candleStickPatterns.bullishEngullfingPattern('BIGBLOC')
    print(result)