from itertools import starmap
from typing import Iterable
from objects.day_seven.part_one.card import Card
from objects.day_seven.part_one.combination import Combination
from objects.day_seven.part_one.hand import Hand

        
def parse_hand_and_bids(lines: list[str]) -> int:
    raw_cards_and_bids = [tuple(line.split(" ")) for line in lines]
    make_hand = lambda cards: Hand(cards=[Card(rank=rank) for rank in cards], make_combination=Combination)
    make_hand_and_bid = lambda cards, bid: (make_hand(cards=cards), int(bid))
    return starmap(make_hand_and_bid, raw_cards_and_bids)

def calculate_total_winnings(hands_and_bids: Iterable[tuple[Hand, int]]) -> int:
    bid_scores = sorted(hands_and_bids, key=lambda v: v[0])
    ranked_bid_scores = enumerate(bid_scores)
    calculate_score = lambda rank, hand_bid: (rank+1) * hand_bid[1]
    return sum(starmap(calculate_score, ranked_bid_scores))


input_file = open("inputs/problem-7.txt")

input_lines = input_file.read().splitlines()
parsed_hands_and_bids = parse_hand_and_bids(input_lines)
answer = calculate_total_winnings(parsed_hands_and_bids)
print(answer)

## TESTING ##
# hand_1 = Hand(cards=[Card(9), Card(Q), Card(Q), Card(Q), Card(Q)])
# hand_2 = Hand(cards=[Card(T), Card(T), Card(6), Card(T), Card(T)])
# hand_3 = Hand(cards=[Card(K), Card(T), Card(T), Card(T), Card(T)]])
# hand_4 = Hand(cards=[Card(K), Card(9), Card(K), Card(K), Card(K)])
# hand_5 = Hand(cards=[Card("A"), Card("J"), Card("3"), Card("3"), Card("8")])
# hand_6 = Hand(cards=[Card("A"), Card("A"), Card("2"), Card("K"), Card("2")])
# hand_7 = Hand(cards=[Card("A"), Card("A"), Card("9"), Card("3"), Card("3")])

# hand_7.get_highest_combination()
# hand_6.get_highest_combination()
# hand_2 > hand_1
# hand_1 > hand_3