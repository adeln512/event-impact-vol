import numpy as np #type: ignore
import pandas as pd #type: ignore
import config
from events import run_events_pipeline
from volatility import realized_vol, ewma_vol

def load_returns(path: str) -> pd.DataFrame:
    return pd.read_csv(path, index_col=0, parse_dates=True)

def build_event_return_panel(returns: pd.DataFrame,
    events: pd.DataFrame,
    window: tuple[int, int],
) -> pd.DataFrame:
    t_min, t_max = window
    offsets = list(range(t_min, t_max + 1))

    trading_days = returns.index
    n_days = len(trading_days)

    rows = []

    for event_date, row in events.iterrows():
        event_type = row["event_type"]
        if event_date not in trading_days:
            continue
        i = trading_days.get_loc(event_date)

        if i + t_min < 0 or i + t_max >= n_days:
            continue

        for ticker in returns.columns:
            for k in offsets:
                d = trading_days[i + k]
                ret = returns.at[d, ticker]
                rows.append((event_date, event_type, ticker, k, ret))

    panel = pd.DataFrame(rows, columns=["event_date", "event_type", "ticker", "t", "ret"])
    return panel

def max_drawdown_from_log_returns(log_rets: pd.Series) -> float:
    log_rets = log_rets.astype(float)

    simple_rets = np.exp(log_rets) - 1.0
    wealth = (1.0 + simple_rets).cumprod()

    running_peak = wealth.cummax()
    drawdown = wealth / running_peak - 1.0

    return float(drawdown.min())

def compute_event_drawdowns(panel: pd.DataFrame) -> pd.DataFrame:
    panel_sorted = panel.sort_values(["event_date", "ticker", "t"])

    dd = (
        panel_sorted
        .groupby(["event_date", "event_type", "ticker"])["ret"]
        .apply(max_drawdown_from_log_returns)
        .reset_index(name="max_drawdown")
    )

    return dd

def compute_event_vol_shift(returns: pd.DataFrame, events: pd.DataFrame, pre_days: int = 20, post_days: int = 20, trading_days: int = 252) -> pd.DataFrame:
    trading_index = returns.index
    n = len(trading_index)

    rows = []

    for event_date, row in events.iterrows():
        event_type = row["event_type"]

        if event_date not in trading_index:
            continue

        i = trading_index.get_loc(event_date)
        if (i - pre_days) < 0:
            continue
        if (i + post_days) >= n:
            continue

        pre_slice = returns.iloc[i - pre_days : i]          
        post_slice = returns.iloc[i + 1 : i + 1 + post_days] 

        for ticker in returns.columns:
            vol_pre = realized_vol(pre_slice[ticker], trading_days=trading_days)
            vol_post = realized_vol(post_slice[ticker], trading_days=trading_days)

            ewma_pre = ewma_vol(pre_slice[ticker], lam=config.EWMA_LAMBDA, trading_days=trading_days)
            ewma_post = ewma_vol(post_slice[ticker], lam=config.EWMA_LAMBDA, trading_days=trading_days)

            ewma_change = ewma_post - ewma_pre
            ewma_ratio = ewma_post / ewma_pre if ewma_pre > 0 else np.nan


            if np.isnan(vol_pre) or np.isnan(vol_post) or vol_pre == 0:
                continue

            vol_change = vol_post - vol_pre
            vol_ratio = vol_post / vol_pre

            rows.append((event_date, event_type, ticker, vol_pre, vol_post, vol_change, vol_ratio, ewma_pre, ewma_post, ewma_change, ewma_ratio))

    out = pd.DataFrame(
        rows,
        columns=[
    "event_date",
    "event_type",
    "ticker",
    "vol_pre",
    "vol_post",
    "vol_change",
    "vol_ratio",
    "ewma_pre",
    "ewma_post",
    "ewma_change",
    "ewma_ratio",
],)

    return out


def summarize_event_panel(panel: pd.DataFrame) -> pd.DataFrame:
    t0 = panel[panel["t"] == 0].groupby(["event_type", "ticker"])["ret"].mean()

    win_1 = panel[panel["t"].between(-1, 1)].groupby(["event_type", "ticker"])["ret"].sum()
    win_3 = panel[panel["t"].between(-3, 3)].groupby(["event_type", "ticker"])["ret"].sum()

    summary = pd.concat([t0, win_1, win_3], axis=1)
    summary.columns = ["mean_ret_t0", "cum_ret_-1_+1", "cum_ret_-3_+3"]

    return summary.reset_index()

def summarize_drawdowns(drawdowns: pd.DataFrame) -> pd.DataFrame:
    return (
        drawdowns
        .groupby(["event_type", "ticker"])["max_drawdown"]
        .mean()
        .reset_index(name="mean_max_drawdown")
    )

def summarize_vol_shifts(vol_df: pd.DataFrame) -> pd.DataFrame:
    return (
        vol_df
        .groupby(["event_type", "ticker"], as_index=False)
        .agg(
    mean_vol_pre=("vol_pre", "mean"),
    mean_vol_post=("vol_post", "mean"),
    mean_vol_change=("vol_change", "mean"),
    mean_vol_ratio=("vol_ratio", "mean"),
    mean_ewma_pre=("ewma_pre", "mean"),
    mean_ewma_post=("ewma_post", "mean"),
    mean_ewma_change=("ewma_change", "mean"),
    mean_ewma_ratio=("ewma_ratio", "mean"),
)

    )



def main():
    returns = load_returns(config.RETURNS_CSV)
    events = run_events_pipeline("data/events.csv", config.PRICES_CSV)

    panel = build_event_return_panel(returns, events, window=(-3, 3))
    summary = summarize_event_panel(panel)

    drawdowns = compute_event_drawdowns(panel)
    dd_summary = summarize_drawdowns(drawdowns)

    vol_df = compute_event_vol_shift(returns, events, pre_days=20, post_days=20, trading_days=config.TRADING_DAYS)
    vol_summary = summarize_vol_shifts(vol_df)


    final_summary = summary.merge(dd_summary, on=["event_type", "ticker"], how="left")

    print(panel.head(12))
    print(final_summary)
    print(vol_df.head(12))
    print(vol_summary)



if __name__ == "__main__":
    main()
