# Cross-Asset Volatility and Risk Repricing Around U.S. Macroeconomic Announcements

## Overview

This project studies how major U.S. macroeconomic announcements—specifically **CPI releases** and **FOMC policy decisions**—affect returns, downside risk, and volatility across multiple asset classes. Rather than attempting to predict market outcomes, the objective is to understand **how markets reprice information** around scheduled macro events and how these reactions differ across assets.

CPI and FOMC announcements are well-suited for this analysis because they are:
- Widely anticipated and scheduled in advance  
- Central to monetary policy expectations  
- Highly relevant for cross-asset pricing and risk transmission  

The focus is on understanding *systematic* market behavior around macro news rather than idiosyncratic price movements.

---

## Asset Universe

The analysis spans several major asset classes to capture heterogeneous market responses:

- **U.S. Equities:** SPY, QQQ  
- **Rates:** Long-duration Treasuries (TLT)  
- **Commodities:** Gold (GLD), broad commodities (DBA)  
- **Crypto:** Bitcoin  

This cross-asset setup allows for direct comparison of how different markets absorb and reprice macroeconomic information.

---

## Methodology

### Event-Study Framework

The project employs a clean **event-study design** based on *event time* rather than calendar time:

- Each CPI or FOMC announcement is treated as **time zero**
- Returns are analyzed over a fixed window of trading days before and after each event
- Aligning events in this way allows market reactions from different periods and regimes to be compared directly

This structure isolates typical macro-announcement behavior while reducing noise from unrelated market movements.

---

### Return Analysis

Two complementary return measures are studied:

- **Event-day returns** to capture immediate price reactions  
- **Cumulative returns** over the event window to assess whether repricing is instantaneous or gradual  

This distinction helps identify whether markets adjust prices immediately or continue to process information over several days.

---

### Downside Risk: Maximum Drawdown

Average returns alone can mask significant interim losses. To capture path-dependent risk, the project computes **maximum drawdown** within each event window:

- Drawdown is calculated from the cumulative return path surrounding each macro event
- This provides a realistic measure of downside risk faced by an investor during announcement periods

This is particularly important for volatile assets where positive average returns may coexist with large temporary losses.

---

### Volatility Repricing

To study how *risk itself* is repriced around macro announcements, volatility is measured using two approaches:

- **Realized volatility:** Computed over fixed 20-day windows to capture slower-moving changes  
- **EWMA volatility:** Places greater weight on recent returns and responds more rapidly to shocks  

By comparing volatility **before and after events** under both measures, the analysis reveals not only whether volatility increases, but also **how quickly different markets react** to new information.

---

## Key Findings

- **CPI releases** are associated with higher post-event volatility in equities and Bitcoin, reflecting sensitivity to inflation and discount-rate expectations  
- Equity volatility responds more strongly to CPI than to FOMC announcements  
- Treasuries and gold exhibit more muted but asymmetric reactions  
- **Bitcoin** consistently shows the largest drawdowns and highest volatility around macro events, even when average returns are positive  
- **EWMA volatility** reacts more sharply than realized volatility, indicating rapid repricing immediately after macro news  

These results highlight the importance of downside-risk and volatility-based analysis when evaluating macro-event exposure.

---

## Interpretation and Contribution

This project demonstrates how a structured event-study framework can be used to analyze **cross-asset market behavior** around macroeconomic announcements in a transparent and reproducible way. Rather than focusing on prediction, it emphasizes:

- Risk transmission across asset classes  
- Timing and speed of volatility repricing  
- Differences in how markets process scheduled macro information  

The approach aligns closely with how macro trading desks, risk teams, and asset managers evaluate economic events.

---

## Reproducibility

All analysis is conducted using publicly available data and deterministic event windows. The project is designed to be easily extensible to:

- Additional macro announcements  
- Alternative assets  
- Intraday or higher-frequency data  

---

## Disclaimer

This project is for educational and research purposes only and does not constitute investment advice.
