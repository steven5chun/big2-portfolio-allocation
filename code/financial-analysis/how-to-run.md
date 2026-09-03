# Financial Analysis — Big 2 Monte Carlo Simulation

## Files

| File | Description |
|------|-------------|
| `ev_convergence.py` | Runs simulations and generates EV convergence graphs |
| `risk_analysis.py` | Calculates Variance, VaR(95%), Sharpe Ratio with risk analysis graphs |
| `game_rule.py` | Card deck, hand, and combination logic (pair, straight, flush, etc.) |
| `big2_game.py` | Big 2 game engine with turn logic, play validation, and game loop |
| `big2_ai.py` | SmartAI player that scores moves and picks optimal plays |
| `partition_finder.py` | Enumerates all valid ways to group a hand into legal Big 2 plays |

## Quick Start

### EV Convergence Analysis

```powershell
cd code\financial-analysis
python ev_convergence.py
```

### Risk Analysis (Variance, VaR, Sharpe Ratio)

```powershell
cd code\financial-analysis
python risk_analysis.py
```

## Configuration

Both scripts share the same config variables. Edit the top of each file to customize:

```python
# 13-card hand to analyze
PLAYER_HAND = [('3', 'd'), ('3', 'h'), ('5', 'c'), ...]

# Number of simulations per partition (more = more accurate, slower)
TOTAL_SIMS = 150

# EV convergence: number of top partitions to highlight in legend
TOP_N_LEGEND = 10

# Risk analysis: number of top partitions to show in bar chart
TOP_N = 10
```

## Output

### EV Convergence (`ev_convergence.py`)

- **Console**: Ranked summary table with Win Rate, Avg Cards Left, and EV
- **Graph**: `ev_convergence_all.png` — EV convergence lines for all partitions with top 10 highlighted

### Risk Analysis (`risk_analysis.py`)

- **Console**: Ranked summary table with EV, Std Dev, VaR(95%), and Sharpe Ratio
- **Graphs**:
  - `risk_return_scatter.png` — Risk (Std Dev) vs Return (EV) scatter plot, bubble size = Sharpe Ratio
  - `risk_histogram.png` — Return distribution histogram for the top Sharpe partition with VaR marker
  - `sharpe_bar_chart.png` — Sharpe Ratio ranking bar chart for top 20 partitions

## Dependencies

```
numpy
matplotlib
```