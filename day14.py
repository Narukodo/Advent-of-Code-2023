from collections import defaultdict
import pprint

pp = pprint.PrettyPrinter(indent=4)

def parse_input():
    with open('day14_test_input.txt') as f:
        setup = f.read().splitlines()
        round_rocks_dict = defaultdict(lambda: [])
        cube_rocks_dict = defaultdict(lambda: [])
        for y, row in enumerate(setup):
            for x, char in enumerate(row):
                if char == 'O':
                    round_rocks_dict[x].append(y)
                if char == '#':
                    cube_rocks_dict[x].append(y)
        rocks = list(enumerate([(y, x, rock_type) for y, row in enumerate(setup) for x, rock_type in enumerate(row) if rock_type != '.']))
        return round_rocks_dict, cube_rocks_dict, len(setup), len(setup[0]), rocks, setup

def find_closest_cube_rock(round_rock, cube_rocks):
    y, x = round_rock
    max_y = -1
    if x in cube_rocks:
        for cube_y in cube_rocks[x]:
            if cube_y < y and max_y < cube_y:
                max_y = cube_y
    return max_y

def load(round_rock, round_rocks, cube_rocks, num_rows):
    y, x = round_rock
    closest_cube_rock = find_closest_cube_rock(round_rock, cube_rocks)
    offset = 0
    if x in round_rocks:
        for round_y in round_rocks[x]:
            if round_y < y and round_y > closest_cube_rock:
                offset += 1
    final_rock_index = closest_cube_rock + offset + 1
    return num_rows - final_rock_index

def count_load():
    round_rocks, cube_rocks, num_rows, width, rocks = parse_input()
    final_load = 0
    for x in round_rocks:
        for y in round_rocks[x]:
            final_load += load((y, x), round_rocks, cube_rocks, num_rows)
    return final_load

# print(count_load())

def find_closest_cube_rock(direction, rock_coordinates, rocks, length, width):
    y, x = rock_coordinates
    if direction == 'N':
        for ny in range(y, -1, -1):
            for rock in rocks:
                if rock[1][0] == ny and rock[1][1] == x and rock[1][2] == '#':
                    return ny
        return -1
    if direction == 'S':
        for sy in range(y, length):
            for rock in rocks:
                if rock[1][0] == sy and rock[1][1] == x and rock[1][2] == '#':
                    return sy
        return length
    if direction == 'W':
        for wx in range(x, -1, -1):
            for rock in rocks:
                if rock[1][0] == y and rock[1][1] == wx and rock[1][2] == '#':
                    return wx
        return -1
    if direction == 'E':
        for ex in range(x, width):
            for rock in rocks:
                if rock[1][0] == y and rock[1][1] == ex and rock[1][2] == '#':
                    return ex
        return width
def count_rocks_between(direction, rock, closest_cube_rock, rocks, length, width):
    y, x = rock
    rock_count = 0
    if direction == 'N':
        for ny in range(y - 1, closest_cube_rock, -1):
            for rock in rocks:
                if rock[1][0] == ny and rock[1][1] == x and rock[1][2] == 'O':
                    rock_count += 1
    if direction == 'S':
        for sy in range(y + 1, closest_cube_rock):
            for rock in rocks:
                if rock[1][0] == sy and rock[1][1] == x and rock[1][2] == 'O':
                    rock_count += 1
    if direction == 'W':
        for wx in range(x - 1, closest_cube_rock, -1):
            for rock in rocks:
                if rock[1][0] == y and rock[1][1] == wx and rock[1][2] == 'O':
                    rock_count += 1
    if direction == 'E':
        for ex in range(x + 1, closest_cube_rock):
            for rock in rocks:
                if rock[1][0] == y and rock[1][1] == ex and rock[1][2] == 'O':
                    rock_count += 1
    return rock_count

def move(direction, rock, rocks, length, width):
    rock_number, props = rock
    y, x, rock_type = props
    closest_cube_rock = find_closest_cube_rock(direction, (y, x), rocks, length, width)
    num_blocking_round_rocks = count_rocks_between(direction, (y, x), closest_cube_rock, rocks, length, width)
    if direction == 'N':
        y = closest_cube_rock + num_blocking_round_rocks + 1
    if direction == 'S':
        y = closest_cube_rock - num_blocking_round_rocks - 1
    if direction == 'E':
        x = closest_cube_rock - num_blocking_round_rocks - 1
    if direction == 'W':
        x = closest_cube_rock + num_blocking_round_rocks + 1
    return [rock_number, [y, x, rock_type]]
        
def tilt(direction, rocks, length, width):
    new_rocks = []
    for rock in rocks:
        if rock[1][2] == 'O':
            new_rocks.append(move(direction, rock, rocks, length, width))
        else:
            new_rocks.append(rock)
    return new_rocks

def plate_load(length, rocks):
    total_load = 0
    for rock in rocks:
        if rock[1][2] == 'O':
            total_load += length - rock[1][0]
    return total_load

def print_plate(length, width, rocks):
    plate = []
    for y in range(length):
        row = []
        for x in range(width):
            is_rock = False
            for rock in rocks:
                if rock[1][0] == y and rock[1][1] == x:
                    if rock[1][2] == 'O':
                        row.append(str(rock[0]))
                    if rock[1][2] == '#':
                        row.append('X')
                    is_rock = True
            if not is_rock: row.append('.')
        plate.append(row)
    print('************************')
    for row in plate:
        print('\t'.join(row))
    print('************************')
    # pp.pprint(plate)
def find_rock(rock_number, rocks):
     for rock in rocks:
         if rock[0] == rock_number:
             return (rock[1][0], rock[1][1])
def simulate():
    length, width, rocks, setup = parse_input()[-3:]
    new_rocks = rocks.copy()
    num_cycles = 1000
    weights = []
    stabilized_weights = set()
    counter = 0
    length_weights = 0
    print(weights[(num_cycles - 3) % 7])
    for i in range(num_cycles):
        load = plate_load(length, new_rocks)
        weights.append(load)
        stabilized_weights.add(load)
        new_rocks = tilt('N', new_rocks, length, width)
        new_rocks = tilt('W', new_rocks, length, width)
        new_rocks = tilt('S', new_rocks, length, width)
        new_rocks = tilt('E', new_rocks, length, width)
    print(plate_load(length, new_rocks))
    
simulate()