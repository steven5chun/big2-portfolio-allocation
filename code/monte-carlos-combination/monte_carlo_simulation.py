from capsa import *


def main():
    deck = Deck()
    player = Player("test")
    n = 1000000

    result = [0] * 7
    for i in range(n):
        player.receive_cards(deck.get_random_cards(13))
        if player.exist_pair():
            result[0] += 1
        if player.exist_three_of_a_kind():
            result[1] += 1
        if player.exist_straight():
            result[2] += 1
        if player.exist_flush():
            result[3] += 1
        if player.exist_full_house():
            result[4] += 1
        if player.exist_four_of_a_kind():
            result[5] += 1
        if player.exist_straight_flush():
            result[6] += 1

        player.reset_hand()

    print("Pair: ", 100 * result[0]/n, "%")
    print("Three of a kind: ",100 * result[1]/n, "%")
    print("Straight: ",100 * result[2]/n, "%")
    print("Flush: ",100 * result[3]/n, "%")
    print("Full house: ",100 * result[4]/n, "%")
    print("Four of a kind: ",100 * result[5]/n, "%")
    print("Straight flush: ",100 * result[6]/n, "%")

if __name__ == '__main__':
    main()