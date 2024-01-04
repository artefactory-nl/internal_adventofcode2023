def find_next_value_in_sequence(line):
    numbers = [x for x in map(int, line.split(" "))]

    def recursive_search(numbers):
        if len(set(numbers)) == 1:
            return numbers[0]
        
        paired_numbers = [tuple(numbers[ix-1:ix+1]) for ix in range(1, len(numbers))]
        differences_in_paired_numbers = [(high-low) for low, high in paired_numbers]
        return numbers[-1] + recursive_search(differences_in_paired_numbers)
    
    return recursive_search(numbers)


input_file = open("inputs/problem-9.txt")

input_lines = input_file.read().splitlines()

answer = sum(find_next_value_in_sequence(line) for line in input_lines)
print(answer)