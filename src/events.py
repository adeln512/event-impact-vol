import pandas as pd #type: ignore
from pathlib import Path
import config

ALLOWED_EVENT_TYPES = {"CPI", "FOMC"}

def load_events(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    bad = set(df["Event"].unique()) - ALLOWED_EVENT_TYPES
    if bad:
        raise ValueError(f"Unknown event types found: {bad}")
    if 'Date' not in df.columns or 'Event' not in df.columns:
        raise ValueError("Events CSV must contain 'Date' and 'Event' columns.")
    df['Date'] = pd.to_datetime(df['Date'])
    df = df[df['Event'].isin(ALLOWED_EVENT_TYPES)]
    df = df.sort_values('Date').reset_index(drop=True)
    df = df.set_index('Date')
    df = df.rename(columns={"Event": "event_type"})
    return df

def map_events_to_tdays(events: pd.DataFrame, trading_days: pd.DatetimeIndex) -> pd.DataFrame:
    mapped_events = []
    for event_date, row in events.iterrows():
        if event_date in trading_days:
            mapped_events.append((event_date, row["event_type"]))
        else:
            future_tdays = trading_days[trading_days > event_date]
            if not future_tdays.empty:
                next_tday = future_tdays[0]
                mapped_events.append((next_tday, row["event_type"]))
    mapped_df = pd.DataFrame(mapped_events, columns=['Date', "event_type"]).set_index('Date')
    return mapped_df

def run_events_pipeline(events_path: str, prices_csv: str) -> pd.DataFrame:
    events = load_events(events_path)
    prices = pd.read_csv(prices_csv, index_col=0, parse_dates=True)
    trading_days = prices.index
    events = map_events_to_tdays(events, trading_days)
    return events

if __name__ == "__main__":
    events = run_events_pipeline("data/events.csv", config.PRICES_CSV)
    print(events.head(10))
    print(events["event_type"].value_counts())
