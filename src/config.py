TICKERS = ["SPY", "QQQ", "TLT", "GLD", "DBA", "BTC-USD"]

TICKER_NAMES = {"SPY": "US Equities (SPY)",
                "QQQ": "US Growth (QQQ)",
                "TLT": "Long Treasuries (TLT)",
                "GLD": "Gold (GLD)",
                "DBA": "Commodities (DBA)",
                "BTC-USD": "Bitcoin (BTC-USD)"
                }

DATA_SOURCE = "yfinance"
PRICE_FIELD_PREFERENCE = ["Adj Close", "Close"]
START_DATE = "2016-01-01"
END_DATE = None
RETURN_TYPE = "log"
TRADING_DAYS = 252
ROLLING_WINDOWS = [20, 60, 120]
EWMA_LAMBDA = 0.94

DATA_DIR = "data"
PRICES_CSV = f"{DATA_DIR}/prices.csv"
RETURNS_CSV = f"{DATA_DIR}/returns.csv"
