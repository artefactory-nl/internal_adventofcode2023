import re
from itertools import cycle
from math import lcm
from tqdm import tqdm


def parse_instructions_and_map(lines: str) -> tuple[str, dict[str, dict[str, str]]]:
    instructions = [*lines[0]]
    alphanumerical_map = dict()
    for direction in lines[2:]:
        map_key, map_values = direction.split(" = ")
        left_val, right_val = map_values.strip("()").split(", ")
        alphanumerical_map[map_key] = {"L": left_val, "R": right_val}
    return instructions, alphanumerical_map

def calculate_steps_to_reach_zzz(instructions, alphanumerical_map):
    search_keys = [search_key for search_key in alphanumerical_map.keys() if re.search(r"^\w{2}A$", search_key)]
    found_zzz_in_steps = [0] * len(search_keys)
    count_steps = 0
    for step in tqdm(cycle(instructions)):
        for sk_position, search_key in enumerate(search_keys):
            if re.search(r"^\w{2}Z$", alphanumerical_map[search_key][step]):
                found_zzz_in_steps[sk_position] = count_steps + 1
        if all(found_zzz_in_steps):
            return lcm(*found_zzz_in_steps) # Return Least Common Multiple of all starting **A points
        else:
            search_keys = [alphanumerical_map[search_key][step] for search_key in search_keys]
            count_steps += 1


input_file = open("inputs/problem-8.txt")

input_lines = input_file.read().splitlines()

instructions, alphanumerical_map = parse_instructions_and_map(input_lines)
answer = calculate_steps_to_reach_zzz(instructions, alphanumerical_map)

print(answer)