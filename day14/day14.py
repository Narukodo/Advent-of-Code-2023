from collections import defaultdict
import pprint

pp = pprint.PrettyPrinter(indent=4)

def parse_input():
    with open('day14_input.txt') as f:
        setup = f.read().splitlines()
        round_rocks_dict = defaultdict(lambda: [])
        cube_rocks_dict = defaultdict(lambda: [])
        for y, row in enumerate(setup):
            for x, char in enumerate(row):
                if char == 'O':
                    round_rocks_dict[x].append(y)
                if char == '#':
                    cube_rocks_dict[x].append(y)
        rocks = [(y, x, rock_type) for y, row in enumerate(setup) for x, rock_type in enumerate(row) if rock_type != '.']
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
    round_rocks, cube_rocks, num_rows = parse_input()[:3]
    final_load = 0
    for x in round_rocks:
        for y in round_rocks[x]:
            final_load += load((y, x), round_rocks, cube_rocks, num_rows)
    return final_load

print(count_load())

def move(direction, rock, length, width, plate):
    rock_count = 0
    y, x, rock_type = rock
    if direction == 'N':
        for i in range(y - 1, -1, -1):
            if plate[i][x] == 'O': rock_count += 1
            if plate[i][x] == '#': return [i + rock_count + 1, x, rock_type]
        return [rock_count, x, rock_type]
    elif direction == 'W':
        for i in range(x - 1, -1, -1):
            if plate[y][i] == 'O': rock_count += 1
            if plate[y][i] == '#': return [y, i + rock_count + 1, rock_type]
        return [y, rock_count, rock_type]
    elif direction == 'S':
        for i in range(y + 1, length):
            if plate[i][x] == 'O': rock_count += 1
            if plate[i][x] == '#': return [i - rock_count - 1, x, rock_type]
        return [length - rock_count - 1, x, rock_type]
    else:
        for i in range(x + 1, width):
            if plate[y][i] == 'O': rock_count += 1
            if plate[y][i] == '#': return [y, i - rock_count - 1, rock_type]
        return [y, width - rock_count - 1, rock_type]

def tilt(direction, rocks, length, width, plate):
    new_rocks = []
    for rock in rocks:
        if rock[2] == 'O':
            new_rocks.append(move(direction, rock, length, width, plate))
        else:
            new_rocks.append(rock)
    plate = construct_plate(new_rocks, length, width)
    return new_rocks, plate

def plate_load(length, rocks):
    total_load = 0
    for rock in rocks:
        if rock[2] == 'O':
            total_load += length - rock[0]
    return total_load

def construct_plate(rocks, length, width):
    new_plate = [['.'] * width for i in range(length)]
    load = 0
    for rock in rocks:
        new_plate[rock[0]][rock[1]] = rock[2]
        if rock[2] == 'O':
            load += length - rock[0]
    new_plate = [''.join(row) for row in new_plate]
    return new_plate

def simulate():
    length, width, rocks, plate = parse_input()[-4:]
    new_rocks = rocks.copy()
    num_cycles = 1000000000
    recorded_positions = dict()
    for i in range(num_cycles):
        new_rocks, plate = tilt('N', new_rocks, length, width, plate)
        new_rocks, plate = tilt('W', new_rocks, length, width, plate)
        new_rocks, plate = tilt('S', new_rocks, length, width, plate)
        new_rocks, plate = tilt('E', new_rocks, length, width, plate)
        current_plate_key = ''.join(plate)
        if current_plate_key in recorded_positions:
            cycles_left = (num_cycles - i) % (i - recorded_positions[current_plate_key]) - 1
            for i in range(cycles_left):
                new_rocks, plate = tilt('N', new_rocks, length, width, plate)
                new_rocks, plate = tilt('W', new_rocks, length, width, plate)
                new_rocks, plate = tilt('S', new_rocks, length, width, plate)
                new_rocks, plate = tilt('E', new_rocks, length, width, plate)
            return plate_load(length, new_rocks)
        else:
            recorded_positions[current_plate_key] = i
    return plate_load(length, new_rocks)
    
print(simulate())