from dataclasses import dataclass, field
from functools import total_ordering
from typing import Self
from objects.day_seven.part_one.card import Card
from objects.day_seven.part_one.combination import Combination

@dataclass(frozen=True)
@total_ordering
class Hand:
    cards: list[Card]
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
    
    def __post_init__(self):
        if len(self.cards) != 5:
            raise ValueError("Provided a number of cards different than 5.")
    
    def get_highest_combination(self) -> str:
        ranks_in_hand = sorted([card.get_rank() for card in self.cards])
        for card_rank in dict.fromkeys(ranks_in_hand):
            if ranks_in_hand.count(card_rank) in [4, 5]: return Combination([Card(card_rank)] * ranks_in_hand.count(card_rank)) # 4/5 of a kind
            if ranks_in_hand.count(card_rank) == 3:
                if ranks_in_hand.count(ranks_in_hand[-1]) == 2:
                    return Combination(cards=[Card(rank=card_rank)] * 3 + [Card(rank=ranks_in_hand[-1])] * 2) # Full house
                else: return Combination(cards=[Card(rank=card_rank)] * 3) # 3 of a kind
            if ranks_in_hand.count(card_rank) == 2:
                if ranks_in_hand.count(ranks_in_hand[-1]) == 3:
                    return Combination(cards=[Card(rank=card_rank)] * 2 + [Card(rank=ranks_in_hand[-1])] * 3) # Full house
                # Check if any of the other ranks is present twice in the hand to determine combination value
                remaining_card_ranks = ranks_in_hand[ranks_in_hand.index(card_rank)+2:]
                ranks_excluding_current_card = filter(lambda rank: rank != card_rank, dict.fromkeys(ranks_in_hand))
                for rank in ranks_excluding_current_card:
                    if remaining_card_ranks.count(rank) == 2:
                        return Combination(cards=[Card(rank=card_rank)] * 2 + [Card(rank=rank)] * 2) # Double pair
                return Combination(cards=[Card(rank=card_rank)] * 2) # Single pair
        max_rank = max(self.cards).get_rank()
        return Combination(cards=[Card(rank=max_rank)])
    
    def _perform_comparison_between_hands(self, other: Self, operation: str) -> bool:
        if operation not in ["greater-than", "less-than", "equal", "greater-than-or-equal", "less-than-or-equal"]:
            raise ValueError("Provide one comparison operation of the following three: 'greater-than', 'less-than', 'equal', 'greater-than-or-equal', 'less-than-or-equal'")
        
        own_hand_highest_combination = self.get_highest_combination()
        other_hand_highest_combination = other.get_highest_combination()
        
        if own_hand_highest_combination.get_type() != other_hand_highest_combination.get_type():
            if operation == "greater-than": return own_hand_highest_combination > other_hand_highest_combination
            if operation == "greater-than-or-equal": return own_hand_highest_combination >= other_hand_highest_combination
            if operation == "less-than": return own_hand_highest_combination < other_hand_highest_combination
            if operation == "less-than-or-equal": return own_hand_highest_combination <= other_hand_highest_combination
            if operation == "equal": return own_hand_highest_combination == other_hand_highest_combination

        else:
            for card_position in range(5):
                if self.cards[card_position] == other.cards[card_position]:
                    continue
                elif self.cards[card_position] > other.cards[card_position]:
                    return (operation in ["greater-than", "greater-than-or-equal"])
                elif self.cards[card_position] < other.cards[card_position]:
                    return (operation in ["less-than", "less-than-or-equal"])
            return (operation in ["equal", "greater-than-or-equal", "less-than-or-equal"])
    
    def __repr__(self) -> str: return f"Hand({str([card.get_rank() for card in self.cards])})"

    def __len__(self) -> str: return len(self.cards)
    
    def __getitem__(self, index: int) -> str:
        if (not isinstance(index, int)) or (index > 4):
            raise ValueError("Incorrect index provided: number must be an int lower than 5.")
        else: return self.cards[index].rank

    def __gt__(self, other: Self) -> bool:
        return self._perform_comparison_between_hands(other, operation="greater-than")
    
    def __lt__(self, other: Self) -> bool:
        return self._perform_comparison_between_hands(other, operation="less-than")

    def __eq__(self, other: Self) -> bool:
        return self._perform_comparison_between_hands(other, operation="equal")

    def __ge__(self, other: Self) -> bool:
        return self._perform_comparison_between_hands(other, operation="greater-than-or-equal")

    def __le__(self, other: Self) -> bool:
        return self._perform_comparison_between_hands(other, operation="less-than-or-equal")
