import random
from big2_game import Play, PlayType, can_beat, symbol_to_int, SUIT_RANK


class SmartAI:
    def __init__(self, name="SmartAI"):
        self.name = name

    def choose_move(self, hand, current_play, is_first_round, game=None):
        valid_moves = self._get_valid_moves(hand, current_play, is_first_round)

        if not valid_moves:
            return None

        if current_play is None:
            return self._choose_lead(valid_moves, hand)
        else:
            return self._choose_beat(valid_moves, hand, current_play)

    def _get_valid_moves(self, hand, current_play, is_first_round):
        from big2_game import Big2Game
        temp_game = Big2Game([hand, [], [], []])
        return temp_game.get_valid_moves(hand, is_first_round=is_first_round, current_play=current_play)

    def _choose_lead(self, valid_moves, hand):
        scored = []
        for move in valid_moves:
            score = self._score_lead(move, hand)
            scored.append((score, move))

        scored.sort(key=lambda x: x[0])
        return scored[0][1]

    def _score_lead(self, move, hand):
        score = 0

        card_values = [symbol_to_int(c[0]) for c in move.cards]
        max_val = max(card_values)

        score += max_val * 10

        if move.play_type == PlayType.SINGLE:
            score += 0
        elif move.play_type == PlayType.PAIR:
            score -= 5
        elif move.play_type == PlayType.TRIPLE:
            score -= 10
        elif move.play_type == PlayType.TWO_PAIR:
            score -= 15
        elif move.play_type in (PlayType.STRAIGHT, PlayType.FLUSH, PlayType.FULL_HOUSE,
                                PlayType.FOUR_OF_A_KIND, PlayType.STRAIGHT_FLUSH):
            score -= 20

        cards_left = len(hand) - len(move.cards)
        if cards_left <= 3:
            score += 50

        has_2 = any(symbol_to_int(c[0]) == 15 for c in hand if c not in move.cards)
        if has_2:
            score -= 5

        return score

    def _choose_beat(self, valid_moves, hand, current_play):
        scored = []
        for move in valid_moves:
            score = self._score_beat(move, hand, current_play)
            scored.append((score, move))

        scored.sort(key=lambda x: x[0])
        return scored[0][1]

    def _score_beat(self, move, hand, current_play):
        score = 0

        card_values = [symbol_to_int(c[0]) for c in move.cards]
        max_val = max(card_values)

        score += max_val * 10

        if max_val > 13:
            score += 30

        cards_left = len(hand) - len(move.cards)
        if cards_left <= 3:
            score += 50

        remaining = [c for c in hand if c not in move.cards]
        has_2_left = any(symbol_to_int(c[0]) == 15 for c in remaining)
        if not has_2_left and max_val > 13:
            score += 20

        return score


class RandomAI:
    def __init__(self, name="RandomAI"):
        self.name = name

    def choose_move(self, hand, current_play, is_first_round, game=None):
        from big2_game import Big2Game
        temp_game = Big2Game([hand, [], [], []])
        valid_moves = temp_game.get_valid_moves(hand, is_first_round=is_first_round, current_play=current_play)

        if not valid_moves:
            return None

        return random.choice(valid_moves)
