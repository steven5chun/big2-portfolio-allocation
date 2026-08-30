# Week 6

## Financial Theories on Portfolio management

#### 1. Modern Portfolio Theory (MPT)
*   **Definition:** A Nobel Prize-winning framework introduced by Harry Markowitz that optimizes a basket of assets. It proves that an asset's risk and return should not be assessed in isolation, but by how it contributes to an entire portfolio’s collective behavior.
*   **The Efficient Frontier:** The mathematical curve representing portfolios that offer the highest expected return for a defined level of risk. Any allocation sitting below this line is inefficient.

#### 2. Variance & Volatility (σ² and σ)
*   **Definition:** Variance (σ²) calculates how far an asset’s returns scatter around its historical mean. Standard Deviation (σ), or Volatility, is the square root of variance. High volatility implies wide, unpredictable price swings.

#### 3. Downside Risk
*   **Definition:** The specific probability that an investment's actual return will fall below its expected value, resulting in financial loss. Unlike general volatility (which tracks both up and down swings), downside risk focuses strictly on worst-case scenarios.

#### 4. Sharpe Ratio

*   **Definition:** A quantitative metric that measures the excess return earned per unit of volatility. It determines whether high returns are due to intelligent asset selection or dangerous, uncompensated gambling. 


    $$\text{Sharpe Ratio} = \frac{\text{Expected Portfolio Return } (R_p) - \text{Risk-Free Rate } (R_f)}{\text{Portfolio Standard Deviation } (\sigma_p)}$$


    A higher Sharpe ratio is always better. It means an investment gives you more return for each unit of risk or price jump you take.
    
    What the Numbers Mean
    
    - Above 1.0: Good. The fund gives a solid return for the risk you take.
    - Above 2.0: Very good. The returns are high while risk stays low.
    - 3.0 or higher: Excellent. Rare and outstanding.
    - Under 1.0: Low or poor. You do not get paid enough extra return for the danger.
    - Zero or negative: Bad. Safe bank savings or bonds pay better than this choice
    


## Translating Financial Metrics to Big 2 Allocation

When splitting a hand in Big 2, you are managing a **fixed capital pool** (your cards). Below is the direct structural alignment:

| Financial Metric | Capital Market Context | Big 2 Systemic Analogy |
| :--- | :--- | :--- |
| **Asset Allocation** | Dividing wealth into Stocks, Bonds, and Commodities to maximize returns. | Dividing a 13-card hand into sub-combos (e.g., *Full House + Pair* vs. *Straight + Trips*). |
| **Monte Carlo Simulation** | Running many random market pathways to stress-test an investment portfolio. | Running many random opponent deals to test how a **fixed hand split** holds up against variance. |
| **Variance / Volatility** | The intensity of asset price fluctuations over a given period. | **Sensitivity to Opponent Distribution:** How wildly your win rate swings depending on what opponents hold. |
| **Downside Risk** | The likelihood of losing capital or suffering a portfolio crash. | **The Penalty Risk:** The probability of failing to gain control, getting blocked, and taking double/triple point penalties. |
| **Risk-Free Rate ($R_f$)** | The baseline return of a zero-risk asset (e.g., US Treasury Bonds). | **Pass Baseline:** The average points lost by passively passing versus actively contesting a round. |
| **Sharpe Ratio** | Risk-adjusted efficiency of a portfolio. | **Game Efficiency Score:** Evaluating if a card split yields a high win rate safely (High Sharpe) or relies on luck (Low Sharpe). |


## Reference

- [1] [Monte Carlo Simulation of a Stock Portfolio with Python](https://www.youtube.com/watch?v=6-dhdMDiYWQ)
- [2] [Value at Risk (VaR) In Python: Monte Carlo Method](https://www.youtube.com/watch?v=X8aNFXJEENs)
