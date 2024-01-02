from dataclasses import dataclass, field
from functools import total_ordering
from objects.day_seven.base_combination import BaseCombination as Combination
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
