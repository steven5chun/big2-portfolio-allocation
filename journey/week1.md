# Week 1
## Summmary
- Introduction to Big 2: Understanding the core rules, card rankings, and gameplay of Big 2.
- Probability Calculations: Using mathematical formulas to calculate the probability of specific card distributions and identifying impossible combinations.
- The Monte Carlo Method: Exploring how the Monte Carlo simulation method can be applied to model game outcomes and determine strategy.

## What is Monte Carlos Simulation
Monte Carlo Simulation is a mathematical technique used to estimate the possible outcomes of an uncertain event by modeling the probability of different outcomes using random sampling. It acts like a way to look into the future to make better business, investment, and planning decisions.

A Monte Carlo simulation will work under virtually any probability distribution, as long as the distribution satisfies one fundamental mathematical condition: it must have a finite expected value (mean)

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
| :------ | :--------------------------- | :----------------------------- |
| Primary Goal | Forecast overall risk, outcomes, or values. | Find the single best next move or decision. |
| Structure | Flat / ***No Structure***. Evaluates completely independent random samples. | ***Tree Structure.*** Dynamically builds a memory tree of moves and game states. |
| Decision Logic | Passive sampling. Samples randomly from fixed probability distributions. | Active learning. Uses formulas (like UCT) to balance exploration and exploitation. |
| How it Works | Runs thousands of random trials to generate a statistical distribution. | Iteratively updates a decision path by running random "rollouts" from specific nodes. |
| Primary Use Cases | Finance (portfolio risk), physics, engineering, project management. | Artificial Intelligence, turn-based games (Go, Chess, Big Two), robotics. |

The reason Monte Carlo Simulation (MCS) is superior to Monte Carlo Tree Search (MCTS) for Big 2 card combination arrangement is because hand organization is fundamentally a portfolio combination problem. It is a one-time macro allocation and forecasting problem. At the moment of arranging your initial 13 cards, you are not engaging in a turn-based, competitive game with a sequential chain of reactive player choices; you are simply optimizing your resources before the match begins.[3]


## Takeaway

A perfect cultural analogy for this methodology can be found in the Marvel film Avengers: Infinity War. To find a way to defeat Thanos, Doctor Strange runs 14,000,605 simulations of parallel futures in real-time, discovering exactly one winning path.

This sequence is a cinematic representation of a ***Monte Carlo Simulation***.

When faced with complex, real-world problems like Big 2 strategy or financial portfolio management, traditional, static mathematical formulas break down completely. The system simply contains too many combinations, exponential possibilities, and imperfect information (unseen cards or hidden market forces).

Instead of trying to solve the problem with an impossible, single calculation, the Monte Carlo method embraces the chaos. By rapidly simulating thousands of randomized, parallel scenarios, it uncovers the underlying probability distribution of the entire system. Learning this method taught me that when a system is too volatile to predict, running extensive parallel simulations is the single most powerful tool we have to navigate uncertainty and find our "one winning path."

## Reference
- [What is Monte Carlos Simulation](https://www.youtube.com/watch?v=7TqhmX92P6U)
- [Monte Carlo Tree Search (MCTS)](https://www.youtube.com/watch?v=2Hv4b0vC7YY)
- [3][Monte Carlos Statstics skills](https://www.youtube.com/watch?v=r7cn3WS5x9c)
