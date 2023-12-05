import re

from utils import read_input


POSSIBLE_GAMES_SCHEMA = {
    "red": 12,
    "green": 13,
    "blue": 14,
}

def extract_samplings(game: str) -> list[str]:
    game = game.split(":")[1]
    game = game.replace(",", "")
    return game.split(";")

def extract_game_id(game: str) -> int:
    descriptive_elt = game.split(":")[0]
    return int(re.findall(r"\d+", descriptive_elt)[0])

def check_sampling_feasible(sampling_schema: dict[str, int]) -> bool:
    for color, number in sampling_schema.items():
        if number > POSSIBLE_GAMES_SCHEMA[color]:
            return False
    return True

def solve(games: list[str]) -> int:
    total_sum = 0
    for game in games:
        game_id = extract_game_id(game)
        samplings = extract_samplings(game)
        feasibility = True
        for sampling in samplings:
            elements = sampling.split(" ")[1:]
            numbers = [int(number) for number in elements[::2]]
            colors = elements[1::2]
            feasibility = check_sampling_feasible(dict(zip(colors, numbers)))
            if not feasibility:
                feasibility = False
                break
        if feasibility:
            total_sum += game_id
    return total_sum
        

if __name__ == '__main__':
    games = read_input('input_day_2.txt')
    print(solve(games))
