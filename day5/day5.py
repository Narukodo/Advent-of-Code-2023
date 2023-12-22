def format_mapping(mapping_list):
    return [[int(value) for value in mapping.split()] for mapping in mapping_list]

def parse_input():
    with open('day5/day5_input.txt') as f:
        almanac = list(map(lambda x: x.split('\n'), f.read().split('\n\n')))
        seeds = [int(seed) for seed in almanac[0][0].split()[1:]]
        mappings_by_category = [seeds] + [format_mapping(mapping_list[1:]) for mapping_list in almanac[1:]]
        mappings_with_ranges = [[(seed, seed + seeds[seed_number * 2 + 1]) for seed_number, seed in enumerate(seeds[::2])]] + [[[(mapping[0], mapping[0] + mapping[2] - 1), (mapping[1], mapping[1] + mapping[2] - 1)] for mapping in mapping_list] for mapping_list in mappings_by_category[1:]]
        return mappings_by_category, mappings_with_ranges

def map_value(value, mapping):
    mapping_range = list(filter(lambda ranges: ranges[1] <= value and ranges[1] + ranges[2] >= value, mapping))
    if len(mapping_range) == 0:
        return value
    mapping_range = mapping_range[0]
    return mapping_range[0] + (value - mapping_range[1])

def find_location(seed_number, mappings):
    current_number = seed_number
    for mapping in mappings:
        current_number = map_value(current_number, mapping)
    return current_number

# part 1
def find_lowest_location_number():
    almanac = parse_input()[0]
    seeds = almanac[0]
    mappings = almanac[1:]
    locations = [find_location(seed, mappings) for seed in seeds]
    return min(locations)

print(find_lowest_location_number())

# part 2
def is_overlapping(interval_a, interval_b):
    ax, ay = interval_a
    bx, by = interval_b
    return (bx <= ay and ay <= by) or (bx <= ax and ax <= by) or (ax <= by and by <= ay) or (ax <= bx and bx <= ay)

def intersect(interval_a, interval_b):
    if not is_overlapping(interval_a, interval_b):
        return []
    ax, ay = interval_a
    bx, by = interval_b
    return (max(ax, bx), min(ay, by))

# overlapping intervals should already be intervals contained within interval_a
def separate_overlapping_intervals(interval_a, overlapping_intervals):
    sorted_overlapping_intervals = sorted(overlapping_intervals, key=lambda interval: interval[0])
    separated_intervals = []
    if interval_a[0] < sorted_overlapping_intervals[0][0]:
        separated_intervals.append((interval_a[0], sorted_overlapping_intervals[0][0] - 1))
    if interval_a[1] > sorted_overlapping_intervals[-1][1]:
        separated_intervals.append((sorted_overlapping_intervals[-1][1] + 1, interval_a[1]))
    for index, interval in enumerate(sorted_overlapping_intervals[:-1]):
        separated_intervals.append(interval)
        if interval[1] < sorted_overlapping_intervals[index + 1][0] - 1:
            separated_intervals.append((interval[1] + 1, sorted_overlapping_intervals[index + 1][0] - 1))
    separated_intervals.append(sorted_overlapping_intervals[-1])
    return sorted(separated_intervals)

def get_mapping(interval, mappings):
    mapping = list(filter(lambda mapping: is_overlapping(mapping[1], interval), mappings))
    if len(mapping) == 0:
        return interval
    destination, source = mapping[0]
    return (destination[0] + interval[0] - source[0], destination[0] - source[0] + interval[1])

def combine_continuous_intervals(intervals):
    sorted_intervals = sorted(intervals)
    interval_start = sorted_intervals[0][0]
    interval_end = sorted_intervals[0][1]
    combined_intervals = []
    counter = 1
    num_intervals = len(sorted_intervals)
    while counter <= num_intervals:
        interval_start, interval_end = sorted_intervals[counter - 1]
        while counter < num_intervals and sorted_intervals[counter - 1][1] == sorted_intervals[counter][0] - 1:
            counter += 1
        interval_end = sorted_intervals[counter - 1][1]
        combined_intervals.append((interval_start, interval_end))
        counter += 1
    return combined_intervals

def map_interval(given_source_interval, mappings):
    valid_maps = sorted(list(filter(lambda mapping: is_overlapping(given_source_interval, mapping[1]), mappings)))
    if len(valid_maps) == 0:
        return [given_source_interval]
    intersections = [intersect(given_source_interval, source_interval) for destination_interval, source_interval in valid_maps]
    separated_intervals = separate_overlapping_intervals(given_source_interval, intersections)
    mappings = sorted([get_mapping(interval, valid_maps) for interval in separated_intervals])
    return combine_continuous_intervals(mappings)

def map_all_intervals(given_intervals, mappings):
    sorted_intervals = combine_continuous_intervals(sorted(given_intervals))
    final_intervals = []
    for interval in sorted_intervals:
        final_intervals += map_interval(interval, mappings)
    return final_intervals
    
def find_location(seed_intervals, almanac_mapping):
    mapped_intervals = map_all_intervals(seed_intervals, almanac_mapping[0])
    for mapping in almanac_mapping[1:]:
        mapped_intervals = map_all_intervals(mapped_intervals, mapping)
    return sorted(mapped_intervals)

almanac = parse_input()[1]
print(find_location(almanac[0], almanac[1:])[0][0])