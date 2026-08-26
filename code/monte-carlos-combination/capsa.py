import random
from math import comb, perm

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
    
    def __str__(self):
        return f"{self.value}{self.suit}"

class Deck:
    VALUES = ['3', '4', '5', '6', '7', '8', '9', '10', 'j', 'q', 'k', 'a', '2']
    SUITS = ['d', 'c', 'h', 's']
    
    def __init__(self):
        self.cards = []
        self.create_deck()
    
    def create_deck(self):
        self.cards = [(value, suit) for value in self.VALUES for suit in self.SUITS]
    
    def get_random_cards(self, n):
        array_of_index = random.sample(range(0, 52), n)
        array_of_index.sort()
        return [self.cards[i] for i in array_of_index]

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
    
    def reset_hand(self):
        self.hand = []
        
    def receive_cards(self, cards):
        self.hand.extend(cards)
    
    def symbol_to_int(self, symbol):
        if(symbol == 'a'):
            return 14
        elif(symbol == 'j'):
            return 11
        elif(symbol == 'q'):
            return 12
        elif(symbol == 'k'):
            return 13
        elif(symbol == '2'):
            return 15
        else:
            return int(symbol)
        
    def hand_to_int(self):
        temp = []
        for i, j in self.hand:
            temp.append(self.symbol_to_int(i))
        return temp

    def exist_pair(self):
        temp = self.hand_to_int()
        for i in range(3, 16):
            if(temp.count(i) >= 2):
                return True
        return False
    
    def exist_three_of_a_kind(self):
        temp = self.hand_to_int()
        for i in range(3, 16):
            if(temp.count(i) >= 3):
                return True
        return False
    
    def exist_straight(self):
        temp = self.hand_to_int()
        for i in range(13):
            if(temp[i] + 1 in temp and temp[i] + 2 in temp and temp[i] + 3 in temp and temp[i] + 4 in temp and temp[i] < 12):
                return True
            elif(temp[i] == 14 and 15 in temp and 3 in temp and 4 in temp and 5 in temp):
                return True
            elif(temp[i] == 15 and 3 in temp and 4 in temp and 5 in temp and 6 in temp):
                return True
        return False

    def exist_flush(self):
        temp = []
        for i, j in self.hand:
            temp.append(j)
        for i in range(0, 4):
            if(temp.count(temp[i]) >= 5):
                return True
        return False
    
    def exist_full_house(self):
        temp = self.hand_to_int()
        for i in range(3, 16):
            if(temp.count(i) >= 3):
                for j in range(3, 16 ):
                    if(temp.count(j) >= 2):
                        return True
        return False
    
    def exist_four_of_a_kind(self):
        temp = self.hand_to_int()
        for i in range(3, 16):
            if(temp.count(i) == 4):
                return True
        return False
    
    def exist_straight_flush(self):
        temp = self.hand_to_int()
        for i in range(0, 9):
            if(temp[i] + 1 in temp and temp[i] + 2 in temp and temp[i] + 3 in temp and temp[i] + 4 in temp):
                for j, k in self.hand:
                    if(k == self.hand[i][1] and k == self.hand[i+1][1] and k == self.hand[i+2][1] and k == self.hand[i+3][1] and k == self.hand[i+4][1]):
                        return True
        return False

    def pair_combinations(self):
        temp = self.hand_to_int()
        all_pairs = []
        for i in range(0, 13):
            for j in range(i + 1, 13):
                if(temp[i] == temp[j]):
                    all_pairs.append((self.hand[i], self.hand[j]))
                else:
                    break
        return all_pairs

    def print_pair_combinations(self):
        pairs = self.pair_combinations()
        print(f"Found {len(pairs)} possible pairs:")
        for i, pair in enumerate(pairs, 1):
            print(f"Pair {i}: {' '.join(str(card) for card in pair)}")

    def three_of_a_kind_combinations(self):
        temp = self.hand_to_int()
        all_three_of_a_kinds = []
        for i in range(0, 13):
            for j in range(i + 1, 13):
                for k in range(j + 1, 13):
                    if(temp[i] == temp[j] and temp[j] == temp[k]):
                        all_three_of_a_kinds.append((self.hand[i], self.hand[j], self.hand[k]))
                    else:
                        break
        return all_three_of_a_kinds

    def print_three_of_a_kind_combinations(self):
        three_of_a_kinds = self.three_of_a_kind_combinations()
        print(f"Found {len(three_of_a_kinds)} possible three of a kinds:")
        for i, three_of_a_kind in enumerate(three_of_a_kinds, 1):
            print(f"Three of a kind {i}: {' '.join(str(card) for card in three_of_a_kind)}")

    def straight_combinations(self):
        temp = self.hand_to_int()
        small_straights = []
        big_straights = []
        checked = []

        for i in range(13):
            # Check if we have 5 consecutive cards
            if(temp[i] + 1 in temp and 
            temp[i] + 2 in temp and 
            temp[i] + 3 in temp and 
            temp[i] + 4 in temp and
            not temp[i] in checked and
            temp[i] < 12):
                
                checked.append(temp[i])

                cards_v1 = [(j, k) for j, k in self.hand if self.symbol_to_int(j) == temp[i]]
                cards_v2 = [(j, k) for j, k in self.hand if self.symbol_to_int(j) == temp[i] + 1]
                cards_v3 = [(j, k) for j, k in self.hand if self.symbol_to_int(j) == temp[i] + 2]
                cards_v4 = [(j, k) for j, k in self.hand if self.symbol_to_int(j) == temp[i] + 3]
                cards_v5 = [(j, k) for j, k in self.hand if self.symbol_to_int(j) == temp[i] + 4]

                for c1 in cards_v1:
                    for c2 in cards_v2:
                        for c3 in cards_v3:
                            for c4 in cards_v4:
                                for c5 in cards_v5:
                                    straight = tuple([c1, c2, c3, c4, c5])   
                                    if straight not in big_straights:  
                                        big_straights.append(straight)

            elif(temp[i] == 14 and 15 in temp and 3 in temp and 4 in temp and 5 in temp and not 14 in checked):
                cards_v1 = [(j, k) for j, k in self.hand if self.symbol_to_int(j) == 14]
                cards_v2 = [(j, k) for j, k in self.hand if self.symbol_to_int(j) == 15]
                cards_v3 = [(j, k) for j, k in self.hand if self.symbol_to_int(j) == 3]
                cards_v4 = [(j, k) for j, k in self.hand if self.symbol_to_int(j) == 4]
                cards_v5 = [(j, k) for j, k in self.hand if self.symbol_to_int(j) == 5]
                for c1 in cards_v1:
                    for c2 in cards_v2:
                        for c3 in cards_v3:
                            for c4 in cards_v4:
                                for c5 in cards_v5:
                                    straight = tuple([c1, c2, c3, c4, c5])  
                                    if straight not in small_straights:  
                                        small_straights.append(straight)

            elif(temp[i] == 15 and 3 in temp and 4 in temp and 5 in temp and 6 in temp and not 15 in checked):
                cards_v1 = [(j, k) for j, k in self.hand if self.symbol_to_int(j) == 15]
                cards_v2 = [(j, k) for j, k in self.hand if self.symbol_to_int(j) == 3]
                cards_v3 = [(j, k) for j, k in self.hand if self.symbol_to_int(j) == 4]
                cards_v4 = [(j, k) for j, k in self.hand if self.symbol_to_int(j) == 5]
                cards_v5 = [(j, k) for j, k in self.hand if self.symbol_to_int(j) == 6]
                for c1 in cards_v1:
                    for c2 in cards_v2:
                        for c3 in cards_v3:
                            for c4 in cards_v4:
                                for c5 in cards_v5:
                                    straight = tuple([c1, c2, c3, c4, c5])  
                                    if straight not in small_straights:  
                                        small_straights.append(straight)
                                        
        small_straights = [list(s) for s in small_straights]
        big_straights = [list(s) for s in big_straights]
        
        combined_straights = small_straights + big_straights
        return combined_straights
    
    def print_straight_combinations(self):
        straights = self.straight_combinations()
        print(f"Found {len(straights)} possible straights:")
        for i, straight in enumerate(straights, 1):
            print(f"Straight {i}: {' '.join(str(card) for card in straight)}")
            
    def flush_combinations(self):
        all_flushes = []

        diamonds = [(j, k) for j, k in self.hand if k == 'd']
        clubs = [(j, k) for j, k in self.hand if k == 'c']
        hearts = [(j, k) for j, k in self.hand if k == 'h']
        spades = [(j, k) for j, k in self.hand if k == 's']
        for suit_cards in [diamonds, clubs, hearts, spades]:
            if len(suit_cards) >= 5:
                for i in range(len(suit_cards) - 4):
                    for j in range(i + 1, len(suit_cards) - 3):
                        for k in range(j + 1, len(suit_cards) - 2):
                            for l in range(k + 1, len(suit_cards) - 1):
                                for m in range(l + 1, len(suit_cards)):
                                    flush = [suit_cards[i], suit_cards[j], suit_cards[k], suit_cards[l], suit_cards[m]]
                                    all_flushes.append(flush)
        return all_flushes   

    def print_flush_combinations(self):
        flushes = self.flush_combinations()
        print(f"Found {len(flushes)} possible flushes:")
        for i, flush in enumerate(flushes, 1):
            print(f"Flush {i}: {' '.join(str(card) for card in flush)}")

    def full_house_combinations(self):
        all_full_houses = []
        if(self.exist_three_of_a_kind() and self.exist_pair()):
            pairs = self.pair_combinations()
            three_of_a_kinds = self.three_of_a_kind_combinations()
            for three_of_a_kind in three_of_a_kinds:
                for pair in pairs:
                    if not three_of_a_kind[0] in pair and not three_of_a_kind[1] in pair and not three_of_a_kind[2] in pair:
                        all_full_houses.append(three_of_a_kind + pair)
        return all_full_houses
    
    def print_full_house_combinations(self):
        full_houses = self.full_house_combinations()
        print(f"Found {len(full_houses)} possible full houses:")
        for i, full_house in enumerate(full_houses, 1):
            print(f"Full house {i}: {' '.join(str(card) for card in full_house)}")
            
    def four_of_a_kind_combinations(self):
        temp = self.hand_to_int()
        checked = []
        all_four_of_a_kinds = []
        for i in range(3, 16):
            if temp.count(i) == 4 and i not in checked:
                checked.append(i)
                four_cards = [card for card in self.hand if self.symbol_to_int(card[0]) == i]
                kickers = [card for card in self.hand if self.symbol_to_int(card[0]) != i]
                for kicker in kickers:
                    all_four_of_a_kinds.append(four_cards + [kicker])
        return all_four_of_a_kinds
    
    def print_four_of_a_kind_combinations(self):
        four_of_a_kinds = self.four_of_a_kind_combinations()
        print(f"Found {len(four_of_a_kinds)} possible four of a kinds:")
        for i, four_of_a_kind in enumerate(four_of_a_kinds, 1):
            print(f"Four of a kind {i}: {' '.join(str(card) for card in four_of_a_kind)}")

    def straight_flush_combinations(self):
        all_straight_flushes = []
        if(self.exist_straight() and self.exist_flush()):
            straights = self.straight_combinations()
            flushes = self.flush_combinations()
            for straight in straights:
                if straight in flushes:
                    all_straight_flushes.append(straight)
        return all_straight_flushes
    
    def print_straight_flush_combinations(self):
        straight_flushes = self.straight_flush_combinations()
        print(f"Found {len(straight_flushes)} possible straight flushes:")
        for i, straight_flush in enumerate(straight_flushes, 1):
            print(f"Straight flush {i}: {' '.join(str(card) for card in straight_flush)}")

    def number_of_combinations_pair(self):
        temp = self.hand_to_int()
        count = 0
        for i in range(3, 16):
            if(temp.count(i) >= 2):
                count += comb(temp.count(i), 2)
        return count
    
    def number_of_combinations_three_of_a_kind(self):
        temp = self.hand_to_int()
        count = 0
        for i in range(3, 16):
            if(temp.count(i) >= 3):
                count += comb(temp.count(i), 3)
        return count
    
    def number_of_combinations_straight(self):
        temp = self.hand_to_int()
        checked = []
        count = 0
        for i in range(13):
            if(temp[i] + 1 in temp and temp[i] + 2 in temp and temp[i] + 3 in temp and temp[i] + 4 in temp and temp[i] < 12 and not temp[i] in checked):
                checked.append(temp[i])
                count += temp.count(temp[i]) * temp.count(temp[i] + 1) * temp.count(temp[i] + 2) * temp.count(temp[i] + 3) * temp.count(temp[i] + 4)
            elif(temp[i] == 14 and 15 in temp and 3 in temp and 4 in temp and 5 in temp and not temp[i] in checked):
                checked.append(temp[i])
                count += temp.count(14) * temp.count(15) * temp.count(3) * temp.count(4) * temp.count(5)
            elif(temp[i] == 15 and 3 in temp and 4 in temp and 5 in temp and 6 in temp and not temp[i] in checked):
                checked.append(temp[i])
                count += temp.count(15) * temp.count(3) * temp.count(4) * temp.count(5) * temp.count(6)
        return count
    
    def number_of_combinations_flush(self):
        temp = []
        for i, j in self.hand:
            temp.append(j)
        count = 0
        for i in range(0, 4):
            if(temp.count(temp[i]) >= 5):
                count += comb(temp.count(temp[i]), 5)
        return count
    
    def number_of_combinations_full_house(self):
    # Count cards
        count_threes = 0         
        count_fours = 0   
        count_pairs = 0      
        for i in range(3, 16):             
            if(self.hand_to_int().count(i) == 4):                 
                count_fours += 1             
            elif(self.hand_to_int().count(i) == 3):                 
                count_threes += 1 
            elif(self.hand_to_int().count(i) == 2):                 
                count_pairs += 1

        return (
            comb(4,2) * comb(3,3) * count_threes * count_fours +  
            comb(4,3) * comb(3,2) * count_threes * count_fours +
            comb(4,3) * comb(4,2) * perm(count_fours,2) +
            comb(3,3) * comb(3,2) * perm(count_threes,2) +
            (comb(4,3) * comb(2,2) * count_fours + 
            comb(3,3) * comb(2,2) * count_threes) * count_pairs
        )
    
    def number_of_combinations_four_of_a_kind(self):
        temp = self.hand_to_int()
        count = 0
        for i in range(3, 16):
            if(temp.count(i) == 4):
                count += comb(temp.count(i), 4) * comb(9,1)
        return count

    def number_of_combinations_straight_flush(self):
        diamond = []
        club = []
        heart = []
        spade = []
        for i, j in self.hand:
            if(j == 'd'):
                diamond.append(self.symbol_to_int(i))
            elif(j == 'c'):
                club.append(self.symbol_to_int(i))
            elif(j == 'h'):
                heart.append(self.symbol_to_int(i))
            elif(j == 's'):
                spade.append(self.symbol_to_int(i))
        count = 0
        if(len(diamond) >= 5):
            for i in range(len(diamond)):
                if(diamond[i] + 1 in diamond and diamond[i] + 2 in diamond and diamond[i] + 3 in diamond and diamond[i] + 4 in diamond):
                    count += 1
        if(len(club) >= 5):
            for i in range(len(club)):
                if(club[i] + 1 in club and club[i] + 2 in club and club[i] + 3 in club and club[i] + 4 in club):
                    count += 1
        if(len(heart) >= 5):
            for i in range(len(heart)):
                if(heart[i] + 1 in heart and heart[i] + 2 in heart and heart[i] + 3 in heart and heart[i] + 4 in heart):
                    count += 1
        if(len(spade) >= 5):
            for i in range(len(spade)):
                if(spade[i] + 1 in spade and spade[i] + 2 in spade and spade[i] + 3 in spade and spade[i] + 4 in spade):
                    count += 1
        return count
    
def main():
    deck = Deck()
    player = Player("Player 1")
    player.receive_cards(deck.get_random_cards(13))
    print([str(card) for card in player.hand])
    print("\nExist pair:" + str(player.exist_pair()))
    print("Exist three of a kind:" + str(player.exist_three_of_a_kind()))
    print("Exist straight:" + str(player.exist_straight()))
    print("Exist flush:" + str(player.exist_flush()))
    print("Exist full house:" + str(player.exist_full_house()))
    print("Exist four of a kind:" + str(player.exist_four_of_a_kind()))
    print("Exist straight flush:" + str(player.exist_straight_flush()))
    print("Combinations of pair: " + str(player.number_of_combinations_pair()))
    print("Combinations of three of a kind: " + str(player.number_of_combinations_three_of_a_kind()))
    print("Combinations of straight: " + str(player.number_of_combinations_straight()))
    print("Combinations of flush: " + str(player.number_of_combinations_flush()))
    print("Combinations of full house: " + str(player.number_of_combinations_full_house()))
    print("Combinations of four of a kind: " + str(player.number_of_combinations_four_of_a_kind()))
    print("Combinations of straight flush: " + str(player.number_of_combinations_straight_flush()))


    player.print_pair_combinations()
    player.print_three_of_a_kind_combinations()
    player.print_straight_combinations()
    player.print_flush_combinations()
    player.print_full_house_combinations()
    player.print_four_of_a_kind_combinations()
    player.print_straight_flush_combinations()
if __name__ == "__main__":
    main()