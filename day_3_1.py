import re

from utils import read_input


def extract_symbols(lines: list[str]) -> list[str]:
    """Returns a list of symbols that are in the grid.
    
    Symbols are characters that are not numbers or dots.
    """
    symbols = []
    for line in lines:
        for char in line:
            if char not in symbols and not char.isdigit() and char != ".":
                symbols.append(char)
    return symbols

def find_numbers_positions(lines: list[str]) -> list[dict[str, list[tuple[int, int]]]]:
    """Returns a list of dictionaries containing the positions of each digit that composes the number.
    
    Each dictionary contains the string number as key, and as value a list of tuples containing the coordinates of each digit.
    """
    positions = []
    for line_index, line in enumerate(lines):
        digits_in_line = re.finditer(r"\d+", line)
        for match in digits_in_line:
            positions.append({str(match.group()): [(line_index, i) for i in range(match.start(), match.end())]})
    return positions

def extract_possible_coordinates(coordinates: tuple[int, int], max_x: int, max_y: int) -> list[tuple[int, int]]:
    """Returns a list of coordinates that are around the given coordinates.
    
    The coordinates are extracted from a grid of size max_x * max_y.
    """
    x, y = coordinates
    possible_coordinates = []
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if (i, j) != (0, 0):
                if x + i >= 0 and y + j >= 0 and x + i < max_x and y + j < max_y:
                    possible_coordinates.append((x + i, y + j))
    return possible_coordinates

def extract_around_positions(positions: list[dict[str, list[tuple[int, int]]]], max_x: int, max_y: int) -> list[dict[str, list[tuple[int, int]]]]:
    """Returns a list of dictionaries, each dictionary contains the positions around a number in the grid."""
    positions_to_check = []
    for position in positions:
        for number, positions_list in position.items():
            around_positions = {
                number: []
            }
            for coordinates in positions_list:
                possible_around_coordinates = extract_possible_coordinates(coordinates, max_x=max_x, max_y=max_y)
                possible_around_coordinates = [coord for coord in possible_around_coordinates if coord not in positions_list]
                around_positions[number].extend(possible_around_coordinates)
            positions_to_check.append(around_positions)
    return positions_to_check

def solve(lines: list[str]) -> int:
    total_sum = 0
    symbols = extract_symbols(lines)
    positions = find_numbers_positions(lines)
    around_positions = extract_around_positions(positions, max_x=len(lines), max_y=len(lines[0]))
    for around_position in around_positions:
        for number, coords_to_check in around_position.items():
            for coordinates in coords_to_check:
                x, y = coordinates
                if lines[x][y] in symbols:
                    total_sum += int(number)
                    break
    return total_sum

if __name__ == '__main__':
    lines = read_input('input_day_3.txt')
    print(solve(lines))