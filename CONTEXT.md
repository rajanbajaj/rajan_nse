# rajan_nse — Project Context

## Overview

**rajan_nse** is a Python package (v1.2.6) for analyzing and visualizing stock market data from the National Stock Exchange (NSE) of India. Published on PyPI and documented at https://rajan-nse.readthedocs.io/.

- **Author**: Rajan Bajaj
- **License**: MIT
- **Python**: >= 3.8
- **Build system**: Hatchling

## Project Structure

```
rajan_nse/
├── src/rajan_nse/
│   ├── __init__.py              # Package exports
│   ├── Session.py               # HTTP session management for NSE
│   ├── NseData.py               # NSE API data fetching
│   ├── TechnicalIndicators.py   # SMA, RSI, CMF, trend lines
│   ├── CandleStickPatterns.py   # Pattern detection (Doji, Hammer, Engulfing, Wedge)
│   ├── Strategies.py            # Stock filtering strategies
│   ├── Visualization.py         # Chart plotting
│   ├── helpers.py               # Strategy helper functions
│   └── promoter.py              # (unused/extra)
├── tests/
│   ├── test_nse_data.py         # Tests for NseData methods
│   └── test_strategies.py       # Tests for strategy methods
├── docs/                        # Sphinx documentation
├── .github/workflows/
│   ├── build.yml                # CI build workflow
│   └── python-publish.yml       # PyPI publish workflow
├── pyproject.toml
├── requirements.txt
└── sonar-project.properties     # SonarQube config
```

## Modules

### Session (`Session.py`)
Manages HTTP sessions against `https://www.nseindia.com`. Sets browser-like headers (Firefox UA, cookies) to bypass NSE bot protection.

- `Session(base_url)` — creates session, calls `createNewSession()` to prime cookies
- `makeRequest(url, params=None, responseType='json')` — GET request returning `json | text | content | raw`

**Note**: The `Cookie` header in `Session.py` is hardcoded and will expire. Must be refreshed periodically from a real browser session.

### NseData (`NseData.py`)
Wraps NSE public APIs to fetch market data.

| Method | Description | NSE API Endpoint |
|--------|-------------|-----------------|
| `getCurrentData(symbol)` | Live quote (price, metadata, pre-open) | `/api/quote-equity` |
| `getHistoricalData(symbol, delta=200, to_date=today, depth=3)` | OHLCV historical data (paginated, up to `delta*depth` days) | `/api/historical/cm/equity` |
| `fiftyTwoWeekHighLow(symbol, live=True)` | 52-week high/low + current price | Uses `getCurrentData` / `getHistoricalData` |
| `getOISpurtsData()` | Open interest spurts (F&O) | `/api/live-analysis-oi-spurts-underlyings` |
| `getTopGainersLosers()` | Top gainers, losers, volume, value | Scrapes NSE homepage HTML |
| `getInsiderTradingDataWithSymbol(symbol, delta=90)` | Insider/PIT trading data | `/api/corporates-pit` |

**Historical data fields**: `CH_TIMESTAMP`, `CH_OPENING_PRICE`, `CH_CLOSING_PRICE`, `CH_TRADE_HIGH_PRICE`, `CH_TRADE_LOW_PRICE`, `CH_TOT_TRADED_QTY`

### TechnicalIndicators (`TechnicalIndicators.py`)
Calculates technical indicators from NSE data.

| Method | Description |
|--------|-------------|
| `sma(symbol, period=200, data=None)` | Simple Moving Average (daily close prices) |
| `rsi(symbol, period=14)` | Relative Strength Index |
| `cmf(symbol, period=21)` | Chaikin Money Flow |
| `near52WeekHigh(symbol, live=False, delta=5)` | True if price within `delta`% of 52-week high |
| `near52WeekLow(symbol, live=False, delta=5)` | True if price within `delta`% of 52-week low |
| `trendLine(symbol, delta=200, lower_percentile=40, upper_percentile=98, to_date=today)` | Linear regression trend lines (upper/lower) using sklearn; returns DataFrame with `UPPER_TREND_LINE`, `LOWER_TREND_LINE` columns |

### CandleStickPatterns (`CandleStickPatterns.py`)
Detects candlestick chart patterns. All methods return bool (or string for `wedgePattern`).

| Method | Description |
|--------|-------------|
| `dojiPattern(symbol, live=True, delta=200)` | Open ≈ Close (within 0.5% live, 0.05% historical) |
| `hammerPattern(symbol, live=True, delta=200)` | Small body + long lower shadow; also checks SMA200 and RSI > 30 |
| `bullishEngullfingPattern(symbol, live=True, delta=200)` | Green candle engulfs prior red candle after 3-day downtrend |
| `fallingWedgePattern(symbol, live=False, period=200)` | Both trendlines slope down, upper steeper |
| `risingWedgePattern(symbol, live=False, period=200)` | Both trendlines slope up, lower steeper |
| `wedgePattern(symbol, live=False, period=200)` | Returns `"FW"`, `"RW"`, or descriptive uncertainty string |

### Strategies (`Strategies.py`)
Higher-level stock screening strategies.

| Method | Description |
|--------|-------------|
| `promoterBuyBackStocks(delta=90, to_date=today, save_to_file=False)` | Multi-step promoter buyback screen — see [Promoter Buyback Strategy](#promoter-buyback-strategy) below |
| `oiSpurtsFilteredGainerStocks()` | Top gainers that also appear in OI spurts with avgInOI > 4% |
| `oiSpurtsFilteredLoserStocks()` | Top losers that also appear in OI spurts with avgInOI > 4% |

### Helpers (`helpers.py`)
Internal functions used by `Strategies`:

- `isPromoterFilterPassed(session, symbol)` — promoter holding > 50%, no pledged/encumbered shares
- `isSastRegulationFilterPassed(session, symbol)` — no SAST sale transactions
- `findAvgPrice(session, to_date, from_date, symbol)` — weighted avg price of promoter market purchases
- `lastPrice(session, symbol)` — current last traded price
- `getInsiderTradingData(session, to_date, from_date)` — full PIT data as DataFrame
- `filterStocksBasedOnValueThreshold(session, to_date, from_date, threshold=10000000)` — filter by insider buy value > 1cr
- `filterStocksBasedOnPromoterAndSast(session, to_date, from_date)` — apply promoter + SAST filters
- `filterBasedOnPromoterBuyBackStrategy(session, to_date, from_date, allowed_diff=0.05)` — full pipeline, returns `[[symbol, avg_price, last_price], ...]`

### Visualization (`Visualization.py`)
- `plotDistribution(data, save=False, filePath='distribution_plot.png')` — seaborn histogram + KDE of volume data

## NSE API Endpoints Used

| Endpoint | Purpose |
|----------|---------|
| `GET /api/quote-equity?symbol=X` | Live equity quote |
| `GET /api/historical/cm/equity?symbol=X&from=DD-MM-YYYY&to=DD-MM-YYYY` | Historical OHLCV |
| `GET /api/corporates-pit?index=equities&from_date=X&to_date=X&symbol=X` | Insider/PIT trading data |
| `GET /api/live-analysis-oi-spurts-underlyings` | OI spurts |
| `GET /api/corp-info?symbol=X&corpType=promoterenc&market=equities` | Promoter holding/pledge info |
| `GET /api/corp-info?symbol=X&corpType=sast&market=equities` | SAST regulation data |
| `GET /` (HTML scrape) | Top gainers/losers from `window.headerData` JS variable |

## Dependencies

```
alive_progress==3.1.5
beautifulsoup4==4.12.3
matplotlib==3.9.2
numpy==2.0.1
pandas==2.2.2
Requests==2.32.3
scikit_learn==1.5.1
seaborn==0.13.2
tqdm==4.66.5
```

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests (suppress output)
python3 -m pytest tests

# Run tests (with print output)
python3 -m pytest -s tests

# Build package
python3 -m build

# Install locally
pip install -e .
```

## Usage Example

```python
from rajan_nse import NseData, TechnicalIndicators, CandleStickPatterns, Strategies

# Fetch data
nse = NseData()
historical = nse.getHistoricalData("RELIANCE", delta=200)
current = nse.getCurrentData("RELIANCE")

# Technical indicators
ti = TechnicalIndicators()
sma200 = ti.sma("RELIANCE", period=200)
rsi = ti.rsi("RELIANCE", period=14)
cmf = ti.cmf("RELIANCE", period=21)

# Candlestick patterns
csp = CandleStickPatterns()
is_doji = csp.dojiPattern("RELIANCE", live=True)
is_hammer = csp.hammerPattern("RELIANCE", live=False)

# Strategies
st = Strategies()
watchlist = st.promoterBuyBackStocks(delta=90)
oi_gainers = st.oiSpurtsFilteredGainerStocks()
```

---

## Promoter Buyback Strategy

### Objective

Identify stocks where **company promoters are actively buying back shares at market price** and the **current stock price is still within their average buy price zone** — a signal that promoters believe the stock is undervalued.

### Hypothesis

When promoters (insiders with > 50% holding, no pledged shares) are buying via open market purchases and have not sold during the same period, they are expressing high conviction. If the stock price has not moved significantly above their average buy price, it is still in their "buy zone" and worth watching.

### Call Chain

```
Strategies.promoterBuyBackStocks(delta=90)
  └── helpers.filterBasedOnPromoterBuyBackStrategy(session, to_date, from_date)
        ├── helpers.filterStocksBasedOnPromoterAndSast(session, to_date, from_date)
        │     ├── helpers.filterStocksBasedOnValueThreshold(session, to_date, from_date, threshold=1cr)
        │     │     └── helpers.getInsiderTradingData()   → /api/corporates-pit
        │     ├── helpers.isPromoterFilterPassed()        → /api/corp-info?corpType=promoterenc
        │     └── helpers.isSastRegulationFilterPassed()  → /api/corp-info?corpType=sast
        ├── helpers.findAvgPrice()                        → /api/corporates-pit
        └── helpers.lastPrice()                           → /api/quote-equity
```

### Filter Pipeline

| Step | Filter | Source | Logic |
|------|--------|--------|-------|
| 1 | Fetch all insider (PIT) disclosures for the date range | `/api/corporates-pit` | All categories, all transaction types |
| 2 | Keep only `acqMode == 'Market Purchase'`; group by symbol; keep where total `secVal > 1cr` | — | Eliminates gifts, ESOPs, off-market transfers; ensures meaningful buy size |
| 3 | Promoter holding > 50%, zero pledged shares (`per2 == 0`), zero encumbered shares (`per3 == 0`) | `/api/corp-info?corpType=promoterenc` | Ensures promoters have control and skin in the game with no distress signals |
| 4 | No SAST-regulated share sales during the period (`noOfShareSale.sum() == 0`) | `/api/corp-info?corpType=sast` | Eliminates insiders who are net sellers |
| 5 | Among remaining stocks, find promoter/promoter-group Equity Share **Buy** transactions with **zero sell transactions** in the period; compute weighted avg buy price = `secVal.sum() / secAcq.sum()` | `/api/corporates-pit` | Confirms pure buying conviction with no mixed signals |
| 6 | Fetch current last traded price | `/api/quote-equity` | Live market price |
| 7 | Keep only if `(last_price - avg_price) / avg_price < 5%` | — | Price has not significantly run above promoter's buy zone |

### Output

```python
# Returns list of [symbol, avg_promoter_buy_price, last_traded_price]
[
    ["BAJFINANCE", 650.25, 661.00],
    ["XSYMBOL",   120.10, 118.50],
    ...
]

# Optional: saved to 'final-DD-MM-YYYY.csv' when save_to_file=True
# Side effect: always writes 'stocks_DD-MM-YYYY.tmp.csv' at step 2 (see bugs)
```

### Usage

```python
from rajan_nse import Strategies

st = Strategies()

# Default: last 90 days, today's date
watchlist = st.promoterBuyBackStocks()

# Custom date range (last 6 months)
from datetime import date
watchlist = st.promoterBuyBackStocks(delta=180, to_date=date.today(), save_to_file=True)

print(watchlist)
# [['SYMBOL', avg_buy_price, last_price], ...]
```

### Bugs

**Bug 1 — `from_date` computed incorrectly (`Strategies.py:27`)**

```python
# Current (wrong):
from_date_formated = from_date.replace(day=to_date.day).strftime("%d-%m-%Y")
# Replaces the day of from_date with today's day number.
# Harmless most of the time (off by 1 day), but CRASHES when today's day
# doesn't exist in from_date's month.
# e.g. to_date=May 31, delta=90 → from_date=Mar 2 → .replace(day=31) → ValueError

# Fix:
from_date_formated = from_date.strftime("%d-%m-%Y")
```

**Bug 2 — Price proximity check is one-sided (`helpers.py:161`)**

```python
# Current (wrong):
diff = (last_price - avg_price) / abs(avg_price)
if avg_price != -1 and diff < allowed_diff:
# Passes any stock where last_price is BELOW avg_price by ANY amount.
# e.g. avg=100, last=10 → diff=-0.9 → passes (stock crashed 90%, still included)

# Fix:
if avg_price != -1 and abs(diff) < allowed_diff:
```

**Bug 3 — Fragile string replacement on `secVal` (`helpers.py:117`)**

```python
# Current:
df['secVal'] = df['secVal'].replace('-', 0)
df['secVal'] = to_numeric(df['secVal'])
# pandas Series .replace() does exact value match, so '-' is handled.
# But other non-numeric values (None, NaN, malformed strings) will cause
# to_numeric() to raise or silently NaN — no error handling.

# More robust:
df['secVal'] = pd.to_numeric(df['secVal'].replace('-', '0'), errors='coerce').fillna(0)
```

**Bug 4 — Temp CSV is always written as a side effect (`helpers.py:134`)**

```python
# Current:
df['secVal'].to_csv('stocks_' + to_date_formated + '.tmp.csv')
# This runs unconditionally on every call, cluttering the working directory.
# There is no flag to suppress it (unlike save_to_file in promoterBuyBackStocks).
```

---

## Known Issues / Notes

- **Cookie expiry**: The hardcoded `Cookie` in `Session.py` expires after a few hours. Must be manually updated from a live browser NSE session.
- **`promoter.py`**: File exists in the package but is not imported anywhere — likely unused or work-in-progress.
- **`test_strategies.py`**: Test file exists but was not read — may need review.
- **Historical data**: `getHistoricalData` returns data newest-first (`data[0]` = most recent day).
- **Wedge pattern**: Returns string values (`"FW"`, `"RW"`) not booleans; use `fallingWedgePattern` / `risingWedgePattern` wrappers for bool.
