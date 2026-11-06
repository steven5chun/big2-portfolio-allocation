import time
import random
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from game_rule import Deck
from big2_game import Big2Game
from big2_ai import SmartAI
from partition_finder import find_all_partitions, partition_to_string


PLAYER_HAND = [('3', 'd'), ('3', 'h'), ('5', 'c'), ('5', 's'), ('8', 'd'), ('9', 'h'), 
               ('10', 'c'), ('j', 'd'), ('q', 'h'), ('k', 's'), ('a', 'd'), ('2', 'c'), ('2', 's')]

REPRESENTATIVE_PARTITION = [
    [('8', 'd'), ('9', 'h'), ('10', 'c'), ('j', 'd'), ('q', 'h')],
    [('3', 'd')], [('3', 'h')], [('5', 'c')], [('5', 's')],
    [('k', 's')], [('a', 'd')], [('2', 'c')], [('2', 's')]
]

OPPONENT_CARD_COUNTS = [8, 13]
GAMES_PER_SCENARIO = 300


def run_benchmark(opp_cards, num_games, partition):
    random.seed(42)
    
    enum_times = []
    start_total = time.time()
    
    for game_num in range(num_games):
        deck = Deck()
        all_cards = [c for c in deck.cards if c not in PLAYER_HAND]
        random.shuffle(all_cards)
        
        opponent_hands = []
        idx = 0
        for _ in range(3):
            opponent_hands.append(all_cards[idx:idx + opp_cards])
            idx += opp_cards
        
        start_enum = time.time()
        ai_partitions = []
        for oh in opponent_hands:
            opp_partitions = find_all_partitions(oh, max_partitions=50)
            ai_partitions.append(random.choice(opp_partitions))
        enum_time = time.time() - start_enum
        enum_times.append(enum_time)
        
        all_partitions = [partition] + ai_partitions
        
        game = Big2Game(
            [PLAYER_HAND] + opponent_hands,
            partition_orders=all_partitions,
        )
        ai_players = [SmartAI() for _ in range(4)]
        
        winner, cards_left = game.simulate_with_partition(all_partitions, ai_players)
    
    total_time = time.time() - start_total
    avg_per_game = total_time / num_games
    avg_enum_time = sum(enum_times) / len(enum_times)
    
    return {
        'enum_time': avg_enum_time,
        'total_time': total_time,
        'avg_per_game': avg_per_game
    }


def main():
    print('=' * 70)
    print('BENCHMARK: 8 cards vs 13 cards per opponent')
    print(f'Partition: {partition_to_string(REPRESENTATIVE_PARTITION)}')
    print(f'Games per scenario: {GAMES_PER_SCENARIO}')
    print('=' * 70)
    
    results = {}
    
    for opp_cards in OPPONENT_CARD_COUNTS:
        print(f'\nBenchmarking {opp_cards} cards per opponent...')
        results[opp_cards] = run_benchmark(opp_cards, GAMES_PER_SCENARIO, REPRESENTATIVE_PARTITION)
        
        print(f'  - Partition enumeration: {results[opp_cards]["enum_time"]:.3f}s')
        print(f'  - Total time ({GAMES_PER_SCENARIO} games): {results[opp_cards]["total_time"]:.1f}s')
        print(f'  - Average per game: {results[opp_cards]["avg_per_game"]:.3f}s')
    
    speedup = results[13]['total_time'] / results[8]['total_time']
    
    print()
    print('=' * 70)
    print(f'SPEEDUP FACTOR: {speedup:.1f}x slower with 13 cards')
    print('=' * 70)
    
    print('\nRecommendation:')
    if speedup > 15:
        print(f'  - 13 cards is {speedup:.1f}x slower. Consider sticking with 8 cards.')
        print(f'  - If you must use 13 cards, reduce games from 300 to {int(300/speedup)} for similar runtime.')
    elif speedup > 10:
        print(f'  - 13 cards is {speedup:.1f}x slower. Consider reducing games from 300 to {int(300/speedup)}.')
    else:
        print(f'  - 13 cards is only {speedup:.1f}x slower. Feasible to use with current settings.')


if __name__ == '__main__':
    main()
