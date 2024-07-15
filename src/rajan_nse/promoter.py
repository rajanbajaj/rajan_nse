from rajan_nse.Strategies import Strategies
from rajan_nse.TechnicalIndicators import TechnicalIndicators
from rajan_nse.NseData import NseData
from pandas import DataFrame

# TODO add rajan.nse
from CandleStickPatterns import CandleStickPatterns

if __name__ == "__main__":
    # strategies = Strategies()
    # data = strategies.promoterBuyBackStocks(300)
    # print(data)
    # DataFrame.to_csv(DataFrame(data), 'final.csv')

    # candleStickPatterns = CandleStickPatterns()
    # result = candleStickPatterns.hammerPattern('BRITANNIA')
    # print(result)

    # candleStickPatterns = CandleStickPatterns()
    # result = candleStickPatterns.bullishEngullfingPattern('BIGBLOC')
    # print(result)

    # candleStickPatterns = CandleStickPatterns()
    # result = candleStickPatterns.dojiPattern('ASIANPAINT', False)
    # print(result)

    # technicalIndicators = TechnicalIndicators()

    # print(technicalIndicators.sma('RELIANCE'))
    # print(technicalIndicators.sma('RELIANCE', 14))
    # print(technicalIndicators.rsi('RELIANCE'))
    # print(technicalIndicators.cmf('RELIANCE'))
    # print(technicalIndicators.near52WeekHigh('RELIANCE'))
    # print(technicalIndicators.near52WeekLow('RELIANCE'))

    # technicalIndicators = TechnicalIndicators()
    # print(technicalIndicators.trendLine('RELIANCE').head())

    candleStickPatterns = CandleStickPatterns()
    print(candleStickPatterns.wedgePattern('BAJAJ-AUTO', 50))