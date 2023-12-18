import regex

def extract_calibration_value(text_string: str) -> int:
    numbers_to_text = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    numbers_to_text_dict = {word: str(number + 1) for number, word in enumerate(numbers_to_text)}

    regex_string = "\d{1}|" + "|".join(numbers_to_text)

    first_digit = regex.findall(regex_string, text_string, overlapped=True)[0]
    last_digit = regex.findall(regex_string, text_string, overlapped=True)[-1]

    return int(numbers_to_text_dict.get(first_digit, first_digit) + numbers_to_text_dict.get(last_digit, last_digit))

input_file = open("inputs/day1/problem-1.txt")
input_lines = input_file.read().splitlines()

answer = sum([extract_calibration_value(line) for line in input_lines])

print(answer)
