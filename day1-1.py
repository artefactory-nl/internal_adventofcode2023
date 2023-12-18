import re

def extract_calibration_value(text_string: str) -> int:
    return int(re.findall("\d{1}", text_string)[0] + re.findall("\d{1}", text_string)[-1])

input_file = open("inputs/day1/problem-1.txt")
input_lines = input_file.read().splitlines()

answer = sum([extract_calibration_value(line) for line in input_lines])

print(answer)
