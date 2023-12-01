from utils import read_input

file_name = __file__.split("/")[-1].replace(".py", "")
exercise_number = file_name.split("_")[1]

def get_first_digit(line):
    for char in line:
        if char.isdigit():
            return int(char)

def get_last_digit(line):
    for char in reversed(line):
        if char.isdigit():
            return int(char) 

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