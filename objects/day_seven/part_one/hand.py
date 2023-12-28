from dataclasses import dataclass, field
from functools import total_ordering
from objects.day_seven.part_one.card import Card
from objects.day_seven.part_one.combination import Combination
from objects.day_seven.base_hand import BaseHand

@dataclass(frozen=True)
@total_ordering
class Hand(BaseHand):
    make_combination: field(init=False, default=Combination)
    possible_hands: list[str] = field(
        init=False,
        default_factory=lambda: [
            "five-of-a-kind", 
            "four-of-a-kind", 
            "full-house", 
            "three-of-a-kind", 
            "two-pair", 
            "one-pair", 
            "high-card"
        ]
    )

    def get_highest_combination(self) -> str:
        ranks_in_hand = sorted([card.get_rank() for card in self.cards])
        for card_rank in dict.fromkeys(ranks_in_hand):
            if ranks_in_hand.count(card_rank) in [4, 5]: return self.make_combination([Card(card_rank)] * ranks_in_hand.count(card_rank)) # 4/5 of a kind
            if ranks_in_hand.count(card_rank) == 3:
                if ranks_in_hand.count(ranks_in_hand[-1]) == 2:
                    return self.make_combination(cards=[Card(rank=card_rank)] * 3 + [Card(rank=ranks_in_hand[-1])] * 2) # Full house
                else: return self.make_combination(cards=[Card(rank=card_rank)] * 3) # 3 of a kind
            if ranks_in_hand.count(card_rank) == 2:
                if ranks_in_hand.count(ranks_in_hand[-1]) == 3:
                    return self.make_combination(cards=[Card(rank=card_rank)] * 2 + [Card(rank=ranks_in_hand[-1])] * 3) # Full house
                # Check if any of the other ranks is present twice in the hand to determine combination value
                remaining_card_ranks = ranks_in_hand[ranks_in_hand.index(card_rank)+2:]
                ranks_excluding_current_card = filter(lambda rank: rank != card_rank, dict.fromkeys(ranks_in_hand))
                for rank in ranks_excluding_current_card:
                    if remaining_card_ranks.count(rank) == 2:
                        return self.make_combination(cards=[Card(rank=card_rank)] * 2 + [Card(rank=rank)] * 2) # Double pair
                return self.make_combination(cards=[Card(rank=card_rank)] * 2) # Single pair
        max_rank = max(self.cards).get_rank()
        return self.make_combination(cards=[Card(rank=max_rank)])