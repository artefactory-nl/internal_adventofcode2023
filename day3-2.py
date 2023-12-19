import re
import numpy as np

def aux_find_part_numbers_in_adjacent_line(input_line: str, gear_location: int) -> list[str]:
    right_slice_including_gear_location = input_line[gear_location:]
    left_slice_excluding_gear_location = input_line[:gear_location][::-1]
    
    right_find_part_number_regex = "^([^0-9]{0,1})(\d*)"
    left_find_part_number_regex = "^(\d*)"

    right_lookahead_part_number = re.search(right_find_part_number_regex, right_slice_including_gear_location).group()
    left_lookeahead_part_number = re.search(left_find_part_number_regex, left_slice_excluding_gear_location).group(1)[::-1]

    # CONSIDER right and left number might be the same number -> concatenate strings and split on non-number
    part_number_list = re.split(r"\D", left_lookeahead_part_number + right_lookahead_part_number)
    return [part_number for part_number in part_number_list if part_number] # exclude empty strings

def return_gear_ratios(input_lines: list[str]) -> int:
    number_lines = len(input_lines)
    gear_regex = "(\d*)(\*)(\d*)"

    gear_matches_found = [
        (row_number, gear_match) 
        for row_number, line in enumerate(input_lines) for gear_match in re.finditer(gear_regex, line)]

    gear_ratios = []
    
    for row_number, gear_match in gear_matches_found:
        part_numbers_adjacent_to_gear = []
        # First check: are there part numbers left and right?
        for match_group in [gear_match.group(1), gear_match.group(3)]:
            if bool(match_group): 
                part_numbers_adjacent_to_gear.append(match_group)
        
        # Save index where gear has been found
        gear_location, _ = gear_match.span(2)
        
        # Second check: part numbers in the line above?
        if row_number != 0:
            part_numbers_adjacent_to_gear.extend(
                aux_find_part_numbers_in_adjacent_line(input_line=input_lines[row_number-1], gear_location=gear_location)
            )
        
        # Third check: part numbers in the line above?
        if row_number < (number_lines - 1):
            part_numbers_adjacent_to_gear.extend(
                aux_find_part_numbers_in_adjacent_line(input_line=input_lines[row_number+1], gear_location=gear_location)
            )
        
        if len(part_numbers_adjacent_to_gear) == 2:
            gear_ratios.append(int(part_numbers_adjacent_to_gear[0]) * int(part_numbers_adjacent_to_gear[1]))
    
    return gear_ratios

input_file = open("inputs/problem-3.txt")
input_lines = input_file.read().splitlines()

answer = sum(return_gear_ratios(input_lines))

print(answer)