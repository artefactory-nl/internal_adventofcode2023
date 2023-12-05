from utils import read_input


def is_int(char: str) -> bool: 
    try:
        int(char)
        return True
    except ValueError:
        return False

def solve(lines: list[str]) -> int:
    total_sum = 0
    for line in lines:
        line_length = len(line)
        first_discovered = False
        last_discovered = False
        for index in range(line_length):
            left_char = line[index]
            right_char = line[line_length - index - 1]
            if not first_discovered:
                if is_int(left_char):
                    first_number = int(left_char)
                    first_discovered = True
            if not last_discovered:
                if is_int(right_char):
                    last_number = int(right_char)
                    last_discovered = True
            if first_discovered and last_discovered:
                total_sum += int(str(first_number) + str(last_number))
                break
    return total_sum

if __name__ == '__main__':
    lines = read_input('input_day_1.txt')
    print(solve(lines))