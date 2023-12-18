import re
import numpy as np

def return_numbers_adjacent_to_symbol(input_lines: list[str]) -> int:
    number_lines = len(input_lines)
    line_length = len(input_lines[0])
    number_matches_spans = [(ix, c.span()) for ix, line in enumerate(input_lines) for c in re.finditer("\d+", line)]
    valid_numbers = []

    for row_n, (beg_ix, end_ix) in number_matches_spans:
        symbols_regex = f"[^\.0-9]"
        number_to_evaluate = int(input_lines[row_n][beg_ix:end_ix])

        # Condition number 1: no symbols adjacent in line
        cond_number_1 = bool(
            re.search(symbols_regex, input_lines[row_n][max(beg_ix-1, 0):min(end_ix+1, line_length)])
            )

        # Condition number 2: no symbols adjacent in line above
        cond_number_2 = bool(
            re.search(symbols_regex, input_lines[row_n-1][max(beg_ix-1, 0):min(end_ix+1, line_length)])
            ) if row_n > 0 else False

        # Condition number 3: no symbols adjacent in line below
        cond_number_3 = bool(
            re.search(symbols_regex, input_lines[row_n+1][max(beg_ix-1, 0):min(end_ix+1, line_length)])
            ) if row_n < (number_lines - 1) else False

        if any([cond_number_1, cond_number_2, cond_number_3]):
            valid_numbers.append(number_to_evaluate)
    return valid_numbers

input_file = open("inputs/day1/problem-3.txt")
input_lines = input_file.read().splitlines()

answer = sum(return_numbers_adjacent_to_symbol(input_lines))

print(answer)