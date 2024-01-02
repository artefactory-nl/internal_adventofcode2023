from dataclasses import field
from objects.day_seven.base_card import BaseCard


class Card(BaseCard):
    possible_ranks: list[str] = field(
        init=False,
        default_factory=lambda: ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"])

    def __post_init__(self):
        super().__post_init__()
        if self.rank not in self.possible_ranks.default_factory():
            raise ValueError("Provided card value does not exist in a poker deck.")

    def get_numerical_value(self) -> int:
        return len(self.possible_ranks.default_factory()) - (self.possible_ranks.default_factory().index(self.rank))
