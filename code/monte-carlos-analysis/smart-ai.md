# SmartAI Strategy

## Overview

SmartAI is the default opponent in Big 2 simulations. It is a **scoring-based AI** that evaluates every valid move and picks the one with the **lowest score**.

### Core Principle

**Lowest score wins.** SmartAI tries to minimize waste by:
- Playing low cards first
- Grouping cards into combos when efficient
- Saving 2s for control
- Rushing to go out when close to winning

---

## Two Decision Modes

### 1. Leading (`_choose_lead`)
When there is no current play to beat, SmartAI decides what to lead.

### 2. Beating (`_choose_beat`)
When an opponent has played, SmartAI must find a move that beats it.

---

## Lead Scoring

When leading, each valid move gets a score based on these factors:

| Factor | Formula | Purpose |
|--------|---------|---------|
| Card value | `max_val × 10` | Prefer low cards |
| Play type | Single: `+0`, Pair: `-5`, Triple: `-10`, Two Pair: `-15`, 5-card: `-20` | Reward grouping cards together |
| End game | `+50` if ≤3 cards left after playing | Prioritize going out |
| Holding 2s | `-5` if any 2 remains in hand | Penalize hoarding 2s |

The move with the **lowest total score** is selected.

---

## Beat Scoring

When beating an opponent's play, scoring is adjusted:

| Factor | Formula | Purpose |
|--------|---------|---------|
| Card value | `max_val × 10` | Prefer low cards |
| High card penalty | `+30` if `max_val > 13` (K, A, or 2) | Avoid wasting high cards |
| End game | `+50` if ≤3 cards left after playing | Prioritize going out |
| Spend high cards | `+20` if no 2s left in remaining hand | Use high cards when safe |

---

## Examples

### Example 1: Leading

**Hand:** `[3d, 5h, 5c, 7s, ks, 2s]`

Valid moves: `SINGLE(3d)`, `SINGLE(5h)`, `SINGLE(5c)`, `SINGLE(7s)`, `SINGLE(ks)`, `SINGLE(2s)`, `PAIR(5h, 5c)`

| Move | max_val × 10 | Type Bonus | Has 2 left | Total |
|------|-------------|-----------|-----------|-------|
| `SINGLE(3d)` | 30 | 0 | -5 | **25** ← lowest |
| `SINGLE(5h)` | 50 | 0 | -5 | 45 |
| `SINGLE(5c)` | 50 | 0 | -5 | 45 |
| `PAIR(5h, 5c)` | 50 | -5 | -5 | 40 |
| `SINGLE(7s)` | 70 | 0 | -5 | 65 |
| `SINGLE(ks)` | 130 | 0 | -5 | 125 |
| `SINGLE(2s)` | 150 | 0 | 0 | 150 |

**SmartAI picks `SINGLE(3d)`** — plays the weakest card first to save stronger cards.

---

### Example 2: Beating

**Opponent played:** `SINGLE(8d)`  
**SmartAI hand:** `[3d, 9c, jh, ac, 2s]`

Valid moves to beat: `SINGLE(9c)`, `SINGLE(jh)`, `SINGLE(ac)`, `SINGLE(2s)`

| Move | max_val × 10 | High card (>13) | No 2s left bonus | Total |
|------|-------------|----------------|-----------------|-------|
| `SINGLE(9c)` | 90 | 0 | 0 | **90** ← lowest |
| `SINGLE(jh)` | 110 | 0 | 0 | 110 |
| `SINGLE(ac)` | 140 | 30 | 20 | 190 |
| `SINGLE(2s)` | 150 | 30 | — | 180 |

**SmartAI picks `SINGLE(9c)`** — the cheapest card that beats 8d, saving high cards for later.

---

### Example 3: Near the End (3 cards left)

**Hand:** `[3d, kh, 2s]`  
**Opponent played:** `SINGLE(4d)`

Valid moves: `SINGLE(kh)`, `SINGLE(2s)`

| Move | max_val × 10 | High card (>13) | Cards ≤ 3 | No 2s left | Total |
|------|-------------|----------------|-----------|-----------|-------|
| `SINGLE(kh)` | 130 | 30 | 50 | 0 | **210** ← lowest |
| `SINGLE(2s)` | 150 | 30 | 50 | — | 230 |

**SmartAI picks `SINGLE(kh)`** — even when close to winning, it prefers the king over burning the 2.

---

### Example 4: Leading with a Pair

**Hand:** `[3d, 5h, 5c, 7s, 9d, 9c]`

Valid moves include: `SINGLE(3d)`, `SINGLE(5h)`, `PAIR(5h, 5c)`, `PAIR(9d, 9c)`

| Move | max_val × 10 | Type Bonus | Has 2 left | Total |
|------|-------------|-----------|-----------|-------|
| `SINGLE(3d)` | 30 | 0 | 0 | **30** ← lowest |
| `PAIR(5h, 5c)` | 50 | -5 | 0 | **45** |
| `SINGLE(5h)` | 50 | 0 | 0 | 50 |
| `PAIR(9d, 9c)` | 90 | -5 | 0 | 85 |
| `SINGLE(7s)` | 70 | 0 | 0 | 70 |

**SmartAI picks `SINGLE(3d)`** — still prefers the absolute lowest card, but the pair comes second due to the `-5` grouping bonus.

---

### Example 5: Beating a Pair

**Opponent played:** `PAIR(6d, 6c)`  
**SmartAI hand:** `[5h, 8d, 8c, jh, jc, ac]`

Valid moves: `PAIR(8d, 8c)`, `PAIR(jh, jc)`

| Move | max_val × 10 | High card (>13) | Cards ≤ 3 | No 2s left | Total |
|------|-------------|----------------|-----------|-----------|-------|
| `PAIR(8d, 8c)` | 80 | 0 | 0 | 0 | **80** ← lowest |
| `PAIR(jh, jc)` | 110 | 0 | 0 | 0 | 110 |

**SmartAI picks `PAIR(8d, 8c)`** — cheapest pair that beats 6s.

---

## Comparison with RandomAI

| Feature | SmartAI | RandomAI |
|---------|---------|----------|
| Strategy | Score-based, optimal | Random choice |
| Card priority | Low first, save 2s | None |
| End game awareness | Yes (+50 bonus) | No |
| Grouping reward | Yes (-5 to -20) | No |
| Used in simulations | Default | Optional |

## How to Use

SmartAI is the default opponent in `sim_play.py`:

```python
from big2_ai import SmartAI
ai_players = [SmartAI() for _ in range(3)]
```

To use RandomAI instead:

```python
from big2_ai import RandomAI
ai_players = [RandomAI() for _ in range(3)]
```
