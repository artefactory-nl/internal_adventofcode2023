import re

def return_game_number_or_zero(text_string: str) -> int:
    bag_cubes = {"red": 12, "green": 13, "blue": 14}
    game_number = text_string.split(": ")[0][5:]
    game_individual_scores = text_string.split(": ")[1].split("; ")
    colors = bag_cubes.keys()
    number_of_colored_balls_in_game = fr"(\d+) ({'|'.join(colors)})"

    for game in game_individual_scores:
        game_score_per_ball_color = re.findall(number_of_colored_balls_in_game, game)
        for number_of_balls, ball_color in game_score_per_ball_color:
            if bag_cubes[ball_color] < int(number_of_balls):
                return 0
            else:
                continue
        
    return int(game_number)

input_file = open("inputs/day1/problem-2.txt")
input_lines = input_file.read().splitlines()

answer = sum([return_game_number_or_zero(line) for line in input_lines])

print(answer)