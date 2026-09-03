from itertools import combinations
from game_rule import Player, Deck, symbol_to_int


def get_all_combos(hand):
    combos = []

    for c in hand:
        combos.append([c])

    for i in range(len(hand)):
        for j in range(i + 1, len(hand)):
            if symbol_to_int(hand[i][0]) == symbol_to_int(hand[j][0]):
                combos.append([hand[i], hand[j]])

    for i in range(len(hand)):
        for j in range(i + 1, len(hand)):
            for k in range(j + 1, len(hand)):
                vals = [symbol_to_int(hand[i][0]), symbol_to_int(hand[j][0]), symbol_to_int(hand[k][0])]
                if len(set(vals)) == 1:
                    combos.append([hand[i], hand[j], hand[k]])

    for i in range(len(hand)):
        for j in range(i + 1, len(hand)):
            for k in range(j + 1, len(hand)):
                for l in range(k + 1, len(hand)):
                    vals = [symbol_to_int(hand[i][0]), symbol_to_int(hand[j][0]),
                            symbol_to_int(hand[k][0]), symbol_to_int(hand[l][0])]
                    counts = {}
                    for v in vals:
                        counts[v] = counts.get(v, 0) + 1
                    if sorted(counts.values()) == [2, 2]:
                        combos.append([hand[i], hand[j], hand[k], hand[l]])

    if len(hand) >= 5:
        cp = Player("_temp")
        cp.receive_cards(list(hand))

        for s in cp.straight_combinations():
            combos.append(s)

        for f in cp.flush_combinations():
            combos.append(f)

        for fh in cp.full_house_combinations():
            combos.append(fh)

        for fk in cp.four_of_a_kind_combinations():
            combos.append(fk)

        for sf in cp.straight_flush_combinations():
            combos.append(sf)

    return combos


def remove_cards(hand, combo):
    remaining = list(hand)
    for card in combo:
        if card in remaining:
            remaining.remove(card)
    return remaining


def find_all_partitions(hand, max_partitions=5000):
    hand = sorted(hand, key=lambda c: (symbol_to_int(c[0]), {'d': 0, 'c': 1, 'h': 2, 's': 3}.get(c[1], 0)))
    results = []
    seen = set()
    _backtrack(hand, [], results, seen, max_partitions)
    return results


def _partition_key(partition):
    keys = []
    for combo in partition:
        sorted_combo = tuple(sorted(combo, key=lambda c: (symbol_to_int(c[0]), {'d': 0, 'c': 1, 'h': 2, 's': 3}.get(c[1], 0))))
        keys.append(sorted_combo)
    keys.sort(key=lambda k: (-len(k), k))
    return tuple(keys)


def _backtrack(remaining, current_partition, results, seen, max_partitions):
    if len(results) >= max_partitions:
        return

    if not remaining:
        key = _partition_key(current_partition)
        if key not in seen:
            seen.add(key)
            results.append(list(current_partition))
        return

    non_single_combos = [c for c in get_all_combos(remaining) if len(c) > 1]

    if not non_single_combos:
        singles_partition = current_partition + [[c] for c in remaining]
        key = _partition_key(singles_partition)
        if key not in seen:
            seen.add(key)
            results.append(singles_partition)
        return

    for combo in non_single_combos:
        new_remaining = remove_cards(remaining, combo)
        current_partition.append(combo)
        _backtrack(new_remaining, current_partition, results, seen, max_partitions)
        current_partition.pop()

        if len(results) >= max_partitions:
            return

    singles_partition = current_partition + [[c] for c in remaining]
    key = _partition_key(singles_partition)
    if key not in seen and len(results) < max_partitions:
        seen.add(key)
        results.append(singles_partition)


def partition_to_string(partition):
    parts = []
    singles = []
    
    for combo in partition:
        if len(combo) == 1:
            singles.append(combo[0])
        else:
            if singles:
                card_strs = [f"{c[0]}{c[1]}" for c in singles]
                parts.append(f"{len(singles)} singles ({', '.join(card_strs)})")
                singles = []
            card_strs = [f"{c[0]}{c[1]}" for c in combo]
            parts.append(f"[{', '.join(card_strs)}]")
    
    if singles:
        card_strs = [f"{c[0]}{c[1]}" for c in singles]
        parts.append(f"{len(singles)} singles ({', '.join(card_strs)})")
    
    return " + ".join(parts)


if __name__ == "__main__":
    deck = Deck()
    hand = deck.get_random_cards(13)
    print(f"Hand: {[f'{c[0]}{c[1]}' for c in hand]}")

    partitions = find_all_partitions(hand)
    print(f"\nFound {len(partitions)} complete partitions:\n")

    for i, p in enumerate(partitions[:20], 1):
        print(f"{i}. {partition_to_string(p)}")

    if len(partitions) > 20:
        print(f"\n... and {len(partitions) - 20} more")
