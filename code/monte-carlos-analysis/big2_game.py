import random
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Tuple, Optional
from game_rule import Deck, Player, symbol_to_int


SUIT_RANK = {'d': 0, 'c': 1, 'h': 2, 's': 3}
VALUE_ORDER = ['3', '4', '5', '6', '7', '8', '9', '10', 'j', 'q', 'k', 'a', '2']


class PlayType(Enum):
    SINGLE = 1
    PAIR = 2
    TRIPLE = 3
    TWO_PAIR = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_OF_A_KIND = 8
    STRAIGHT_FLUSH = 9


@dataclass
class Play:
    cards: List[Tuple[str, str]]
    play_type: PlayType
    rank_value: int = 0
    max_suit: int = 0

    def __post_init__(self):
        if self.rank_value == 0 and self.cards:
            self.rank_value = max(symbol_to_int(c[0]) for c in self.cards)
            self.max_suit = max(SUIT_RANK.get(c[1], 0) for c in self.cards)

        if self.play_type in (PlayType.STRAIGHT, PlayType.STRAIGHT_FLUSH):
            vals = set(symbol_to_int(c[0]) for c in self.cards)
            if vals == {3, 4, 5, 14, 15}:
                self.rank_value = 5
            elif vals == {3, 4, 5, 6, 15}:
                self.rank_value = 6

    def __eq__(self, other):
        if not isinstance(other, Play):
            return False
        return self.play_type == other.play_type and sorted(self.cards) == sorted(other.cards)

    def __hash__(self):
        return hash((self.play_type, tuple(sorted(self.cards))))

    def card_count(self):
        return len(self.cards)

    def __str__(self):
        return f"{self.play_type.name}({', '.join(str(c) for c in self.cards)})"


def identify_play_type(cards):
    if len(cards) == 1:
        return PlayType.SINGLE

    if len(cards) == 2:
        if symbol_to_int(cards[0][0]) == symbol_to_int(cards[1][0]):
            return PlayType.PAIR

    if len(cards) == 3:
        vals = [symbol_to_int(c[0]) for c in cards]
        if len(set(vals)) == 1:
            return PlayType.TRIPLE

    if len(cards) == 4:
        vals = [symbol_to_int(c[0]) for c in cards]
        counts = {}
        for v in vals:
            counts[v] = counts.get(v, 0) + 1
        if sorted(counts.values()) == [2, 2]:
            return PlayType.TWO_PAIR

    if len(cards) == 5:
        return identify_5_card_type(cards)

    return None


def identify_5_card_type(cards):
    vals = [symbol_to_int(c[0]) for c in cards]
    suits = [c[1] for c in cards]
    is_flush = len(set(suits)) == 1

    sorted_vals = sorted(vals)
    is_straight = True
    for i in range(4):
        if sorted_vals[i + 1] != sorted_vals[i] + 1:
            is_straight = False
            break

    if not is_straight:
        if set(vals) == {3, 4, 5, 14, 15}:
            is_straight = True
        elif set(vals) == {3, 4, 5, 6, 15}:
            is_straight = True

    counts = {}
    for v in vals:
        counts[v] = counts.get(v, 0) + 1
    count_vals = sorted(counts.values())

    if is_straight and is_flush:
        return PlayType.STRAIGHT_FLUSH
    if is_four_of_a_kind(counts):
        return PlayType.FOUR_OF_A_KIND
    if count_vals == [2, 3]:
        return PlayType.FULL_HOUSE
    if is_flush:
        return PlayType.FLUSH
    if is_straight:
        return PlayType.STRAIGHT

    return None


def is_four_of_a_kind(counts):
    return 4 in counts.values()


def can_beat(new_play, current_play):
    if new_play.play_type != current_play.play_type:
        return False
    if new_play.card_count() != current_play.card_count():
        return False

    if new_play.play_type == PlayType.TWO_PAIR:
        return compare_two_pair(new_play, current_play)

    if new_play.rank_value > current_play.rank_value:
        return True
    if new_play.rank_value == current_play.rank_value:
        return new_play.max_suit > current_play.max_suit
    return False


def compare_two_pair(new_play, current_play):
    new_vals = sorted([symbol_to_int(c[0]) for c in new_play.cards])
    cur_vals = sorted([symbol_to_int(c[0]) for c in current_play.cards])

    new_counts = {}
    for v in new_vals:
        new_counts[v] = new_counts.get(v, 0) + 1
    new_pairs = sorted([v for v, c in new_counts.items() if c == 2], reverse=True)
    new_kicker = [v for v, c in new_counts.items() if c == 1]
    new_kicker = new_kicker[0] if new_kicker else 0

    cur_counts = {}
    for v in cur_vals:
        cur_counts[v] = cur_counts.get(v, 0) + 1
    cur_pairs = sorted([v for v, c in cur_counts.items() if c == 2], reverse=True)
    cur_kicker = [v for v, c in cur_counts.items() if c == 1]
    cur_kicker = cur_kicker[0] if cur_kicker else 0

    if new_pairs[0] != cur_pairs[0]:
        return new_pairs[0] > cur_pairs[0]
    if new_pairs[1] != cur_pairs[1]:
        return new_pairs[1] > cur_pairs[1]
    if new_kicker != cur_kicker:
        return new_kicker > cur_kicker

    new_max_suit = max(SUIT_RANK.get(c[1], 0) for c in new_play.cards)
    cur_max_suit = max(SUIT_RANK.get(c[1], 0) for c in current_play.cards)
    return new_max_suit > cur_max_suit


class Big2Game:
    def __init__(self, hands, partition_orders=None, verbose=False, player_names=None):
        self.hands = [list(h) for h in hands]
        self.partition_orders = partition_orders or [None] * 4
        self.current_player = 0
        self.current_play = None
        self.pass_count = 0
        self.first_round = True
        self.winner = None
        self.round_leader = 0
        self.verbose = verbose
        self.player_names = player_names or [f"Player {i}" for i in range(4)]
        self.round_num = 0
        self.turn_log = []

    def _log(self, msg):
        if self.verbose:
            print(msg)

    def _format_play(self, play):
        cards_str = ", ".join(f"{c[0]}{c[1]}" for c in play.cards)
        return f"{play.play_type.name}({cards_str})"

    def _format_hand(self, player_idx):
        return ", ".join(f"{c[0]}{c[1]}" for c in self.hands[player_idx])

    def find_starting_player(self):
        for i, hand in enumerate(self.hands):
            for card in hand:
                if card == ('3', 'd'):
                    return i
        return random.randint(0, 3)

    def get_valid_moves(self, hand, is_first_round=False, current_play=None, must_follow_leader=False):
        moves = []

        if is_first_round:
            must_have_3d = True
        else:
            must_have_3d = False

        singles = [(c,) for c in hand]
        if must_have_3d:
            singles = [s for s in singles if s[0] == ('3', 'd')]
        for s in singles:
            moves.append(Play(list(s), PlayType.SINGLE))

        for i in range(len(hand)):
            for j in range(i + 1, len(hand)):
                if symbol_to_int(hand[i][0]) == symbol_to_int(hand[j][0]):
                    pair = [hand[i], hand[j]]
                    if must_have_3d and not any(c == ('3', 'd') for c in pair):
                        continue
                    moves.append(Play(pair, PlayType.PAIR))

        for i in range(len(hand)):
            for j in range(i + 1, len(hand)):
                for k in range(j + 1, len(hand)):
                    vals = [symbol_to_int(hand[i][0]), symbol_to_int(hand[j][0]), symbol_to_int(hand[k][0])]
                    if len(set(vals)) == 1:
                        triple = [hand[i], hand[j], hand[k]]
                        if must_have_3d and not any(c == ('3', 'd') for c in triple):
                            continue
                        moves.append(Play(triple, PlayType.TRIPLE))

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
                            tp = [hand[i], hand[j], hand[k], hand[l]]
                            if must_have_3d and not any(c == ('3', 'd') for c in tp):
                                continue
                            moves.append(Play(tp, PlayType.TWO_PAIR))

        five_card_moves = self._get_5_card_moves(hand, must_have_3d)
        moves.extend(five_card_moves)

        if current_play is not None:
            moves = [m for m in moves if can_beat(m, current_play)]

        return moves

    def _get_5_card_moves(self, hand, must_have_3d=False):
        moves = []
        from game_rule import Player as CapsaPlayer
        cp = CapsaPlayer("_temp")
        cp.receive_cards(list(hand))

        straights = cp.straight_combinations()
        for s in straights:
            if must_have_3d and not any(c == ('3', 'd') for c in s):
                continue
            moves.append(Play(s, PlayType.STRAIGHT))

        flushes = cp.flush_combinations()
        for f in flushes:
            if must_have_3d and not any(c == ('3', 'd') for c in f):
                continue
            moves.append(Play(f, PlayType.FLUSH))

        full_houses = cp.full_house_combinations()
        for fh in full_houses:
            if must_have_3d and not any(c == ('3', 'd') for c in fh):
                continue
            moves.append(Play(fh, PlayType.FULL_HOUSE))

        four_kinds = cp.four_of_a_kind_combinations()
        for fk in four_kinds:
            if must_have_3d and not any(c == ('3', 'd') for c in fk):
                continue
            moves.append(Play(fk, PlayType.FOUR_OF_A_KIND))

        sf_combos = cp.straight_flush_combinations()
        for sf in sf_combos:
            if must_have_3d and not any(c == ('3', 'd') for c in sf):
                continue
            moves.append(Play(sf, PlayType.STRAIGHT_FLUSH))

        return moves

    def play_cards(self, player_idx, play):
        for card in play.cards:
            if card in self.hands[player_idx]:
                self.hands[player_idx].remove(card)

    def pass_turn(self):
        self.pass_count += 1

    def check_round_complete(self):
        if self.pass_count >= 3:
            self.current_play = None
            self.pass_count = 0
            return True
        return False

    def check_winner(self):
        for i, hand in enumerate(self.hands):
            if len(hand) == 0:
                self.winner = i
                return i
        return None

    def simulate_with_partition(self, partition_orders, ai_players):
        self.current_player = self.find_starting_player()
        self.current_play = None
        self.pass_count = 0
        self.first_round = True
        self.winner = None
        self.round_leader = self.current_player
        self.round_num = 1
        self.turn_log = []

        if self.verbose:
            self._log("=" * 60)
            self._log("GAME START")
            self._log("=" * 60)
            for i in range(4):
                name = self.player_names[i]
                hand_str = self._format_hand(i)
                self._log(f"  {name}: [{hand_str}]")
            self._log("")
            has_3d = any(c == ('3', 'd') for c in self.hands[self.current_player])
            if has_3d:
                self._log(f"{self.player_names[self.current_player]} holds 3 of diamonds - goes first!")
            else:
                self._log(f"No 3d dealt — {self.player_names[self.current_player]} goes first (random)!")
            self._log("")

        partition_idxs = [0, 0, 0, 0]
        partition_lists = []
        for p in partition_orders:
            if p is not None:
                partition_lists.append([list(c) for c in p])
            else:
                partition_lists.append(None)
        max_turns = 200
        turn_count = 0
        last_action_played = False
        last_player_who_played = self.current_player

        while self.winner is None and turn_count < max_turns:
            turn_count += 1
            hand = self.hands[self.current_player]
            player_name = self.player_names[self.current_player]

            player_partition = partition_lists[self.current_player]
            partition_remaining = player_partition if player_partition is not None else []

            ai = ai_players[self.current_player]
            play = ai.choose_move_constrained(hand, self.current_play, self.first_round, partition_remaining, self)

            if play is None:
                self.pass_turn()
                if self.verbose:
                    self._log(f"  {player_name:15} | Passes")
                if self.check_round_complete():
                    self.round_leader = last_player_who_played
                    self.first_round = False
                    self.current_play = None
                    self.pass_count = 0
                    self.current_player = self.round_leader
                    if self.verbose:
                        self._log(f"\n--- Round complete! New leader: {self.player_names[self.round_leader]} ---\n")
                    continue
                last_action_played = False
            else:
                self.play_cards(self.current_player, play)
                self.current_play = play
                self.pass_count = 0
                self.first_round = False
                last_player_who_played = self.current_player
                if player_partition is not None:
                    for i, combo in enumerate(player_partition):
                        combo_play = Play(combo, identify_play_type(combo))
                        if play == combo_play:
                            player_partition.pop(i)
                            break
                last_action_played = True
                if self.verbose:
                    remaining = len(self.hands[self.current_player])
                    self._log(f"  {player_name:15} | Plays: {self._format_play(play)} | Remaining: {remaining}")

            winner = self.check_winner()
            if winner is not None:
                break

            self.current_player = (self.current_player + 1) % 4

        if self.pass_count >= 3 and self.winner is None:
            self.round_num += 1
            self.pass_count = 0
            self.current_play = None
            self.first_round = False
            self.round_leader = last_player_who_played
            if self.verbose:
                self._log("")
                self._log(f"--- Round complete! New leader: {self.player_names[self.round_leader]} ---")

        if self.verbose:
            self._log("")
            self._log("=" * 60)
            self._log("GAME OVER")
            self._log("=" * 60)
            if self.winner is not None:
                winner_name = self.player_names[self.winner]
                self._log(f"Winner: {winner_name}!")
            else:
                self._log(f"No winner after {max_turns} turns.")
            self._log("Final cards remaining:")
            for i in range(4):
                name = self.player_names[i]
                remaining = len(self.hands[i])
                self._log(f"  {name:15} | {remaining}")
            self._log("=" * 60)

        return self.winner, [len(h) for h in self.hands]

    def _is_valid_starter(self, play, hand):
        if self.first_round:
            return any(c == ('3', 'd') for c in play.cards)
        return True
