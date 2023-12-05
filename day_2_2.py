from day_2_1 import extract_samplings
from utils import read_input


def solve(games: list[str]) -> int:
    total_sum = 0
    for game in games:
        samplings = extract_samplings(game)
        min_dict = {
            "red": 0,
            "green": 0,
            "blue": 0,
        }
        for sampling in samplings:
            elements = sampling.split(" ")[1:]
            numbers = [int(number) for number in elements[::2]]
            colors = elements[1::2]
            for color, number in zip(colors, numbers):
                if number > min_dict[color]:
                    min_dict[color] = number
        total_sum += min_dict["red"] * min_dict["green"] * min_dict["blue"]
    return total_sum

if __name__ == '__main__':
    games = read_input('input_day_2.txt')
    print(solve(games))