from itertools import cycle


def parse_instructions_and_map(lines: str) -> tuple[str, dict[str, dict[str, str]]]:
    instructions = [*lines[0]]
    alphanumerical_map = dict()
    for direction in lines[2:]:
        map_key, map_values = direction.split(" = ")
        left_val, right_val = map_values.strip("()").split(", ")
        alphanumerical_map[map_key] = {"L": left_val, "R": right_val}
    return instructions, alphanumerical_map

def calculate_steps_to_reach_zzz(instructions, alphanumerical_map):
    count_steps = 0
    search_key = "AAA"
    for step in cycle(instructions):
        if alphanumerical_map[search_key][step] != "ZZZ":
            search_key = alphanumerical_map[search_key][step]
            count_steps+=1
        else:
            return count_steps + 1


# input_file = open("inputs/example-input-8-2.txt")
input_file = open("inputs/problem-8.txt")

input_lines = input_file.read().splitlines()

instructions, alphanumerical_map = parse_instructions_and_map(input_lines)

answer = calculate_steps_to_reach_zzz(instructions, alphanumerical_map)

print(answer)