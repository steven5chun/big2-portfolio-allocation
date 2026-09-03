# Week 6

## Financial Theories on Portfolio management

## Summary

In both strategic gameplay and financial investing, agents are inherently loss-averse; focusing solely on the probability of winning is an incomplete strategy. A robust optimization model must concurrently evaluate the probability and systemic impact of losing. Therefore, any rational decision-making framework must balance upside potential against downside risk. Quantitative metrics—specifically volatility, Risk and the Sharpe Ratio—serve as ideal tools to analyze risk exposure and outcome impacts across different card combinations or asset portfolios.



#### 1. Modern Portfolio Theory (MPT) [[1](https://www.youtube.com/watch?v=InJ1alATnRw)]
*   **Definition:** A Nobel Prize-winning framework introduced by Harry Markowitz that optimizes a basket of assets. It proves that an asset's risk and return should not be assessed in isolation, but by how it contributes to an entire portfolio’s collective behavior.
*   **The Efficient Frontier:** The mathematical curve representing portfolios that offer the highest expected return for a defined level of risk. Any allocation sitting below this line is inefficient.

#### 2. Variance & Volatility (σ² and σ)
*   **Definition:** Variance (σ²) calculates how far an asset’s returns scatter around its historical mean. Standard Deviation (σ), or Volatility, is the square root of variance. High volatility implies wide, unpredictable price swings.

#### 3. Value at Risk (VaR) [[2](https://www.youtube.com/watch?v=a1f-Zso8spk)]
*   **Definition:** Value at Risk (VaR) is a standardized financial metric that measures the maximum expected loss an asset or portfolio could face under normal market conditions within a specific timeframe and at a set confidence level.

#### 4. Sharpe Ratio  [[3](https://www.youtube.com/watch?v=B7XbE5UelKk&t=39s)] [[4](https://www.youtube.com/watch?v=9HD6xo2iO1g&t=228s)]

*   **Definition:** A quantitative metric that measures the excess return earned per unit of volatility. It determines whether high returns are due to intelligent asset selection or dangerous, uncompensated gambling. 


    $$\text{Sharpe Ratio} = \frac{\text{Expected Portfolio Return } (R_p) - \text{Risk-Free Rate } (R_f)}{\text{Portfolio Standard Deviation } (\sigma_p)}$$


    A higher Sharpe ratio is always better. It means an investment gives you more return for each unit of risk or price jump you take.
    
    What the Numbers Mean
    
    - Above 1.0: Good. The fund gives a solid return for the risk you take.
    - Above 2.0: Very good. The returns are high while risk stays low.
    - 3.0 or higher: Excellent. Rare and outstanding.
    - Under 1.0: Low or poor. You do not get paid enough extra return for the danger.
    - Zero or negative: Bad. Safe bank savings or bonds pay better than this choice
    
## Financial Analogue to the Big 2 Game
In a Big 2 simulation, the Sharpe ratio measures the consistency and safety of a card combination strategy.

Instead of just telling you how often a strategy wins (win rate), the Sharpe ratio tells you how much risk you had to take to get those wins.Because Big 2 scoring penalizes you exponentially for the number of cards left in your hand (e.g., doubling your penalty if you hold 10+ cards, or tripling it for 13 cards), a high win rate alone can be deceptive. 

### Interpreting the Numbers in Big 2

- Negative Sharpe Ratio (< 0): The strategy is a net-loser. You are losing more points to penalties when you fail than you are gaining when you win. Avoid this combination.
- Low Sharpe Ratio (0 to 1.0): The strategy yields positive points over time, but it is highly volatile. This represents a high-risk, "all-or-nothing" strategy (e.g., saving a Royal Flush but getting trapped with 11 cards in hand if someone else goes out first).
- High Sharpe Ratio (> 1.0): The strategy is incredibly stable. It gives you reliable point gains while heavily mitigating catastrophic losses. This is your "best" card combination strategy.

### Win Rate vs. Sharpe Ratio: 
- A Big 2 Example    
    - Strategy A: "The Gambler" (High Win Rate, Low Sharpe Ratio)
        - Approach: You hold back your single 2s and Aces to build a massive 5-card combo for later in the game.
        - Result: You win 60% of games.
        - The Catch: In the 40% of games where you lose, you get completely locked out. You are left holding 10+ cards, leading to a massive double-point penalty.
        - Sharpe Ratio Meaning: Low. The average return is positive, but the standard deviation (volatility) is massive because of those crushing double-point losses.
    - Strategy B: "The Grinder" (Lower Win Rate, High Sharpe Ratio)
        - Approach: You aggressively play your single high cards early to maintain control and shed cards as fast as possible.
        - Result: You win 48% of games. 
        - The Catch: When you lose, you almost manage to get down to just 1 or 2 cards left in your hand, meaning your point penalty is tiny.
        - Sharpe Ratio Meaning: High. Even though you win less often, your losses are tightly controlled. Your downside risk is minimized.

## Reference

- [1] [Modern Portfolio Theory Explained: The Math Behind Diversification](https://www.youtube.com/watch?v=InJ1alATnRw)
- [2] [Value at Risk (VaR) Explained: A Comprehensive Overview](https://www.youtube.com/watch?v=a1f-Zso8spk)
- [3] [What is the Sharpe Ratio? Risk-Adjusted Returns Explained](https://www.youtube.com/watch?v=B7XbE5UelKk&t=39s)
- [4] [The Sharpe Ratio Explained (by a quant trader)](https://www.youtube.com/watch?v=9HD6xo2iO1g&t=228s)
- [5] [Monte Carlo Simulation of a Stock Portfolio with Python](https://www.youtube.com/watch?v=6-dhdMDiYWQ)
- [6] [Value at Risk (VaR) In Python: Monte Carlo Method](https://www.youtube.com/watch?v=X8aNFXJEENs)
