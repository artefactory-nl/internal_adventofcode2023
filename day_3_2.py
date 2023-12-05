from day_3_1 import find_numbers_positions, extract_around_positions, extract_possible_coordinates
from utils import read_input


SYMBOLS = ["*"]


def extract_adjacent_numbers_to_symbols(lines: list[str], around_positions: list[dict[str, list[tuple[int, int]]]]) -> dict[str, list[int]]:
    """Returns a dictionary containing the numbers adjacent to a symbol.
    
    The key is the coordinates of the symbol, and the value is a list of numbers adjacent to the symbol.
    """
    numbers_adjacent_to_symbols = {}
    for around_position in around_positions:
        for number, coords_to_check in around_position.items():
            for coordinates in coords_to_check:
                x, y = coordinates
                if lines[x][y] in SYMBOLS:
                    if str(coordinates) not in numbers_adjacent_to_symbols:
                        numbers_adjacent_to_symbols[str(coordinates)] = []
                    numbers_adjacent_to_symbols[str(coordinates)].append(int(number))
                    break
    return numbers_adjacent_to_symbols

def solve(lines: list[str]) -> int:
    total_sum = 0
    positions = find_numbers_positions(lines)
    around_positions = extract_around_positions(positions, max_x=len(lines), max_y=len(lines[0]))
    numbers_adjacent_to_symbols = extract_adjacent_numbers_to_symbols(lines, around_positions)
    for symbols_coords, adj_numbers_list in numbers_adjacent_to_symbols.items():
        if len(adj_numbers_list) == 2:
            total_sum += adj_numbers_list[0] * adj_numbers_list[1]
    return total_sum

if __name__ == '__main__':
    lines = read_input('input_day_3.txt')
    print(solve(lines))