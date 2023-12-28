from abc import abstractmethod
from dataclasses import dataclass, field
from functools import total_ordering
from typing import Self, final
from objects.day_seven.part_one.card import Card


@dataclass(frozen=True)
@total_ordering
class BaseCombination:
    cards: list[Card]
    possible_combinations: list[str] = field(
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
        if len(self.cards) > 5 or len(self.cards) == 0:
            raise ValueError("Provided a number of cards higher than 5 or no cards at all.")
        
    @abstractmethod
    def get_type(self) -> str:
        pass
    
    @abstractmethod
    def _perform_comparison_between_combinations(self, other: Self, operation: str) -> bool:
        pass


    @final
    def get_priority_of_combination(self) -> int:
        return len(self.possible_combinations) - self.possible_combinations.index(self.get_type())
    
    @final
    def __repr__(self) -> str: return f"Combination({str([card.get_rank() for card in self.cards])})"

    @final
    def __len__(self) -> str: return len(self.cards)
    
    @final
    def __getitem__(self, index: int) -> str:
        if (not isinstance(index, int)) or (index > 4):
            raise ValueError("Incorrect index provided: number must be an int lower than 5.")
        else: return self.cards[index].rank

    @final
    def __gt__(self, other: Self) -> bool:
        return self._perform_comparison_between_combinations(other, operation="greater-than")
    
    @final
    def __lt__(self, other: Self) -> bool:
        return self._perform_comparison_between_combinations(other, operation="less-than")

    @final
    def __eq__(self, other: Self) -> bool:
        return self._perform_comparison_between_combinations(other, operation="equal")

    @final
    def __ge__(self, other: Self) -> bool:
        return self._perform_comparison_between_combinations(other, operation="greater-than-or-equal")

    @final
    def __le__(self, other: Self) -> bool:
        return self._perform_comparison_between_combinations(other, operation="less-than-or-equal")
