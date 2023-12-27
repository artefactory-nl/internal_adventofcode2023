import re
from typing import Mapping

def process_seeds(raw_seeds: str) -> Mapping[str, int]:
    extract_seeds_regex = r"seeds: (.+)"
    seeds = map(int, re.search(extract_seeds_regex, raw_seeds).group(1).split(" "))
    return seeds

def find_seed_location(seed: int, clean_maps: dict[str, list[tuple[int]]]) -> int:
    mappings = clean_maps.keys()
    seed_location = seed
    for mapping in mappings:
        for destination_start, source_start, max_range in clean_maps[mapping]:
            if seed_location in range(source_start, source_start+max_range):
                seed_location = (seed_location - source_start) + destination_start
                break
    return seed_location


def process_mappings(text_lines: list[str]) -> dict[str, list[tuple[int]]]:
    replace_separator_input = [string_info if string_info else "/" for string_info in text_lines]
    raw_mappings = "__".join(replace_separator_input).split("/")
    raw_mappings = [raw_map.strip("_ ") for raw_map in raw_mappings]
    processed_mappings = {
        raw_mapping.split("__")[0]: [
            tuple(map(int, custom_range.split())) for custom_range in raw_mapping.split("__")[1:]]
        for raw_mapping in raw_mappings
    }
    return processed_mappings

input_file = open("inputs/problem-5.txt")

input_lines = input_file.read().splitlines()

seeds = process_seeds(raw_seeds=input_lines[0])
mappings = process_mappings(text_lines=input_lines[2:])
 
answer = min([find_seed_location(seed, mappings) for seed in seeds])

print(answer)