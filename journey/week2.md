# Week 2
## Python Installation (mac os)
- Installation using Homebrew
Homebrew is an open-source software package management system that simplifies software installation on Apple's Mac OS and Linux. 

```shell
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

```
- After Homebrew has been installed, you can install Python by running the following command in your terminal:
```shell
brew install python
```

- Verifying the installation
You can verify that Python was correctly installed by running the following command in your terminal:

```shell
python3 --version
```

## Learn Python
- Learn Python [[1](https://www.w3schools.com/python/python_intro.asp)]
- Create virtual environment and Write Simple Python code
- Different Python structure: function, class, Loop etc..
- Object Oriented Programming (OOP) in Python. [[2](https://www.w3schools.com/python/python_oop.asp)]
- Python libaray: NumPy [[3](https://www.w3schools.com/python/numpy/numpy_intro.asp)], Pandas [[4](https://www.w3schools.com/python/pandas/default.asp)] and matpoltlib [[5](https://www.w3schools.com/python/matplotlib_getting_started.asp)]
- Based on what we learn on pyhton, Study Big2 Monte Carlos Python code to find out possibility of different combination of big 2 cards [[6](https://github.com/BobSwagg13/Application-of-Combinatorics-in-Big-Two/tree/main/src)]

## big 2 card representation by python code

Cards are represented as tuples (value, suit):

Values (ordered by rank in Big 2):
|Symbol|Integer| Rank |
| :----| :-----| :----|
|'3'   |3	   |Lowest|
|'4'-'9'|4-9   |      |	 
|'10'	|10	   |      |
|'j'	|11	   |      |
|'q'	|12	   |      |
|'k'	|13	   |      |
|'a'	|14	   |      |
|'2'	|15	   | Highest|

Suits:
|Symbol |	Meaning |
| :-----| :---------|
|'d'	|Diamonds   |
|'c'	|Clubs      |
|'h'	|Hearts     |
|'s'	|Spades     |

Example 
card: ('3', 'd') = 3 of Diamonds, ('a', 's') = Ace of Spades, ('2', 'h') = 2 of Hearts.

A full deck is 52 cards: 13 values × 4 suits, stored as a list of tuples.

## big 2 card hand probabilities by python code
This is a Monte Carlo simulation for estimating poker hand probabilities in a 13-card hand (used in Big 2).
It runs 1,000,000 iterations, dealing random 13-card hands and checking for the presence of
- Pair — Two cards of the same rank (e.g., 7♥ 7♠)
- Three of a kind — Three cards of the same rank (e.g., K♥ K♠ K♦)
- Straight — Five consecutive cards of mixed suits (e.g., 5♠ 6♥ 7♦ 8♣ 9♥)
- Flush — Five cards of the same suit, not in sequence (e.g., 2♥ 5♥ 9♥ J♥ K♥)
- Full house — A three of a kind plus a pair (e.g., 8♣ 8♦ 8♠ Q♥ Q♠)
- Four of a kind — Four cards of the same rank (e.g., A♥ A♠ A♦ A♣)
- Straight flush — Five consecutive cards all of the same suit (e.g., 4♣ 5♣ 6♣ 7♣ 8♣) — the rarest hand

## Takeaway 

This week covered Python installation, basic numerical calculations, and data visualization. Furthermore, I implemented a Monte Carlo method to experimentally determine the mathematical probability of drawing specific Big 2 card combinations, such as pairs, three of a kind, straight etc.. By mapping custom game rules into Python code, I successfully modeled individual cards and hand structures. Acquiring these fundamental data science skills provides a strong foundation for developing a comprehensive Big 2 analytics portfolio project in the future.

## Reference
- [1] [Introduction of Python](https://www.w3schools.com/python/python_intro.asp)
- [2] [Python OOP](https://www.w3schools.com/python/python_oop.asp)
- [3] [NumPy](https://www.w3schools.com/python/numpy/numpy_intro.asp)
- [4] [Pandas](https://www.w3schools.com/python/pandas/default.asp)
- [5] [Matplotlib](https://www.w3schools.com/python/matplotlib_getting_started.asp)
- [6] [Big 2 Monte Carlos Python code](https://github.com/BobSwagg13/Application-of-Combinatorics-in-Big-Two/tree/main/src)