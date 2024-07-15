"""
rajan_nse package

The rajan_nse package is a comprehensive toolkit designed for analyzing and visualizing stock market data from the National Stock Exchange (NSE) of India. This package provides various modules to facilitate technical analysis, identify candlestick patterns, create visual representations, and develop trading strategies.
"""

# Import specific functions or classes for easy access
from .CandleStickPatterns import CandleStickPatterns
from .NseData import NseData
from .Session import Session
from .Strategies import Strategies
from .TechnicalIndicators import TechnicalIndicators
from .Visualization import Visualization

# Define what should be accessible when 'from rajan_nse import *' is used
__all__ = [
    "CandleStickPatterns",
    'NseData', 
    'Session', 
    'Strategies', 
    'TechnicalIndicators', 
    'Visualization'
]

