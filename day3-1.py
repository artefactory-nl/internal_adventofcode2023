import re
import numpy as np

def return_part_numbers(input_lines: list[str]) -> int:
    number_lines = len(input_lines)
    line_length = len(input_lines[0])
    number_matches_spans = [
        (row_number, number_match.span()) 
        for row_number, line in enumerate(input_lines) for number_match in re.finditer("\d+", line)
    ]
    part_numbers = []

    for row_number, (beg_ix, end_ix) in number_matches_spans:
        symbols_regex = f"[^\.0-9]"
        number_to_evaluate = int(input_lines[row_number][beg_ix:end_ix])

        # Condition number 1: no symbols adjacent in line
        cond_number_1 = bool(
            re.search(symbols_regex, input_lines[row_number][max(beg_ix-1, 0):min(end_ix+1, line_length)])
            )

        # Condition number 2: no symbols adjacent in line above
        cond_number_2 = bool(
            re.search(symbols_regex, input_lines[row_number-1][max(beg_ix-1, 0):min(end_ix+1, line_length)])
            ) if row_number > 0 else False

        # Condition number 3: no symbols adjacent in line below
        cond_number_3 = bool(
            re.search(symbols_regex, input_lines[row_number+1][max(beg_ix-1, 0):min(end_ix+1, line_length)])
            ) if row_number < (number_lines - 1) else False

        if any([cond_number_1, cond_number_2, cond_number_3]):
            part_numbers.append(number_to_evaluate)
    return part_numbers

input_file = open("inputs/problem-3.txt")
input_lines = input_file.read().splitlines()

answer = sum(return_part_numbers(input_lines))

print(answer)