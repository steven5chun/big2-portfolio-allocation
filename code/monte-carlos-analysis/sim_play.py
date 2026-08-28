import sys
import os
import random
import time
import csv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from game_rule import Deck
from big2_game import Big2Game, Play, identify_play_type
from big2_ai import SmartAI
from partition_finder import find_all_partitions, partition_to_string

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker


# ======================== CONFIG ========================
PLAYER_HAND = [('3', 'd'), ('5', 'h'), ('5', 'c'), ('7', 's'), ('k', 's'), ('8', 'd'), ('8', 'c'), ('8', 'h')]
OPP_CARDS = 8
ITERATIONS = [100, 500, 1000, 1500, 2000, 2500, 3000]
TOP_N = 5
MAX_PARTITIONS = 500
RESULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
# ========================================================


def card_str(c):
    return f"{c[0]}{c[1]}"


def hand_str(hand):
    return ", ".join(card_str(c) for c in hand)


def partition_label(partition):
    s = partition_to_string(partition)
    if len(s) > 60:
        return s[:57] + "..."
    return s


def run_sims_cumulative(player_hand, partition, total_sims, opp_cards):
    wins = 0
    total_cards_left = 0
    milestones = {}
    current_milestone_idx = 0
    player_card_count = len(player_hand)

    for sim in range(1, total_sims + 1):
        deck = Deck()
        all_cards = deck.cards.copy()
        random.shuffle(all_cards)

        opponent_hands = []
        idx = player_card_count
        for _ in range(3):
            opponent_hands.append(all_cards[idx:idx + opp_cards])
            idx += opp_cards

        game = Big2Game(
            [player_hand] + opponent_hands,
            partition_orders=[partition, None, None, None],
        )
        ai_players = [SmartAI() for _ in range(3)]

        winner, cards_left = game.simulate_with_partition(partition, ai_players)

        if winner == 0:
            wins += 1
        total_cards_left += cards_left[0]

        while current_milestone_idx < len(ITERATIONS) and sim == ITERATIONS[current_milestone_idx]:
            milestones[sim] = (wins / sim, total_cards_left / sim)
            current_milestone_idx += 1

    milestones[total_sims] = (wins / total_sims, total_cards_left / total_sims)
    return milestones


def plot_convergence_winrate(top_results, max_iters):
    fig, ax = plt.subplots(figsize=(10, 6))
    for rank, (partition, final_wr, final_acl, ms) in enumerate(top_results):
        x = sorted(ms.keys())
        y = [ms[i][0] * 100 for i in x]
        label = f"#{rank+1} {partition_to_string(partition)}"
        if len(label) > 50:
            label = label[:47] + "..."
        ax.plot(x, y, marker="o", markersize=4, linewidth=1.5, label=label, color=COLORS[rank % len(COLORS)])

    ax.set_xlabel("Iterations")
    ax.set_ylabel("Win Rate (%)")
    ax.set_title("Win Rate Convergence (Top 5 Partitions)")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=7, loc="lower right")
    ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
    fig.tight_layout()
    fig.savefig(os.path.join(RESULTS_DIR, "convergence_winrate.png"), dpi=150)
    plt.close(fig)


def plot_convergence_cards(top_results, max_iters):
    fig, ax = plt.subplots(figsize=(10, 6))
    for rank, (partition, final_wr, final_acl, ms) in enumerate(top_results):
        x = sorted(ms.keys())
        y = [ms[i][1] for i in x]
        label = f"#{rank+1} {partition_to_string(partition)}"
        if len(label) > 50:
            label = label[:47] + "..."
        ax.plot(x, y, marker="o", markersize=4, linewidth=1.5, label=label, color=COLORS[rank % len(COLORS)])

    ax.set_xlabel("Iterations")
    ax.set_ylabel("Avg Cards Left")
    ax.set_title("Avg Cards Left Convergence (Top 5 Partitions)")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=7, loc="lower right")
    ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
    fig.tight_layout()
    fig.savefig(os.path.join(RESULTS_DIR, "convergence_cards_left.png"), dpi=150)
    plt.close(fig)


COLORS = ["#2196F3", "#4CAF50", "#FF9800", "#E91E63", "#9C27B0"]


def plot_final_ranking(top_results):
    fig, ax = plt.subplots(figsize=(10, 6))
    for rank, (partition, final_wr, final_acl, ms) in enumerate(top_results):
        label = f"#{rank+1} {partition_to_string(partition)}"
        if len(label) > 60:
            label = label[:57] + "..."
        ax.bar(rank, final_wr * 100, color=COLORS[rank % len(COLORS)], label=label)
        ax.text(rank, final_wr * 100 + 0.3, f"{final_wr*100:.1f}%", ha="center", fontsize=9, fontweight="bold")

    ax.set_ylabel("Win Rate (%)")
    ax.set_title(f"Final Ranking ({max(ITERATIONS)} iterations)")
    ax.grid(True, axis="y", alpha=0.3)
    ax.legend(fontsize=7, loc="upper right")
    ax.set_xticks([])
    fig.tight_layout()
    fig.savefig(os.path.join(RESULTS_DIR, "final_ranking.png"), dpi=150)
    plt.close(fig)


def save_csv(top_results):
    filepath = os.path.join(RESULTS_DIR, "convergence_results.csv")
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Rank", "Partition", "Iterations", "Win Rate", "Avg Cards Left"])
        for rank, (partition, final_wr, final_acl, ms) in enumerate(top_results):
            for iters in sorted(ms.keys()):
                wr, acl = ms[iters]
                writer.writerow([rank + 1, partition_to_string(partition), iters, f"{wr:.4f}", f"{acl:.4f}"])


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)

    print("=" * 70)
    print("Big 2 Convergence Analysis")
    print("=" * 70)
    print()
    print(f"Hand: [{hand_str(PLAYER_HAND)}]")
    print(f"Opponent hand size: {OPP_CARDS} cards each")
    print(f"Max iterations: {max(ITERATIONS)}")
    print()

    print("Finding partitions...")
    partitions = find_all_partitions(PLAYER_HAND, max_partitions=MAX_PARTITIONS)
    print(f"Found {len(partitions)} partitions")
    print()

    print(f"Running {max(ITERATIONS)} simulations per partition...")
    start = time.time()

    all_results = []

    for i, partition in enumerate(partitions):
        ms = run_sims_cumulative(PLAYER_HAND, partition, max(ITERATIONS), OPP_CARDS)
        final_wr, final_acl = ms[max(ITERATIONS)]
        all_results.append((partition, final_wr, final_acl, ms))

        elapsed = time.time() - start
        eta = (elapsed / (i + 1)) * (len(partitions) - i - 1) if i + 1 > 0 else 0
        best_wr = max(r[1] for r in all_results)
        print(f"  [{i+1}/{len(partitions)}] {partition_to_string(partition)[:50]:50s} | Win: {final_wr:.1%} | ETA: {eta:.0f}s")

    all_results.sort(key=lambda x: x[1], reverse=True)
    top_results = all_results[:TOP_N]

    print()
    print("=" * 70)
    print(f"TOP {TOP_N} PARTITIONS - METRICS BY ITERATION")
    print("=" * 70)

    for rank, (partition, final_wr, final_acl, ms) in enumerate(top_results, 1):
        print(f"\n#{rank} {partition_to_string(partition)}")
        print(f"  {'Iters':>7}   {'Win Rate':>10}   {'Avg Left':>10}")
        for iters in ITERATIONS:
            wr, acl = ms.get(iters, ms[max(ITERATIONS)])
            print(f"  {iters:>7}   {wr:>9.1%}   {acl:>10.2f}")

    total_time = time.time() - start
    print(f"\nTotal time: {total_time:.1f}s")
    print()

    print("Generating graphs...")
    plot_convergence_winrate(top_results, max(ITERATIONS))
    plot_convergence_cards(top_results, max(ITERATIONS))
    plot_final_ranking(top_results)
    save_csv(top_results)

    for fname in ["convergence_winrate.png", "convergence_cards_left.png", "final_ranking.png", "convergence_results.csv"]:
        print(f"  Saved: {os.path.join(RESULTS_DIR, fname)}")

    print()
    print("=" * 70)
    print("Done!")
    print("=" * 70)


if __name__ == "__main__":
    main()
