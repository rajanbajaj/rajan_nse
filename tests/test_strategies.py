from rajan_nse import Strategies

strategies = Strategies()

def test_oi_spurts_filtered_gainer_stocks():
    data = strategies.oiSpurtsFilteredGainerStocks()
    print(data)
    assert isinstance(data, list), "data type must be list."

def test_oi_spurts_filtered_loser_stocks():
    data = strategies.oiSpurtsFilteredLoserStocks()
    print(data)
    assert isinstance(data, list), "data type must be list."


