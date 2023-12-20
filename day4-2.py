import re

def calculate_total_number_scratchcards(input_lines: list[str]) -> list[int]:
    card_regex = r"Card +(\d+): +([0-9 ]+)\|([0-9 ]+)"
    split_card_nums_string = lambda card_nums: list(map(int, re.split(" +", card_nums)))
    card_components_matches = [re.search(card_regex, line) for line in input_lines]
    scratchcards_dict = {
        int(match.group(1)): {
            "winning_numbers": split_card_nums_string(match.group(2).strip()),
            "player_numbers":  split_card_nums_string(match.group(3).strip()),
        } for match in card_components_matches}
    
    def recursive_auxiliary_func(card, card_num, scratchcards_dict):
        if card == 0: return 0 # base case 1
        amount_of_winning_numbers = len(
            [number for number in card["player_numbers"] if number in card["winning_numbers"]])
        if amount_of_winning_numbers == 0:
            return 1 # base case 2
        else:
            return 1 + sum(
                [
                    recursive_auxiliary_func(scratchcards_dict.get(card_ix, 0), card_ix, scratchcards_dict)
                    for card_ix in range(card_num+1, card_num+amount_of_winning_numbers+1)]
            )
    
    return [recursive_auxiliary_func(card, card_num, scratchcards_dict) for card_num, card in scratchcards_dict.items()]

input_file = open("inputs/problem-4.txt")

input_lines = input_file.read().splitlines()

answer = sum(calculate_total_number_scratchcards(input_lines))

print(answer)