## Project Title

The Big 2 Portfolio Allocation: A Journey to Learn Portfolio Management by Monte Carlo Simulation through Big 2

## Project Goal

Driven by a desire to master foundational quantitative finance concepts, I built a Python-based Monte Carlo Simulation (MCS) framework. By treating the traditional card game Big 2 (鋤大D) as an asset allocation problem, this project explores how optimizing a 13-card hand directly mirrors managing financial risk in highly volatile markets.

## The Learning Journey & System Realizations

1. ***Breaking the Code Barrier via "Vibe Coding":***

   I started this project with zero programming experience. By leveraging GitHub open-source repositories for basic game rules and relying on AI-assisted "Vibe Coding," I stitched together a high-performance simulation script. The journey was to learn core software architecture, data structures, and debugging through direct, iterative execution.

2. ***The Core Realization: Hand Arrangements = Asset Allocation***

   This project was realizing that arranging a 13-card hand is functionally identical to constructing a stock portfolio.

   - The Strategic Dilemma: Should I split my cards into a high-risk 5-card Straight and weak singles, or partition them into stable pairs and high-ranking control cards?
   - The Financial Equivalent: This maps perfectly to the Efficient Frontier in Modern Portfolio Theory (MPT). I learned how to balance aggressive, high-yield combinations against low-volatility preservation assets (like Aces and Twos) to maximize my structural "Sharpe Ratio" before the game even begins.
   

## Core Takeaway

This project did not yield a perfect, unbeatable card algorithm—because in systems dominated by human behavior, a perfect formula does not exist.
The true value is the mastery of the methodology. I transitioned from a non-programmer to an analytical systems-thinker, proving that complex financial engineering concepts can be mastered by analyzing the rule-bound systems we interact with every day.

I quickly discovered that static formulas are not enough. Big 2, like Wall Street, is a highly volatile, dynamic system where an individual's success depends heavily on the unpredictable, non-linear actions of other players. 

## Background

Big 2 (鋤大D) is a popular Asian card game for four players. The goal is to play all your cards first. Players use single cards, pairs, or five-card hands like poker. The player with the 3 of diamonds goes first. The 2 is the highest card, and diamonds are the lowest suit.where the number 2 holds the highest value. 

I have always been curious about how to consistently win at Big 2 and whether there is a strategic approach to improving the win rate. 

This project aims to discover the optimal strategy for various in-game situations while documenting my personal learning journey.

## Learning Journey

[Week 1](./journey/week1.md)

- **Game Rules & Constraint Logic:** Mastered the core rule matrices, hierarchy rankings, and discrete system mechanics governing Big 2 gameplay.
- **Combinatorial Probability Modeling:** Deployed mathematical formulas to calculate specific card distribution parameters and algorithmically identify impossible subsets or hand boundaries.
- **Stochastic Methodology Foundations:** Explored the structural principles of the Monte Carlo simulation framework to model game trees under uncertainty and optimize decision-making strategies.


[Week 2](./journey/week2.md)
- **Python Fundamentals:** Mastered syntax foundations, object-oriented programming concepts, and algorithmic control flows.
- **Script Prototyping:** Engineered baseline scripts to execute simple deterministic calculations and data structures.
- **Stochastic Analysis:** Explored Monte Carlo Python logic to model the empirical probabilities and distribution characteristics of complex Big 2 card combinations.

[Week 3](./journey/week3.md)
- **Generative AI Development:** Researched the paradigms of "vibe coding" and advanced prompt-driven software orchestration.
- **IDE & Tools Infrastructure:** Configured integrated development environments (IDEs), localized AI-assisted coding extensions, and version control tools.
- **Rapid Prototyping Execution:** Leveraged generative AI tooling to rapidly build and debug simple, reactive game-engine models.


[Week 4-5](./journey/week4-5.md)
- **Combinatorial Card Partitioning:** Algorithmic generation of all valid card combinations and potential hand partitions from a fixed starting hand.
- **Stochastic Game Engine Architecture:** Design and implementation of a discrete state-machine engine governing Big 2 rules, structural logic, and transition states.
- **Expected Value (EV) Modeling:** Formal mathematical modeling of the game’s utility function to calculate probability-weighted point returns rather than binary win rates.
- **Monte Carlo Simulation Optimization:** Development of an iterative stochastic loop framework to isolate the mathematically optimal card configuration across thousands of independent trials.
- **Quantitative Results Analysis:** Statistical evaluation of the simulation data to map out the Efficient Frontier and evaluate strategy performance under uncertainty.


[Week 6](./journey/week6.md)

- **Modern Portfolio Theory (MPT) Core:** Researched the foundations of quantitative portfolio optimization, asset weighting frameworks, and the mathematics of the Efficient Frontier.
- **Quantitative Metrics Exploration:** Analyzed key financial risk parameters, including systemic Variance, standard Volatility measures, Downside Risk boundaries, and the Sharpe Ratio framework.
- **Asset-to-Card Allocation Mapping:** Formulated a structural cross-disciplinary mapping system to translate financial metrics directly into Big 2 card distribution parameters.
- **Financial Benchmark Prototyping:** Engineered a baseline stock allocation model using Monte Carlo simulations to calculate risk-adjusted equity weights.


## References

- [Big 2 Wiki](https://en.wikipedia.org/wiki/Big_two)
- [Big 2 mathematical formula calculation](https://github.com/BobSwagg13/Application-of-Combinatorics-in-Big-Two/blob/main/docs/Application%20of%20Combinatorics%20in%20Big%20Two.pdf)
