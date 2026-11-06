# Week 7 - Financial Analysis Code

## Overview

This document explains the Python code used for financial analysis of Big 2 card combinations. The analysis framework evaluates different card combination strategies using Monte Carlo simulation and calculates risk-adjusted performance metrics.

## Expected Value (EV)

EV measures the probability-weighted average of points won or lost per hand:

- **Win**: You gain points equal to the sum of opponents' remaining cards
- **Lose**: You lose points = `-2 × your remaining cards` (double penalty)

**Positive EV** means the strategy is profitable long-term. **Negative EV** means it loses points on average.

## How It Works

1. **Partition Enumeration** — Finds every valid way to group the 13-card hand into legal Big 2 plays (e.g., pairs, straights, singles)
2. **Simulation Loop** — For each combination:
   - Deals 13 random cards to 3 opponents (standard Big 2 rules)
   - Runs 300 full games with all players using SmartAI
   - Records each game's point outcome (Pi)
3. **Reproducibility** — Fixed random seed (`random.seed(42)`) ensures identical results across runs
4. **Ranking** — Sorts partitions by EV or Sharpe Ratio (descending)
5. **Visualization** — Generates convergence curves, scatter plots, histograms, bar charts, and Efficient Frontier

## Code: [ev_convergence.py](../code/financial-analysis/ev_convergence.py)

This script tracks how Expected Value stabilizes as more simulations run.

**Configuration:**
```python
PLAYER_HAND = [('3', 'd'), ('3', 'h'), ('5', 'c'), ('5', 's'), ('8', 'd'), ('9', 'h'), 
               ('10', 'c'), ('j', 'd'), ('q', 'h'), ('k', 's'), ('a', 'd'), ('2', 'c'), ('2', 's')]
OPP_CARDS = 13
TOTAL_SIMS = 300
```

**Test Hand:** The simulation evaluates how to optimally arrange this 13-card hand:
- **Hand:** `[3d, 3h, 5c, 5s, 8d, 9h, 10c, jd, qh, ks, ad, 2c, 2s]`

**Core Function:**
```python
def run_simulations(player_hand, partition, total_sims, opp_cards):
    ev_values = []
    total_ev = 0
    wins = 0
    total_cards_left = 0

    for sim in range(1, total_sims + 1):
        # Deal random cards to opponents
        deck = Deck()
        all_cards = [c for c in deck.cards if c not in player_hand]
        random.shuffle(all_cards)
        
        opponent_hands = []
        idx = 0
        for _ in range(3):
            opponent_hands.append(all_cards[idx:idx + opp_cards])
            idx += opp_cards

        # Generate random partitions for opponents
        ai_partitions = []
        for oh in opponent_hands:
            opp_partitions = find_all_partitions(oh, max_partitions=50)
            ai_partitions.append(random.choice(opp_partitions))

        all_partitions = [partition] + ai_partitions

        # Run game
        game = Big2Game([player_hand] + opponent_hands, partition_orders=all_partitions)
        ai_players = [SmartAI() for _ in range(4)]
        winner, cards_left = game.simulate_with_partition(all_partitions, ai_players)

        # Calculate points
        if winner == 0:
            wins += 1
            pi = sum(cards_left[1:])  # Sum of opponents' remaining cards
        else:
            pi = -2 * cards_left[0]  # Double penalty on your remaining cards

        total_ev += pi
        total_cards_left += cards_left[0]
        ev_values.append(total_ev / sim)  # Cumulative EV at each step

    return ev_values, wins / total_sims, total_cards_left / total_sims, total_ev / total_sims
```

**Visualization:**
```python
def plot_ev_convergence(all_results, total_sims, colors):
    # Plots EV convergence lines for all 66 partitions
    # Highlights top 10 partitions with thicker lines and labels
    # Shows break-even line at EV = 0
    # Saves to ev_convergence_all.png
```

**Output:**
- Console: Ranked summary table with Win Rate, Avg Cards Left, and EV
- Graph: `ev_convergence_all.png` — EV convergence lines for all partitions

## Code: [risk_analysis.py](../code/financial-analysis/risk_analysis.py)

This script calculates risk metrics (variance, VaR, Sharpe ratio) and identifies the Efficient Frontier.

**Core Function:**
```python
def run_risk_simulation(player_hand, partition, total_sims, opp_cards):
    pi_values = []  # Individual game outcomes
    wins = 0
    total_cards_left = 0

    for sim in range(1, total_sims + 1):
        # ... same game setup as ev_convergence.py ...
        
        if winner == 0:
            wins += 1
            pi = sum(cards_left[1:])
        else:
            pi = -2 * cards_left[0]

        pi_values.append(pi)  # Store each game's outcome
        total_cards_left += cards_left[0]

    return pi_values, wins / total_sims, total_cards_left / total_sims
```

**Risk Metrics Calculation:**
```python
def calculate_risk_metrics(pi_values):
    arr = np.array(pi_values)
    mean_ev = np.mean(arr)           # Expected Value
    variance = np.var(arr)           # Variance
    std_dev = np.std(arr)            # Standard Deviation (risk)
    var_95 = np.percentile(arr, 5)   # Value at Risk (95% confidence)
    sharpe = mean_ev / std_dev if std_dev > 0 else 0.0  # Sharpe Ratio

    return {
        'ev': mean_ev,
        'variance': variance,
        'std_dev': std_dev,
        'var_95': var_95,
        'sharpe': sharpe,
    }
```

**Efficient Frontier:**
```python
def find_efficient_frontier(all_risk_results):
    sorted_results = sorted(all_risk_results, key=lambda x: x['metrics']['std_dev'])
    frontier = []
    max_ev = float('-inf')
    for r in sorted_results:
        ev = r['metrics']['ev']
        if ev >= max_ev:
            frontier.append(r)
            max_ev = ev
    return frontier
```

The Efficient Frontier identifies partitions that offer the best expected return for a given level of risk. A partition is on the frontier if no other partition provides higher EV for the same or lower risk.

**Visualization Functions:**

1. **plot_risk_return_scatter()** — Risk (Std Dev) vs Return (EV) scatter plot with Efficient Frontier overlay
2. **plot_efficient_frontier()** — Clean view showing only optimal partitions on the frontier curve
3. **plot_return_histogram()** — Return distribution histogram for top Sharpe partition with VaR marker
4. **plot_sharpe_bar_chart()** — Sharpe Ratio ranking bar chart for top 20 partitions

## Other Codes: Big 2 Game rule and engine
Refer to [week5.md](./week5.md)

## Document: [how-to-play.md](../code/financial-analysis/how-to-run.md)

This document explains how to run the Monte Carlo simulations.

**Prerequisites:**
```bash
pip install matplotlib
```

**Run the Analysis:**
```bash
python sim_play.py
```

**Configuration Options:**

| Setting | What It Does | Example |
|---------|-------------|---------|
| `PLAYER_HAND` | Your 13-card hand to test | Change to any 13 cards |
| `OPP_CARDS` | How many cards each AI opponent has | 13 (standard Big 2 rules) |
| `ITERATIONS` | Milestones to track during simulation | Add/remove values as needed |
| `TOP_N` | Number of best partitions to display and graph | 5 (default), increase to see more |
| `MAX_PARTITIONS` | Cap on partitions to search (prevents slowdown) | 500 (default) |

**Card Format:**
Cards are tuples: `(value, suit)`
- Values: `'3'`, `'4'`, ..., `'10'`, `'j'`, `'q'`, `'k'`, `'a'`, `'2'`
- Suits: `'d'` (diamonds) < `'c'` (clubs) < `'h'` (hearts) < `'s'` (spades)

Example: `('3', 'd')` = 3 of Diamonds, `('a', 's')` = Ace of Spades

See [how-to-play.md](../code/monte-carlos-analysis/how-to-play.md) for complete documentation.
