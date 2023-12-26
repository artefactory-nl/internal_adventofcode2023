"""ASSUMPTIONS:

1. Negative source values will never be provided in seed or mapping intervals.
2. Mapping keys such as "fertilizer-to-water" contain a list of mappings for certain number intervals.
    
    These intervals will be consecutive. If w is the minimum source value in the mappings provided
    for the mapping key, and z is the maximum source value, any int number between w and z will
    be possibly mapped with the mappings provided for the conversion ("fertilizer-to-water"),
    without need of resorting to the alternative default case. 

    (alternative default case: if number is not in the intervals provided by the mappings, the 
    destination number will be the same than the source one)
"""


import re

def intersection_of_intervals(a_lower: int, a_upper: int, b_lower: int, b_upper: int) -> tuple[int]:
    """Return the intersection of two intervals expressed as lower and upper boundaries.
    
    Given two intervals:
    - a = [a_lower, a_upper]
    - b = [b_lower, b_upper]

    We define the intersection c = a ∩ b doing the following:

    if ((b_lower > a_upper) or (a_lower > b_upper)) 
    → then return ∅ (expressed as None, None, since we are returning lower and upper boundaries of interval)
    else {
        c_lower = max(a_lower, b_lower)
        c_upper = min(a_upper, b_upper)
        return [c_lower, c_upper]
    }

    (source: https://scicomp.stackexchange.com/a/26260)

    Args:
        a_lower: int. Lower boundary of interval a.
        a_upper: int. Upper boundary of interval a.
        b_lower: int. Lower boundary of interval b.
        b_upper: int. Upper boundary of interval b.
    
    Returns:
        Lower boundary of intersection a ∩ b.
        Upper boundary of intersection a ∩ b.
    """
    if ((b_lower > a_upper) or (a_lower > b_upper)):
        return None, None
    else:
        lower = max([a_lower, b_lower])
        upper = min([a_upper, b_upper])
        return lower, upper

def process_seeds(raw_seeds: str) -> list[tuple[int]]:
    """Process string of unprocessed seeds into the actionable seed ranges we need to search for solutions.
    
    The returned item will be a list of tuples, where the second item always will be higher than the first one.
    Each tuple will represent a range of seeds that can be explored.

    Args:
        raw_seeds: str. String that contains the raw seed numbers (starting values and max range).
    
    Returns:
        List of tuples, where each tuple is a seed range and both boundaries are inclusive.
    """
    extract_seeds_regex = r"seeds: (.+)"
    pre_clean_seeds = list(map(int, re.search(extract_seeds_regex, raw_seeds).group(1).split(" ")))
    # Start -> even indexes in list (0, 2, 4...); Ranges -> odd indexes in list (1, 3, 5...)
    processed_seeds_start, processed_seeds_range = pre_clean_seeds[::2], pre_clean_seeds[1::2]
    processed_seeds = [(startval, startval+rangeval-1) for startval, rangeval in zip(processed_seeds_start, processed_seeds_range)]
    return processed_seeds

def process_mappings(text_lines: list[str]) -> dict[str, list[tuple[int]]]:
    """Process raw text mappings into dictionary with keys and values.
    
    The input produced has a key that is a description of the conversion, and as a value, a list of tuples.
    Each tuple has 3 items as described in the description of the problem:
    - First value is is the lowest value in the mapping that can be produced as a destination.
    - Second value is the lowest value in the mapping that can be passed as a source.
    - Third value is the size of the interval of the mapping: how many additional consecutively higher values can be passed starting from the second value.

    Values are list that contain mappings (each mapping is represented as the tuple described above).

    Args:
        text_lines: list of strings. Contains the raw data for mappings.
    
    Returns:
        A dictionary with keys as descriptor of conversions and values as list of mappings (represented as tuples)
    """
    replace_separator_input = [string_info if string_info else "/" for string_info in text_lines]
    raw_mappings = "__".join(replace_separator_input).split("/")
    raw_mappings = [raw_map.strip("_ ") for raw_map in raw_mappings]
    processed_mappings = {
        raw_mapping.split("__")[0]: [
            tuple(map(int, custom_range.split())) for custom_range in raw_mapping.split("__")[1:]]
        for raw_mapping in raw_mappings
    }
    return processed_mappings

def find_min_location_in_seed_range(seed_lower: int, seed_upper: int, mappings: dict[str, tuple[int]]) -> int:
    """Find the minimum location in a given seed range for a given mappings dictionary.
    
    Calls a recursive function defined inside until mappings are exhausted and all 
    conversions from seed to location have been performed.

    Args:
        seed_lower: int. Lower boundary of seed interval.
        seed_higher: int. Higher boundary of seed interval.
        mappings: dict. Mappings to perform conversions.

    Returns:
        the minimum location that can be found for the given seed range.
    """
    
    def aux_recursive_find_min_location(source_values_space: list[tuple[int]], mappings: dict[str, list[tuple[int]]], mapping_keys: list[str]) -> int:
        """Recursive function to find the minimum location given a list of intervals.

        We denote an interval as a tuple such as: interval = (interval_lower, interval_upper) (range objects are not used)
        
        The original input is a seed interval. The seed interval is then converted numerous time using the mappings provided
        in the input. During each conversion, it is possible that an interval is split into different slices.
        This is due to the input interval being forced to using different mapping keys depending on the section.
        Eventually, the base case will be reached and a list of intervals that are all the possible location values that
        the original seed interval can take on. We select the minimum lower boundary of these intervals, that is, the
        lowest value that can come up of that seed interval.

        Recursive steps occur by shortening the length of mapping_keys by 1 (the item at the beginning of the list). Which
        means, we move ahead in the conversion pipeline. Reaching the base case means reaching the point where the only
        remaining conversion in mapping_keys is "humidity-to-location".

        Args:
            source_values_space: list of intervals. Values that will be converted into the next mapping conversion
            (e.g. intervals for "fertilizer" that are converted using the "fertilizer-to-water" list of mappings.)
            mappings: dict. Mappings to perform conversions.
            mapping_keys: list of strings. Conversions left to complete the conversion of the seed interval.
        
        Returns:
            Recursive case: function call using as arguments new list of converted values and shortened mapping keys list
            Base case: The minimum location value that can be found for a list of source value intervals 
            (which have been generated after successive recursive calls coming from the original 
            seed interval)
        """
        # Crop the mapping dictionary to current searching stage
        # E.g. if "fertilizer to water" is the first mapping_key
        # → then select it as first item and select the following in the order they had originally
        # → but ommit the keys that precede "fertilizer to water"
        mapping_values = mappings[mapping_keys[0]]

        # Define, in this step, what ranges of values are determined to be equivalent to the input `source_values_space`
        current_step_destination_values_space = []
        
        # Iterate over all potential candidates in `source_values_space`
        for target_source_lower, target_source_upper in source_values_space:
            
            # Define in step what intervals of the target source value have continuity in the mapping tuples of the current mapping key
            target_extend_destination_space = []
            target_extend_source_space = []
            
            # Iterate over mappings
            for destination_lower, source_lower, max_range in mapping_values:
                source_upper = source_lower + max_range - 1
                
                # Calculate intersection between seed interval and mapping source interval
                intersect_lower, intersect_upper = intersection_of_intervals(source_lower, source_upper, target_source_lower, target_source_upper)
                
                # Perform if intersection has been found
                if all([intersect_lower!=None, intersect_upper!=None]):
                    transformed_lower = destination_lower + (intersect_lower - source_lower)
                    transformed_upper = destination_lower + (intersect_upper - source_lower)
                    
                    # Append to source values list the source values that have intersection 
                    target_extend_source_space.append((intersect_lower, intersect_upper))

                    # Append to destination values list the destination values that have intersection 
                    target_extend_destination_space.append((transformed_lower, transformed_upper))
            
            # If there have been no matches at all for the given seed → mapping key returns as equivalent destination the same value than source
            # Thus, we append all values to the the destination values space and go on with the next seed
            if len(target_extend_destination_space) == 0:
                current_step_destination_values_space.append((target_source_lower, target_source_upper))
                continue

            # We also account for seed values that precede the interval, but haven't been mapped (last resort scenario)
            # Same with values that are placed next to the interval, but haven't been mapped (last resort scenario)
            
            min_lower_stored = min(target_extend_source_space, key=lambda t: t[0])[0]
            max_upper_stored = max(target_extend_source_space, key=lambda t: t[1])[1]

            if min_lower_stored > target_source_lower:
                target_extend_destination_space = [(target_source_lower, min_lower_stored-1)] + target_extend_destination_space
            
            if max_upper_stored < target_source_upper:
                target_extend_destination_space.append((max_upper_stored+1, target_source_upper))
        
            # Append all retrieved destination intervals to our current step search space
            current_step_destination_values_space.extend(target_extend_destination_space)
        
        if len(mapping_keys) == 1:
            # BASE CASE → we are iterating over our last mapping key -> then we return the minimum destination value
            # (destination value is first value in tuple, explicitly specified)
            return min(current_step_destination_values_space, key=lambda mapping: mapping[0])[0]
        
        # RECURSIVE CASE → Repeat the recursive step, using retrieved target destination values pool
        # We exclude the first item of mapping keys so we can effectively move to the next conversion mappings
        # By cropping mapping_keys, eventually we will reach the base case (only one mapping key in list)
        return aux_recursive_find_min_location(current_step_destination_values_space, mappings, mapping_keys[1:])
    
    mapping_keys = list(mappings.keys())
    initial_space = [(seed_lower, seed_upper)]
    return aux_recursive_find_min_location(initial_space, mappings, mapping_keys)
    
input_file = open("inputs/problem-5.txt")

input_lines = input_file.read().splitlines()

seeds = process_seeds(raw_seeds=input_lines[0])
mappings = process_mappings(text_lines=input_lines[2:])

answer = min([find_min_location_in_seed_range(seed_lower, seed_upper, mappings) for seed_lower, seed_upper in seeds])
print(answer)