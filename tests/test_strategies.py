from rajan_nse import Strategies

strategies = Strategies()

def test_oi_spurts_filtered_stocks():
    data = strategies.oiSpurtsFilteredStocks()
    print(data)
    assert isinstance(data, list), "data type must be list."

