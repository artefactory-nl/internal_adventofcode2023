from itertools import starmap
from typing import Iterable
from objects.day_seven.part_two.card import Card
from objects.day_seven.part_two.combination import Combination
from objects.day_seven.part_two.hand import Hand
        

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
# input_file = open("inputs/example-input-7-1.txt")
# input_file = open("inputs/edge-cases-7-2.txt")
