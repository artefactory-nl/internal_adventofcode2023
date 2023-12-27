from functools import reduce
from itertools import starmap
import re

def parse_data(lines: list[str]) -> list[tuple[int]]:
    times, distances = (map(int, re.split(r" +", lines[i])[1:]) for i in range(2))
    return [(time, distance) for time, distance in zip(times, distances)]

def number_of_ways_to_beat_record(total_race_time: int, record_distance: int):
    total_number_of_ways = 0
    for num_of_ms in range(total_race_time + 1):
        travelled_mm = (total_race_time - num_of_ms) * num_of_ms # speed = num_of_ms
        if travelled_mm > record_distance: total_number_of_ways+=1
    return total_number_of_ways


input_file = open("inputs/problem-6.txt")
input_lines = input_file.read().splitlines()
parsed_input = parse_data(input_lines)

answer = reduce(lambda a, b: a*b, starmap(number_of_ways_to_beat_record, parsed_input))
print(answer)