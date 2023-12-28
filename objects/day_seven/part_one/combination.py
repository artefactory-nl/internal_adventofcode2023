from typing import Self
from objects.day_seven.base_combination import BaseCombination


class Combination(BaseCombination):  
    def get_type(self) -> str:
        ranks_in_combination = sorted([card.get_rank() for card in self.cards])
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
            cards_in_own_combination = [card for card in self.cards]
            sorted_ranks_in_own_combination = sorted(cards_in_own_combination, key=lambda r: self.cards[0].possible_ranks.index(r.get_rank()))
            cards_in_other_combination = [card for card in other.cards]
            sorted_cards_in_other_combination = sorted(cards_in_other_combination, key=lambda r: self.cards[0].possible_ranks.index(r.get_rank()))
            for card_pos in range(len(cards_in_own_combination)):
                if sorted_ranks_in_own_combination[card_pos].get_numerical_value() > sorted_cards_in_other_combination[card_pos].get_numerical_value():
                    return operation in ["greater-than", "greater-than-or-equal"]
                elif sorted_ranks_in_own_combination[card_pos].get_numerical_value() < sorted_cards_in_other_combination[card_pos].get_numerical_value():
                    return operation in ["less-than", "less-than-or-equal"]
                else: continue
            return operation in ["equal", "greater-than-or-equal", "less-than-or-equal"]
        elif operation in ["greater-than", "greater-than-or-equal"]:
            return self.get_priority_of_combination() > other.get_priority_of_combination()
        elif operation in ["less-than", "less-than-or-equal"]:
            return self.possible_combinations.index(self.get_type()) > other.possible_combinations.index(other.get_type())
        elif operation == "equal":
            raise RuntimeError("The program should not get this deep if looking for equality operation.")

