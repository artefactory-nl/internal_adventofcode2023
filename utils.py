def read_input(exercise):
    day, part = exercise.split("-")
    with open(f'input/day_{day}.txt', 'r') as file:
        input = file.read()
    with open(f'input/day_{day}-{part}_example.txt', 'r') as file:
        example = file.read()
        
    return input, example
