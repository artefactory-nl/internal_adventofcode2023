from dataclasses import dataclass, field
from functools import total_ordering
from typing import Self
from objects.day_seven.part_two.card import Card
from objects.day_seven.base_hand import BaseHand

@dataclass(frozen=True)
@total_ordering
class Hand(BaseHand):
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
        super().__post_init__()
        if len(self.cards) != 5:
            raise ValueError("Provided a number of cards different than 5.")
    
    def get_highest_combination(self) -> str:
        cards_in_hand = sorted([card for card in self.cards], key=lambda card: card.get_numerical_value())
        ranks_in_hand = [card.get_rank() for card in cards_in_hand]

        def sort_by_count_and_dedup(card_ranks: list[str], slice_ix=None) -> list[str]:
            count_cards = lambda card_rank: (
                card_ranks.count(card_rank), Card(rank=card_rank).get_numerical_value())
            return sorted(dict.fromkeys(card_ranks[slice_ix:]), key=count_cards, reverse=True)

        ## SPECIAL CASE ONLY IF CARD IS J ##
        card_rank = ranks_in_hand[0]
        if card_rank == "J":
            if ranks_in_hand.count(card_rank) in [4, 5]: 
                return self.make_combination(cards=cards_in_hand)
            elif ranks_in_hand.count(card_rank) == 3:
                if len(dict.fromkeys(ranks_in_hand[3:])) == 1:
                    return self.make_combination(cards=cards_in_hand)
                else: return self.make_combination(cards=cards_in_hand[:3]+cards_in_hand[-1:])
            elif ranks_in_hand.count(card_rank) == 2:
                if len(dict.fromkeys(ranks_in_hand[2:])) == 1:
                    return self.make_combination(cards=cards_in_hand)
                card_rank_left = sort_by_count_and_dedup(card_ranks=ranks_in_hand, slice_ix=2)[0]
                if ranks_in_hand.count(card_rank_left) == 3:
                    return self.make_combination(cards=cards_in_hand)
                if ranks_in_hand.count(card_rank_left) == 2:
                    return self.make_combination(cards=cards_in_hand[:2]+[Card(rank=card_rank_left)]*2)
                return self.make_combination(cards=cards_in_hand[:2]+cards_in_hand[-1:])
            else:
                card_rank_left = sort_by_count_and_dedup(card_ranks=ranks_in_hand, slice_ix=2)[0]
                try:
                    next_card_rank_left = sort_by_count_and_dedup(card_ranks=ranks_in_hand, slice_ix=2)[1]
                except IndexError:
                    next_card_rank_left = None
                if ranks_in_hand.count(card_rank_left) == 4:
                    return self.make_combination(cards=cards_in_hand)
                if ranks_in_hand.count(card_rank_left) == 3:
                    return self.make_combination(cards=cards_in_hand[:1]+[Card(rank=card_rank_left)]*3)
                if ranks_in_hand.count(card_rank_left) == 2:
                    if next_card_rank_left:
                        if ranks_in_hand.count(next_card_rank_left) == 2: # Check potential full house
                            return self.make_combination(cards=cards_in_hand[:1]+[Card(rank=card_rank_left)]*2+[Card(rank=next_card_rank_left)]*2)
                    return self.make_combination(cards=cards_in_hand[:1]+[Card(rank=card_rank_left)]*2)
                return self.make_combination(cards=cards_in_hand[:1]+cards_in_hand[-1:])
        
        ## BASE CASE -> NO JOKERS, CALL SUPER ##
        else:
            return super().get_highest_combination()
    
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
