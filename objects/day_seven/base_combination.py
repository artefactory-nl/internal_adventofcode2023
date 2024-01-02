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

    def get_type(self) -> str:
        cards_in_combination = sorted([card for card in self.cards], key=lambda card: card.get_numerical_value())
        ranks_in_combination = [card.get_rank() for card in cards_in_combination]
        if (len(set(ranks_in_combination)) == 1) and (len(self.cards) == 5): return "five-of-a-kind"
        for card_rank in dict.fromkeys(ranks_in_combination):
            if ranks_in_combination.count(card_rank) == 4: return "four-of-a-kind"
            if ranks_in_combination.count(card_rank) == 3:
                if ranks_in_combination.count(ranks_in_combination[-1]) == 2: return "full-house"
                else: return "three-of-a-kind"
            if ranks_in_combination.count(card_rank) == 2:
                if ranks_in_combination.count(ranks_in_combination[-1]) == 3: return "full-house"
                # Check if any of the other ranks is present twice in the hand to determine if it is a double pair
                remaining_card_ranks = ranks_in_combination[ranks_in_combination.index(card_rank)+2:]
                ranks_excluding_current_card = filter(lambda rank: rank != card_rank, dict.fromkeys(ranks_in_combination))
                if any(remaining_card_ranks.count(rank) == 2 for rank in ranks_excluding_current_card):
                    return "two-pair"
                else: return "one-pair"
            else: return "high-card"

    def _perform_comparison_between_combinations(self, other: Self, operation: str) -> bool:
        if operation not in ["greater-than", "less-than", "equal", "greater-than-or-equal", "less-than-or-equal"]:
            raise ValueError("Provide one comparison operation of the following three: 'greater-than', 'less-than', 'equal', 'greater-than-or-equal', 'less-than-or-equal'")
        if self.get_type() == other.get_type():
            return self._perform_comparison_between_equal_type_combinations(other, operation)
        else:
            if operation in ["greater-than", "greater-than-or-equal"]:
                return self.get_priority_of_combination() > other.get_priority_of_combination()
            elif operation in ["less-than", "less-than-or-equal"]:
                return self.possible_combinations.index(self.get_type()) > other.possible_combinations.index(other.get_type())
            elif operation == "equal":
                raise RuntimeError("The program should not get this deep if looking for equality operation.")

    def _perform_comparison_between_equal_type_combinations(self, other: Self, operation: str) -> bool:
        cards_in_own_combination = sorted([card for card in self.cards], key=lambda card: card.get_numerical_value())
        cards_in_other_combination = sorted([card for card in other.cards], key=lambda card: card.get_numerical_value())
        for own_card, other_card in zip(cards_in_own_combination, cards_in_other_combination):
            if own_card.get_numerical_value() > other_card.get_numerical_value():
                return operation in ["greater-than", "greater-than-or-equal"]
            elif own_card.get_numerical_value() < other_card.get_numerical_value():
                return operation in ["less-than", "less-than-or-equal"]
        return operation in ["equal", "greater-than-or-equal", "less-than-or-equal"]
    
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
        else: return self.cards[index].get_rank()

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
