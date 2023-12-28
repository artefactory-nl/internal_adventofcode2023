from dataclasses import dataclass, field
from functools import total_ordering
from typing import Self, Type
from abc import abstractmethod
from objects.day_seven.part_one.card import Card
from objects.day_seven.base_combination import BaseCombination

@dataclass(frozen=True)
@total_ordering
class BaseHand:
    cards: list[Card]
    make_combination: Type[BaseCombination]
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
    
    @abstractmethod
    def get_highest_combination(self) -> str:
        raise NotImplementedError("get_highest_combination() is not implemented.")
    
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
