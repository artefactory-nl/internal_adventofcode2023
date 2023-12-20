import re

def calculate_points_in_card(line):
    card_regex = r"(Card +\d+): +([0-9 ]+)\|([0-9 ]+)"
    winning_numbers_str = re.search(card_regex, line).group(2).strip()
    player_numbers_str = re.search(card_regex, line).group(3).strip()
    winning_numbers = re.split(" +", winning_numbers_str)
    player_numbers = re.split(" +", player_numbers_str)
    amount_of_winning_numbers = len([card for card in player_numbers if card in winning_numbers])
    return 2 ** (amount_of_winning_numbers-1) if amount_of_winning_numbers != 0 else 0

input_file = open("inputs/problem-4.txt")

input_lines = input_file.read().splitlines()

answer = sum([calculate_points_in_card(line) for line in input_lines])

print(answer)