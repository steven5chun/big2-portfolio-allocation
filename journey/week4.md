# Week 4 - Design Phase: Monte Carlo Simulation for Big 2

## Big 2 Cards Combinations (or partitions)

Each card has two parts: value and suit.

**Values** (lowest to highest): `3, 4, 5, 6, 7, 8, 9, 10, J, Q, K, A, 2`

**Suits** (lowest to highest): Diamonds < Clubs < Hearts < Spades

Example: 3 of Diamonds is the lowest card, 2 of Spades is the highest.


Big 2 card combination type

| Type | Cards | Description |
|------|-------|-------------|
| SINGLE | 1 | Any card |
| PAIR | 2 | Same rank |
| TRIPLE | 3 | Same rank |
| TWO_PAIR | 4 | Two distinct pairs |
| STRAIGHT | 5 | 5 consecutive, mixed suits |
| FLUSH | 5 | Same suit |
| FULL_HOUSE | 5 | Triple + pair |
| FOUR_OF_A_KIND | 5 | Quad + kicker |
| STRAIGHT_FLUSH | 5 | Consecutive + same suit |


## The Design of a Monte Carlo Simulation for Big 2 

The goal of this project is to use Monte Carlo simulation to find the best way to arrange cards in Big 2 and maximize expected value.

Monte Carlo simulations need a well-designed environment. In a real Big 2 game, it's too complex to model everything because we can't see other players' cards, there are too many possible card combinations, and players behave differently. To make the simulation fast and practical, we focus on the most important factors and keep other things simple.

***

### Key Simulation Assumptions & Constraints

*   **Same Strategy for All Players:** To avoid unpredictable results from different play styles, all players use the same simple rule-based strategy. The strategy is: play low cards first, group cards into combinations when possible, save 2s for important moments, and try to empty your hand quickly when you're close to winning.
  
*   **Smaller Hand Size:** Each player starts with **8 cards** instead of 13. This makes the simulation much faster while still keeping the core game mechanics intact.

*   **Fixed Hand, Random Opponents:** The player's 8-card hand stays the same across all simulations. To fairly test how good that hand is, the remaining cards are randomly shuffled and dealt to opponents in each simulation run.



## Big 2 game engine

The game works like this:

1. **Find the starting player** — Whoever has the 3 of diamonds goes first. If no one has it, we pick a random player.

2. **Each player takes a turn:**
   - If it's the first turn and you have the 3 of diamonds, you must play it first (this is a Big 2 rule)
   - If you're starting a new round (no one has played yet), you play the first card grouping from your plan
   - If someone else just played and you need to beat them, you look through your remaining card groupings for valid plays and pick the best one
   - If you can't beat the current play, you pass

3. **When you play cards:** They're removed from your hand and from your plan. The "current play" is updated to what you just played.

4. **When everyone passes:** If 3 players pass in a row, the round ends. The last player who actually played cards gets to start the next round with any play they want.

5. **Winning the game:** The first player to empty their hand wins. If 200 turns pass with no winner, the game stops.

6. **Game result:** We record which player won and how many cards each player had left.


## Computer Player

All 4 players in the simulation use the same strategy. Each player has a plan (their card groupings) and follows these rules:

- **Starting a round:** Play the first card grouping from your plan
- **Beating someone's play:** Look through your remaining groupings for valid plays, pick the one that costs the least (save your high cards)
- **Can't beat the play:** Pass
- **Close to winning (3 cards left):** Rush to empty your hand

The simulation has two AI modes:

***SmartAI*** — Plays strategically. Always picks the lowest-cost move, plays low cards first, groups cards efficiently, saves 2s for important moments, and rushes to win when close.

***RandomAI*** — Plays randomly. Just picks any valid move without thinking. We use this to compare against SmartAI and see how much better strategy performs.

- [Computer player explanation](../code/monte-carlos-analysis/smart-ai.md)


## Expected value (EV) of big 2 game

Expected Value (EV) is the average outcome if you repeat the same situation many times. In Big 2, we measure EV in points won or lost per hand.

$$
EV = \frac{1}{N} \sum_{i=1}^{N} P_{i}
$$

*   **$N$** = Total number of simulated games (e.g., 3,000)
*   **$P_{i}$** = The score of game $i$.
    *   If you win, $P_{i}$ is **positive** (the total cards left in your opponents' hands).
    *   If you lose, $P_{i}$ is **negative** (the cards left in your hand, with a double penalty).

Example 1
- You win 40% of the time (+13 points from opponents).
- You lose 60% of the time, but because your hand is weak, you get stuck with 10 cards (2× penalty = -20 points).
- Win Rate: 40%
- Expected Value: \((0.40 x 13) + (0.60 x -20) = 5.2 - 12.0 = -6.8 points

Example 2
- You win only 35% of the time (+13 points).
- You lose 65% of the time, but because your hand is flexible, you usually get rid of most cards, leaving only 2 cards when the winner finishes (-2 points).
- Win Rate: 35%
- Expected Value: \((0.35 x 13) + (0.65 x -2) = 4.55 - 1.3 = +3.25 points

**Note:** This EV formula is simplified. In real Big 2, the penalty system is more complex—holding more cards at the end means much bigger losses due to double and triple penalties.

Just looking at win rate isn't enough. The cards left in your hand create big swings in your score. That's why we use EV—it tells us the average points we expect to win or lose, not just whether we win or lose. This is similar to how investors look at expected returns and risk in finance.

## Design of Monte Carlo simulation

The Monte carlos simuluation runs thousands of games to find which card grouping strategy gives the best expected value.

### Simulation Pipeline

1. **Fixed hand input** — The player's hand stays the same in all simulations. Test hand: `[3d, 5h, 5c, 7s, ks, 8d, 8c, 2d]` (8 cards with a pair of 5s, a pair of 8s, and a 2).

2. **Find all card groupings** — The program finds every valid way to group the hand into Big 2 plays. For this hand, the top 5 groupings are:
   - `[5c,5h,8d,8c] + 4 singles` — play two pair first, then singles
   - `[5c,5h] + [8d,8c] + 4 singles` — play pairs separately, then singles
   - `[5c,5h] + 6 singles` — play one pair first, then singles
   - `[8d,8c] + 6 singles` — play the other pair first, then singles
   - `8 singles` — play every card individually

3. **Random opponent hands** — For each game, the remaining 24 cards are shuffled and dealt to 3 opponents (8 cards each). Each opponent also gets a random card grouping, so everyone plays with a plan.

4. **Play the game** — All 4 players use SmartAI with their card groupings:
   - **3d rule**: On the first turn, whoever has 3d must play it first
   - **Leading**: Play the first combo from your grouping
   - **Beating**: Look through your remaining combos for valid plays, pick the best one
   - **No valid play**: Pass

5. **Track progress** — Record three numbers at 100, 500, 1000, 1500, 2000, 2500, and 3000 games:
   - **Win Rate**: How often you win
   - **Average Cards Left**: How many cards you have when the game ends
   - **Expected Value (EV)**: Average points per hand
     - Win: Points = total cards left in opponents' hands
     - Lose: Points = -2 × cards left in your hand

6. **Rank and visualize** — Sort groupings by final EV (best first), pick top 5, and create 4 graphs showing how results stabilize over time.

## Takeaway

Monte Carlo simulation works because it tests each card grouping against many different opponent hands. Instead of guessing which grouping is best, you play thousands of realistic games and let the data show you the winner.

The graphs show that results become stable after enough games. The **Expected Value (EV) framework** is better than just looking at win rate because it accounts for risk. Instead of just asking "Do I win or lose?", EV tells us "How many points do I expect to win or lose on average?" This is similar to how investors evaluate portfolios—they don't just look at whether they win, but how much they win or lose on average.
