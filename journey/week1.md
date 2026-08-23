# Week 1
## Summmary
- Introduction to Big 2: Understanding the core rules, card rankings, and gameplay of Big 2.
- Probability Calculations: Using mathematical formulas to calculate the probability of specific card distributions and identifying impossible combinations.
- The Monte Carlo Method: Exploring how the Monte Carlo simulation method can be applied to model game outcomes and determine strategy.

## What is Monte Carlos Simulation
Monte Carlo Simulation is a mathematical technique used to estimate the possible outcomes of an uncertain event by modeling the probability of different outcomes using random sampling. It acts like a way to look into the future to make better business, investment, and planning decisions.

### Who uses it
It is widely applied in portfolio management, investment planning, risk analysis, option pricing, and capacity planning. It is also used across diverse fields such as medicine, astrophysics, and even solving Wordle puzzles

### Accuracy
Running the simulation repeatedly provides standard deviation and variance metrics, ensuring that the more you sample, the more accurate your future estimation becomes

### The 3 Core Steps to Run a Simulation
1. ***Set up the predictive model:*** Identify the dependent variable you want to predict and the independent variables (input risks or predictive factors) that will drive those predictions
2. ***Specify the probability distribution:*** Define a range of likely values and assign probability weights for the independent variables using historical data or subjective expert judgment.
3. ***Run simulations repeatedly:*** Generate random values for the independent variables repeatedly until you gather a large enough sample size to represent the near-infinite combinations of outcomes

## Different between Monte Carlos Tree Search (MCTS) and Monte Carlos Simulation (MCS)
The fundamental difference is that Monte Carlo Simulation (MCS) is a statistical tool used to calculate static probabilities and risk, while Monte Carlo Tree Search (MCTS) is an AI search algorithm designed to make optimal sequential choices.

| Feature | Monte Carlo Simulation (MCS) | Monte Carlo Tree Search (MCTS) |
| :---------------- | :------: | ----: |
| Primary Goal | Forecast overall risk, outcomes, or values. | Find the single best next move or decision. |
| Structure | Flat / ***No Structure***. Evaluates completely independent random samples. | ***Tree Structure.*** Dynamically builds a memory tree of moves and game states. |
| Decision Logic | Passive sampling. Samples randomly from fixed probability distributions. | Active learning. Uses formulas (like UCT) to balance exploration and exploitation. |
| How it Works | Runs thousands of random trials to generate a statistical distribution. | Iteratively updates a decision path by running random "rollouts" from specific nodes. |
| Primary Use Cases | Finance (portfolio risk), physics, engineering, project management. | Artificial Intelligence, turn-based games (Go, Chess, Big Two), robotics. |

| Item              | In Stock | Price |
| :---------------- | :------: | ----: |
| Python Hat        |   True   | 23.99 |
| SQL Hat           |   True   | 23.99 |
| Codecademy Tee    |  False   | 19.99 |
| Codecademy Hoodie |  False   | 42.99 |


## Takeaway
Monte Carlos Simulation need 

## Reference
[What is Monte Carlos Simulation](https://www.youtube.com/watch?v=7TqhmX92P6U)
[Monte Carlo Tree Search (MCTS)](https://www.youtube.com/watch?v=2Hv4b0vC7YY)
