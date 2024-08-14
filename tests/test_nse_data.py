from rajan_nse import NseData

nse_data = NseData()
def test_oi_spurts():
    """Test OI spurts"""
    data = nse_data.getOISpurtsData()
    print(data)
    assert isinstance(data, list), "data type must be list."

def test_top_gainer_loser():
    """Test method for top days gainers and loser"""
    data = nse_data.getTopGainersLosers()
    print(data)
    assert data != None and "topGainers" in data and "topLosers" in data
