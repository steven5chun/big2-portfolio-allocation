import sys
import os
import random
import time
import matplotlib
import matplotlib.colors as mcolors

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from game_rule import Deck
from big2_game import Big2Game, Play, identify_play_type, PlayType
from big2_ai import SmartAI
from partition_finder import find_all_partitions, partition_to_string

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker


PLAYER_HAND = [('3', 'd'), ('3', 'h'), ('5', 'c'), ('5', 's'), ('8', 'd'), ('9', 'h'), ('10', 'c'), ('j', 'd'), ('q', 'h'), ('k', 's'), ('a', 'd'), ('2', 'c'), ('2', 's')]
OPP_CARDS = 8
TOTAL_SIMS = 150
TOP_N_LEGEND = 10
RESULTS_DIR = os.path.dirname(os.path.abspath(__file__))


def get_distinct_colors(n):
    base = ['#2196F3', '#4CAF50', '#FF9800', '#E91E63', '#9C27B0', '#00BCD4', '#FF5722', '#607D8B', '#795548', '#8BC34A',
            '#F44336', '#3F51B5', '#009688', '#CDDC39', '#FFC107', '#9E9E9E', '#673AB7', '#03A9F4', '#4CAF50', '#E040FB',
            '#FF6E40', '#18FFFF', '#EEFF41', '#651FFF', '#D500F9', '#00E676', '#FFEA00', '#FF1744', '#2979FF', '#1DE9B6',
            '#7C4DFF', '#F50057', '#00E5FF', '#76FF03', '#FFAB40', '#B388FF', '#82B1FF', '#CCFF90', '#EA80FC', '#FFE57F']
    if n <= len(base):
        return base[:n]
    extra = list(mcolors.TABLEAU_COLORS.values())
    return base + extra[:n - len(base)]


def card_str(c):
    return f'{c[0]}{c[1]}'


def hand_str(hand):
    return ', '.join(card_str(c) for c in hand)


def run_simulations(player_hand, partition, total_sims, opp_cards):
    ev_values = []
    total_ev = 0
    wins = 0
    total_cards_left = 0

    for sim in range(1, total_sims + 1):
        deck = Deck()
        all_cards = [c for c in deck.cards if c not in player_hand]
        random.shuffle(all_cards)

        opponent_hands = []
        idx = 0
        for _ in range(3):
            opponent_hands.append(all_cards[idx:idx + opp_cards])
            idx += opp_cards

        ai_partitions = []
        for oh in opponent_hands:
            opp_partitions = find_all_partitions(oh, max_partitions=50)
            ai_partitions.append(random.choice(opp_partitions))

        all_partitions = [partition] + ai_partitions

        game = Big2Game(
            [player_hand] + opponent_hands,
            partition_orders=all_partitions,
        )
        ai_players = [SmartAI() for _ in range(4)]

        winner, cards_left = game.simulate_with_partition(all_partitions, ai_players)

        if winner == 0:
            wins += 1
            pi = sum(cards_left[1:])
        else:
            pi = -2 * cards_left[0]

        total_ev += pi
        total_cards_left += cards_left[0]
        ev_values.append(total_ev / sim)

    final_wr = wins / total_sims
    final_acl = total_cards_left / total_sims
    final_ev = total_ev / total_sims

    return ev_values, final_wr, final_acl, final_ev


def plot_ev_convergence(all_results, total_sims, colors):
    fig, ax = plt.subplots(figsize=(16, 9))

    for rank, (partition, ev_values, final_wr, final_acl, final_ev) in enumerate(all_results):
        x = list(range(1, total_sims + 1))
        color = colors[rank % len(colors)]
        linewidth = 2.5 if rank < TOP_N_LEGEND else 1.0
        alpha = 0.9 if rank < TOP_N_LEGEND else 0.4

        if rank < TOP_N_LEGEND:
            label = f'#{rank+1} {partition_to_string(partition)}'
            if len(label) > 70:
                label = label[:67] + '...'
        else:
            label = None

        ax.plot(x, ev_values, linewidth=linewidth, color=color, label=label, alpha=alpha)

    ax.axhline(y=0, color='black', linestyle='--', alpha=0.5, linewidth=1.5, label='Break-even (EV = 0)')

    ax.set_xlabel('Number of Simulations', fontsize=13, fontweight='bold')
    ax.set_ylabel('Expected Value (Points per Hand)', fontsize=13, fontweight='bold')
    ax.set_title('Monte Carlos simulation of big 2 (13 card hand)', fontsize=15, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=9, loc='lower right', framealpha=0.9)
    ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))

    fig.tight_layout()
    output_path = os.path.join(RESULTS_DIR, 'ev_convergence_all.png')
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    return output_path


def main():
    print('=' * 70)
    print('Financial Analysis - All Partitions EV Convergence')
    print('=' * 70)
    print()
    print(f'Hand: [{hand_str(PLAYER_HAND)}]')
    print(f'Simulations per partition: {TOTAL_SIMS}')
    print()

    print('Enumerating all partitions...')
    partitions = find_all_partitions(PLAYER_HAND, max_partitions=5000)
    print(f'Found {len(partitions)} partitions')
    print()

    colors = get_distinct_colors(len(partitions))

    all_results = []
    overall_start = time.time()

    for i, partition in enumerate(partitions):
        sim_start = time.time()
        ev_values, final_wr, final_acl, final_ev = run_simulations(
            PLAYER_HAND, partition, TOTAL_SIMS, OPP_CARDS
        )
        sim_elapsed = time.time() - sim_start

        all_results.append((partition, ev_values, final_wr, final_acl, final_ev))

        eta = (sim_elapsed * (len(partitions) - i - 1)) if i + 1 > 0 else 0
        print(f'  [{i+1}/{len(partitions)}] {partition_to_string(partition)[:55]:55s} | Win: {final_wr:.1%} | EV: {final_ev:+.2f} | ETA: {eta:.0f}s')

    all_results.sort(key=lambda x: x[4], reverse=True)

    total_elapsed = time.time() - overall_start

    print()
    print('=' * 70)
    print('RANKED SUMMARY')
    print('=' * 70)
    print(f'{"Rank":>4} | {"Partition":55s} | {"Win Rate":>8} | {"Avg Left":>8} | {"EV":>8}')
    print('-' * 95)
    for rank, (partition, ev_values, final_wr, final_acl, final_ev) in enumerate(all_results, 1):
        label = partition_to_string(partition)
        if len(label) > 55:
            label = label[:52] + '...'
        print(f'{rank:>4} | {label:55s} | {final_wr:>7.1%} | {final_acl:>8.2f} | {final_ev:>+8.2f}')
    print()
    print(f'Total time: {total_elapsed:.1f}s')
    print()

    print('Generating EV convergence graph...')
    output_path = plot_ev_convergence(all_results, TOTAL_SIMS, colors)
    print(f'Saved: {output_path}')
    print()
    print('=' * 70)
    print('Done!')
    print('=' * 70)


if __name__ == '__main__':
    main()