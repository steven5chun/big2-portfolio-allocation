import sys
import os
import random
import time
import numpy as np
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
TOP_N = 10
RESULTS_DIR = os.path.dirname(os.path.abspath(__file__))


def card_str(c):
    return f'{c[0]}{c[1]}'


def hand_str(hand):
    return ', '.join(card_str(c) for c in hand)


def run_risk_simulation(player_hand, partition, total_sims, opp_cards):
    pi_values = []
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

        pi_values.append(pi)
        total_cards_left += cards_left[0]

    final_wr = wins / total_sims
    final_acl = total_cards_left / total_sims

    return pi_values, final_wr, final_acl


def calculate_risk_metrics(pi_values):
    arr = np.array(pi_values)
    mean_ev = np.mean(arr)
    variance = np.var(arr)
    std_dev = np.std(arr)
    var_95 = np.percentile(arr, 5)
    sharpe = mean_ev / std_dev if std_dev > 0 else 0.0

    return {
        'ev': mean_ev,
        'variance': variance,
        'std_dev': std_dev,
        'var_95': var_95,
        'sharpe': sharpe,
    }


def plot_risk_return_scatter(all_risk_results):
    fig, ax = plt.subplots(figsize=(14, 9))

    std_devs = [r['metrics']['std_dev'] for r in all_risk_results]
    evs = [r['metrics']['ev'] for r in all_risk_results]
    sharpes = [r['metrics']['sharpe'] for r in all_risk_results]

    median_std = np.median(std_devs)

    ax.axvline(x=median_std, color='gray', linestyle=':', alpha=0.4)
    ax.axhline(y=0, color='black', linestyle='--', alpha=0.5, linewidth=1.2, label='Break-even (EV = 0)')

    for i, r in enumerate(all_risk_results):
        color = '#4CAF50' if r['metrics']['sharpe'] > 0 else '#E91E63'
        size = max(30, min(400, abs(r['metrics']['sharpe']) * 80))
        alpha = 0.9 if i < TOP_N else 0.4
        zorder = 3 if i < TOP_N else 1

        if i < TOP_N:
            label = f'#{i+1} {partition_to_string(r["partition"])}'
            if len(label) > 60:
                label = label[:57] + '...'
        else:
            label = None

        ax.scatter(r['metrics']['std_dev'], r['metrics']['ev'],
                   s=size, c=color, alpha=alpha, edgecolors='none',
                   label=label, zorder=zorder)

    ax.set_xlabel('Standard Deviation (Risk)', fontsize=13, fontweight='bold')
    ax.set_ylabel('Expected Value (Return)', fontsize=13, fontweight='bold')
    ax.set_title('Risk-Return Scatter Plot — Sharpe Ratio (Bubble Size)', fontsize=15, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8, loc='best', framealpha=0.9, scatterpoints=1)
    ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))

    fig.tight_layout()
    output_path = os.path.join(RESULTS_DIR, 'risk_return_scatter.png')
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    return output_path


def plot_return_histogram(top_risk_result, total_sims):
    fig, ax = plt.subplots(figsize=(12, 7))

    pi_values = top_risk_result['pi_values']
    ax.hist(pi_values, bins=30, color='#2196F3', edgecolor='white', alpha=0.8)

    var_95 = top_risk_result['metrics']['var_95']
    mean_ev = top_risk_result['metrics']['ev']

    ax.axvline(x=mean_ev, color='green', linestyle='--', linewidth=2, label=f'Mean EV = {mean_ev:+.2f}')
    ax.axvline(x=var_95, color='red', linestyle='--', linewidth=2, label=f'VaR(95%) = {var_95:.2f}')
    ax.axvline(x=0, color='black', linestyle='-', alpha=0.5, linewidth=1.5, label='Break-even')

    label = partition_to_string(top_risk_result['partition'])
    if len(label) > 50:
        label = label[:47] + '...'
    ax.set_xlabel('Points per Game (Pi)', fontsize=13, fontweight='bold')
    ax.set_ylabel('Frequency', fontsize=13, fontweight='bold')
    ax.set_title(f'Return Distribution — {label}\nTop Sharpe Partition ({total_sims} simulations)', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    ax.legend(fontsize=11, loc='upper right')

    fig.tight_layout()
    output_path = os.path.join(RESULTS_DIR, 'risk_histogram.png')
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    return output_path


def plot_sharpe_bar_chart(all_risk_results):
    fig, ax = plt.subplots(figsize=(14, 8))

    labels = []
    sharpes = []
    for i, r in enumerate(all_risk_results):
        if len(labels) >= 20:
            break
        label = f'#{i+1} {partition_to_string(r["partition"])}'
        if len(label) > 55:
            label = label[:52] + '...'
        labels.append(label)
        sharpes.append(r['metrics']['sharpe'])

    colors = ['#4CAF50' if s > 0 else '#E91E63' for s in sharpes]
    x = list(range(len(labels)))

    ax.bar(x, sharpes, color=colors, edgecolor='white', alpha=0.85)

    for i, (xi, s) in enumerate(zip(x, sharpes)):
        offset = 0.15 if s > 0 else -0.15
        ax.text(xi, s + offset, f'{s:.2f}', ha='center', fontsize=9,
                fontweight='bold', color='green' if s > 0 else 'red',
                va='bottom' if s > 0 else 'top')

    ax.axhline(y=0, color='black', linestyle='-', alpha=0.5, linewidth=1.5)
    ax.axhline(y=0.5, color='gray', linestyle=':', alpha=0.4, label='Sharpe = 0.5 (Good)')
    ax.axhline(y=1.0, color='orange', linestyle=':', alpha=0.4, label='Sharpe = 1.0 (Excellent)')

    ax.set_ylabel('Sharpe Ratio', fontsize=13, fontweight='bold')
    ax.set_title('Sharpe Ratio Ranking — Top 20 Partitions', fontsize=15, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    ax.legend(fontsize=10, loc='upper right')
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=70, ha='right', fontsize=8)

    fig.tight_layout()
    output_path = os.path.join(RESULTS_DIR, 'sharpe_bar_chart.png')
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    return output_path


def main():
    print('=' * 70)
    print('Financial Analysis - Risk Metrics (Variance, VaR, Sharpe)')
    print('=' * 70)
    print()
    print(f'Hand: [{hand_str(PLAYER_HAND)}]')
    print(f'Simulations per partition: {TOTAL_SIMS}')
    print()

    print('Enumerating all partitions...')
    partitions = find_all_partitions(PLAYER_HAND, max_partitions=5000)
    print(f'Found {len(partitions)} partitions')
    print()

    all_risk_results = []
    overall_start = time.time()

    for i, partition in enumerate(partitions):
        sim_start = time.time()
        pi_values, final_wr, final_acl = run_risk_simulation(
            PLAYER_HAND, partition, TOTAL_SIMS, OPP_CARDS
        )
        metrics = calculate_risk_metrics(pi_values)
        sim_elapsed = time.time() - sim_start

        all_risk_results.append({
            'partition': partition,
            'pi_values': pi_values,
            'win_rate': final_wr,
            'avg_cards_left': final_acl,
            'metrics': metrics,
        })

        eta = (sim_elapsed * (len(partitions) - i - 1)) if i + 1 > 0 else 0
        print(f'  [{i+1}/{len(partitions)}] {partition_to_string(partition)[:55]:55s} | EV: {metrics["ev"]:+.2f} | StdDev: {metrics["std_dev"]:.2f} | VaR: {metrics["var_95"]:.2f} | Sharpe: {metrics["sharpe"]:+.2f} | ETA: {eta:.0f}s')

    all_risk_results.sort(key=lambda x: x['metrics']['sharpe'], reverse=True)

    total_elapsed = time.time() - overall_start

    print()
    print('=' * 70)
    print('RISK METRICS SUMMARY (Sorted by Sharpe Ratio)')
    print('=' * 70)
    header = f'{"Rank":>4} | {"Partition":55s} | {"EV":>7} | {"Std Dev":>8} | {"VaR(95%)":>8} | {"Sharpe":>7}'
    print(header)
    print('-' * 100)
    for rank, r in enumerate(all_risk_results, 1):
        label = partition_to_string(r['partition'])
        if len(label) > 55:
            label = label[:52] + '...'
        m = r['metrics']
        print(f'{rank:>4} | {label:55s} | {m["ev"]:>+7.2f} | {m["std_dev"]:>8.2f} | {m["var_95"]:>8.2f} | {m["sharpe"]:>+7.2f}')
    print()
    print(f'Total time: {total_elapsed:.1f}s')
    print()

    print('Generating risk analysis graphs...')
    p1 = plot_risk_return_scatter(all_risk_results)
    print(f'  Saved: {p1}')

    top = all_risk_results[0]
    p2 = plot_return_histogram(top, TOTAL_SIMS)
    print(f'  Saved: {p2}')

    p3 = plot_sharpe_bar_chart(all_risk_results)
    print(f'  Saved: {p3}')

    print()
    print('=' * 70)
    print('Done!')
    print('=' * 70)


if __name__ == '__main__':
    main()