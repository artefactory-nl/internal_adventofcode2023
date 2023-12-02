import regex
from utils import read_input

file_name = __file__.split("/")[-1].replace(".py", "")
exercise_number = file_name.split("_")[1]

loaded_colors = (12,13,14)

def extract_color_number(draw, color):
    if color in draw:
        return int(regex.search(f"(\d+)(?=\s*{color})", draw).group())
    else:
        return 0
        
def read_game(line):
    """Not used as it was more optimised to stop 
    reading a game when a color was too high 
    but useful to be able to read an entire game"""
    
    # Remove the Game part
    line = line.replace("Game ", "")
    # Extract the game number
    id = int(line.split(":")[0])
    # Extract the draws
    draws = line.split(": ")[1].split("; ")
    game_result = []
    for draw in draws:            
        r = extract_color_number(draw, "red")
        g = extract_color_number(draw, "green")
        b = extract_color_number(draw, "blue")
        game_result.append((r, g, b))
    return id, game_result      

def read_game_return_valid_id(line):
    """Reads a game and returns the id if it is valid or stop
    reading the game if a color is too high and returns None"""
    # Remove the Game part
    line = line.replace("Game ", "")
    # Extract the game number
    id = int(line.split(":")[0])
    # Extract the draws
    draws = line.split(": ")[1].split("; ")
    for draw in draws:            
        r = extract_color_number(draw, "red")
        if r > loaded_colors[0]:
            return None
        g = extract_color_number(draw, "green")
        if g > loaded_colors[1]:
            return None
        b = extract_color_number(draw, "blue")
        if b > loaded_colors[2]:
            return None
    return id
        
input, example = read_input(exercise_number)


def solve(input):
    games = input.split("\n")
    solution = 0
    for game in games:
        id = read_game_return_valid_id(game)
        solution += id if id is not None else 0
    return solution

print("For the example we get:")
print(solve(example))

print("For the solution answer we get:")
print(solve(input))
