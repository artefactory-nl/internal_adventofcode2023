from objects.day_seven.base_combination import BaseCombination

class Combination(BaseCombination):  
    def get_type(self) -> str:
        cards_in_combination = sorted([card for card in self.cards], key=lambda card: card.get_numerical_value())
        ranks_in_combination = [card.get_rank() for card in cards_in_combination]
        ## SPECIAL CASE ONLY IF CARD IS J ##
        card_rank = ranks_in_combination[0]
        if card_rank == "J": # will always be first value:
            if ranks_in_combination.count(card_rank) in [4, 5]: 
                return "five-of-a-kind"
            elif ranks_in_combination.count(card_rank) == 3:
                if (len(dict.fromkeys(ranks_in_combination[3:])) == 1) and (len(cards_in_combination) == 5):
                    return "five-of-a-kind"
                else:
                    return "four-of-a-kind"
            elif ranks_in_combination.count(card_rank) == 2:
                if (len(dict.fromkeys(ranks_in_combination[2:])) == 1) and (len(cards_in_combination) == 5):
                    return "five-of-a-kind"
                for card_rank_left in dict.fromkeys(ranks_in_combination[2:]):
                    if ranks_in_combination.count(card_rank_left) == 2:
                        return "four-of-a-kind"
                else: return "three-of-a-kind"
            elif ranks_in_combination.count(card_rank) == 1:
                if (len(dict.fromkeys(ranks_in_combination[1:])) == 1):
                    if (len(cards_in_combination) == 5):
                        return "five-of-a-kind"
                    elif (len(cards_in_combination) == 4):
                        return "four-of-a-kind"
                for card_rank_left in dict.fromkeys(ranks_in_combination[1:]):
                    if ranks_in_combination.count(card_rank_left) == 3:
                        return "four-of-a-kind"
                full_house_flag = False
                for card_rank_left in dict.fromkeys(ranks_in_combination[1:]):
                    if ranks_in_combination.count(card_rank_left) == 2:
                        if full_house_flag:
                            return "full-house"
                        full_house_flag = True
                return "one-pair" if not full_house_flag else "three-of-a-kind"
            else:
                raise RuntimeError("No combination type found.")

        ## BASE CASE -> NO JOKERS, CALL SUPER ##
        else:
            return super().get_type()
