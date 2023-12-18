import re
import numpy as np

def return_product_of_minimum_balls_per_color(text_string: str) -> int:
    bag_cubes = {"red": 0, "green": 0, "blue": 0}
    game_individual_scores = text_string.split(": ")[1].split("; ")
    colors = bag_cubes.keys()
    number_of_colored_balls_in_game = fr"(\d+) ({'|'.join(colors)})"

    for game in game_individual_scores:
        game_score_per_ball_color = re.findall(number_of_colored_balls_in_game, game)
        for number_of_balls, ball_color in game_score_per_ball_color:
            if bag_cubes[ball_color] < int(number_of_balls):
                bag_cubes[ball_color] = int(number_of_balls)
            else:
                continue
        
    return np.prod(list(bag_cubes.values()))

input_file = open("inputs/day1/problem-2.txt")
input_lines = input_file.read().splitlines()

answer = sum([return_product_of_minimum_balls_per_color(line) for line in input_lines])

print(answer)