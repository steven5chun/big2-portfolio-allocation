# Big 2 Game Play - Monte Carlos Convergence Analysis

## What This Does

This tool runs Monte Carlo simulations to find the **best way to play your Big 2 hand**. It tests every valid way to split your cards into combinations (pairs, straights, singles, etc.) and measures which strategy wins most often.

### Key Features

- **Fixed hand testing** - Uses a predefined hand so results are reproducible and comparable
- **Convergence tracking** - Records win rate and average cards left at milestones (100, 500, 1000, 1500, 2000, 2500, 3000 iterations)
- **Visual graphs** - Generates charts showing how metrics stabilize as more simulations run
- **Top N ranking** - Shows only the best partitions to keep output readable

### Output

| File | Description |
|------|-------------|
| `results/convergence_winrate.png` | Multi-line chart showing win rate convergence for each top partition |
| `results/convergence_cards_left.png` | Multi-line chart showing average cards left convergence |
| `results/final_ranking.png` | Bar chart comparing final win rates of top partitions |
| `results/convergence_results.csv` | Raw data for all milestones in spreadsheet format |

## How to Run

### Prerequisites

```bash
pip install matplotlib
```

### Run the Analysis

```bash
python sim_play.py
```

This will:
1. Find all valid partitions for the configured hand
2. Run 3,000 simulations per partition against 3 Smart AI opponents
3. Print a progress table with win rates and ETA
4. Display top partitions with metrics at each milestone
5. Generate 3 graphs and a CSV in the `results/` folder

## Configuration

Edit the **CONFIG section** at the top of `sim_play.py`:

```python
PLAYER_HAND = [('3', 'd'), ('5', 'h'), ('5', 'c'), ('7', 's'), ('k', 's')]
OPP_CARDS = 5
ITERATIONS = [100, 500, 1000, 1500, 2000, 2500, 3000]
TOP_N = 5
MAX_PARTITIONS = 500
```

### Config Options

| Setting | What It Does | Example |
|---------|-------------|---------|
| `PLAYER_HAND` | Your 5-card hand to test | Change to any 5 cards |
| `OPP_CARDS` | How many cards each AI opponent has | 8 (default), try 5 for easier games |
| `ITERATIONS` | Milestones to track during simulation | Add/remove values as needed |
| `TOP_N` | Number of best partitions to display and graph | 5 (default), increase to see more |
| `MAX_PARTITIONS` | Cap on partitions to search (prevents slowdown) | 500 (default) |

### Card Format

Cards are tuples: `(value, suit)`

**Values**: `'3'`, `'4'`, `'5'`, `'6'`, `'7'`, `'8'`, `'9'`, `'10'`, `'j'`, `'q'`, `'k'`, `'a'`, `'2'`
- Integer ranking: `3-10` = 3-10, `j`=11, `q`=12, `k`=13, `a`=14, `2`=15

**Suits**: `'d'` (diamonds) < `'c'` (clubs) < `'h'` (hearts) < `'s'` (spades)

Example: `('3', 'd')` = 3 of Diamonds, `('a', 's')` = Ace of Spades

## Understanding Results

### Console Output

```
#1 5 singles (3d, 5c, 5h, 7s, ks)
    Iters     Win Rate     Avg Left
      100       26.0%         1.42
      500       26.4%         1.43
     1000       28.1%         1.39
     ...
     3000       28.2%         1.39
```

- **Win Rate** - Percentage of games won at this milestone
- **Avg Left** - Average cards remaining when the game ends (lower = better)
- **Convergence** - Values should stabilize as iterations increase

### Graphs

1. **Win Rate Convergence** - Lines that flatten indicate stable estimates
2. **Avg Cards Left** - Shows consistency of card-clearing efficiency
3. **Final Ranking** - Bar chart comparing all top partitions side by side

## Interpreting Partitions

A **partition** is a way to group your cards into valid Big 2 plays:

- `5 singles (3d, 5c, 5h, 7s, ks)` - Play each card individually
- `[5c, 5h] + 3 singles (3d, 7s, ks)` - Play the pair first, then singles

The analysis tells you which grouping wins most often.
