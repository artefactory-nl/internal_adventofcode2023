import regex as re

from day_1_1 import solve
from utils import read_input


DIGIT_MAPPING = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9"
}


def apply_digit_mapping(lines: list[str], mapping: dict[str, str]) -> list[str]:
    for line_index in range(len(lines)):
        line = lines[line_index]
        matches = [match for match in re.finditer(f"({'|'.join(mapping.keys())})", line, overlapped=True)]
        if matches:
            if len(matches) == 1:
                line = line.replace(matches[0].group(), mapping[matches[0].group()])
            else:
                first_match = matches[0]
                last_match = matches[-1]
                line = line[:first_match.start()] + mapping[first_match.group()] + line[first_match.start():]
                line = line[:last_match.end() + 1] + mapping[last_match.group()] + line[last_match.end() + 1:]
        lines[line_index] = line
    return lines


if __name__ == "__main__":
    lines = read_input('input_day_1.txt')
    lines = apply_digit_mapping(lines, DIGIT_MAPPING)
    print(solve(lines))
