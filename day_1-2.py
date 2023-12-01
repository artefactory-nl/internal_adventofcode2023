from utils import read_input

file_name = __file__.split("/")[-1].replace(".py", "")
exercise_number = file_name.split("_")[1]

digits = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9
}

def is_number_spelled(word):
    for digit, _ in digits.items():
        if digit in word :
            return True
        
def get_number_spelled(word):
    for digit, number in digits.items():
        if digit in word:
            return number

def get_first_digit(line):
    word = ""
    for char in line:
        if char.isdigit():
            return int(char)
        elif char.isalpha():
            word = word + char

        if is_number_spelled(word):
            return get_number_spelled(word)

def get_last_digit(line):
    word = ""
    for char in reversed(line):
        if char.isdigit():
            return int(char) 
        elif char.isalpha():
            word = char + word
            
        if is_number_spelled(word):
            return get_number_spelled(word)
            


input, example = read_input(exercise_number)

def solve(input):
    tot = 0

    for line in input.split("\n"):
        first_digit = get_first_digit(line)
        last_digit = get_last_digit(line)
        combined = int(str(first_digit) + str(last_digit))
        tot += combined
        
    return tot

print("For the example we get:")
print(solve(example))

print("For the solution answer we get:")
print(solve(input))
