import re

def number_of_ways_to_beat_record(total_race_time: int, record_distance: int) -> int:
    lowest_button_ms_to_beat_record, highest_way_to_beat_record = None, None
    
    for num_of_ms in range(total_race_time + 1):
        travelled_mm = (total_race_time - num_of_ms) * num_of_ms # speed = num_of_ms
        if travelled_mm > record_distance: lowest_button_ms_to_beat_record=num_of_ms; break
    
    for num_of_ms in range(total_race_time + 1)[::-1]:
        travelled_mm = (total_race_time - num_of_ms) * num_of_ms # speed = num_of_ms
        if travelled_mm > record_distance: highest_way_to_beat_record=num_of_ms; break

    return (highest_way_to_beat_record+1) - lowest_button_ms_to_beat_record


input_file = open("inputs/problem-6.txt")
input_lines = input_file.read().splitlines()

total_race_time = int(re.split(r"Time: +", input_lines[0])[1].replace(" ", ""))
record_distance = int(re.split(r"Distance: +", input_lines[1])[1].replace(" ", ""))

answer = number_of_ways_to_beat_record(total_race_time, record_distance)
print(answer)