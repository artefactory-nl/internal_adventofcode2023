import re

def extract_calibration_value(text_string: str) -> int:
    first_digit = re.findall("\d{1}", text_string)[0]
    last_digit = re.findall("\d{1}", text_string)[-1]

    # Compose a number by concatenating the 2 digits
    return int(first_digit + last_digit)

input_file = open("inputs/day1/problem-1.txt")
input_lines = input_file.read().splitlines()

answer = sum([extract_calibration_value(line) for line in input_lines])

print(answer)
