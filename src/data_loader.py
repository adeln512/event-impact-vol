from pathlib import Path
import pandas as pd #type: ignore
import numpy as np #type: ignore
import yfinance as yf #type: ignore

import config

def fetch_prices(tickers: list[str], start: str, end: str | None) -> pd.DataFrame:
    raw = yf.download(tickers = tickers, start = start, end = end, auto_adjust = False, progress = False, group_by="column")
    price_field = None
    if isinstance(raw.columns, pd.MultiIndex):
        available_fields = set(raw.columns.get_level_values(0))
        for field in config.PRICE_FIELD_PREFERENCE:
            if field in available_fields:
                price_field = field
                break
        if price_field is None:
            raise ValueError(f"No preferred price field found. Available: {sorted(available_fields)}")
        prices = raw[price_field]
    else:
        for field in config.PRICE_FIELD_PREFERENCE:
            if field in raw.columns:
                price_field = field
                break
        if price_field is None:
            raise ValueError(f"No preferred price field found. Available: {list(raw.columns)}")
        prices = raw[price_field]

    prices = prices.reindex(columns=tickers)
    return prices



def clean_prices(prices: pd.DataFrame) -> pd.DataFrame:
    prices = prices.copy()
    prices.index = pd.to_datetime(prices.index)
    prices = prices.sort_index()
    prices = prices[~prices.index.duplicated(keep='first')]

    bdays = pd.date_range(prices.index.min(), prices.index.max(), freq='B')
    prices = prices.reindex(bdays)

    prices = prices.ffill()
    return prices

def compute_log_returns(prices: pd.DataFrame) -> pd.DataFrame:
    return np.log(prices / prices.shift(1))

def save_dataset(df: pd.DataFrame, path: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index = True)

def run_data_pipeline():
    prices = fetch_prices(config.TICKERS, config.START_DATE, config.END_DATE)
    prices = clean_prices(prices)
    returns = compute_log_returns(prices)

    save_dataset(prices, config.PRICES_CSV)
    save_dataset(returns, config.RETURNS_CSV)

    return prices, returns

if __name__ == "__main__":
    prices, returns = run_data_pipeline()
    print("Saved:", config.PRICES_CSV, config.RETURNS_CSV)
    print("Prices shape:", prices.shape)
    print("Returns shape:", returns.shape)
    print(prices.tail())
    print(returns.tail())
