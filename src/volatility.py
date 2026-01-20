from __future__ import annotations

import numpy as np # type: ignore
import pandas as pd # type: ignore


def realized_vol(
    returns: pd.Series | np.ndarray,
    trading_days: int = 252,
    ddof: int = 1,
) -> float:
    r = np.asarray(returns, dtype=float)

    r = r[~np.isnan(r)]
    if r.size < 2:
        return float("nan")

    daily_std = r.std(ddof=ddof)
    ann_vol = daily_std * np.sqrt(trading_days)
    return float(ann_vol)


def ewma_vol(
    returns: pd.Series | np.ndarray,
    lam: float = 0.94,
    trading_days: int = 252,
) -> float:
    
    if not (0.0 < lam < 1.0):
        raise ValueError("lam must be between 0 and 1 (exclusive).")

    r = np.asarray(returns, dtype=float)

    r = r[~np.isnan(r)]
    if r.size < 2:
        return float("nan")

    var = np.var(r, ddof=1)

    for x in r:
        var = lam * var + (1.0 - lam) * (x ** 2)

    ann_vol = np.sqrt(var * trading_days)
    return float(ann_vol)
