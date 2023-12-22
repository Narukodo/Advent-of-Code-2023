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
    round_rocks, cube_rocks, num_rows, width, rocks = parse_input()
    final_load = 0
    for x in round_rocks:
        for y in round_rocks[x]:
            final_load += load((y, x), round_rocks, cube_rocks, num_rows)
    return final_load

# print(count_load())

# def find_closest_cube_rock(direction, rock_coordinates, length, width, plate):
#     y, x = rock_coordinates
#     if direction == 'N':
#         for ny in range(y, -1, -1):
#             if plate[ny][x] == '#':
#                 return ny
#         return -1
#     if direction == 'S':
#         for sy in range(y, length):
#             if plate[sy][x] == '#':
#                 return sy
#         return length
#     if direction == 'W':
#         for wx in range(x, -1, -1):
#             if plate[y][wx] == '#':
#                 return wx
#         return -1
#     if direction == 'E':
#         for ex in range(x, width):
#             if plate[y][ex] == '#':
#                 return ex
#         return width
# def count_rocks_between(direction, rock, closest_cube_rock, plate):
#     y, x = rock
#     rock_count = 0
#     if direction == 'N':
#         for ny in range(y - 1, closest_cube_rock, -1):
#             if plate[ny][x] == 'O':
#                 rock_count += 1
#     if direction == 'S':
#         for sy in range(y + 1, closest_cube_rock):
#             if plate[sy][x] == 'O':
#                 rock_count += 1
#     if direction == 'W':
#         for wx in range(x - 1, closest_cube_rock, -1):
#             if plate[y][wx] == 'O':
#                 rock_count += 1
#     if direction == 'E':
#         for ex in range(x + 1, closest_cube_rock):
#             if plate[y][ex] == 'O':
#                 rock_count += 1
#     return rock_count

def new_position(direction, rock, length, width, plate):
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

def move(direction, rock, length, width, plate):
    # y, x, rock_type = rock
    return new_position(direction, rock, length, width, plate)
    # closest_cube_rock = find_closest_cube_rock(direction, (y, x), length, width, plate)
    # num_blocking_round_rocks = count_rocks_between(direction, (y, x), closest_cube_rock, plate)
    # if direction == 'N':
    #     y = closest_cube_rock + num_blocking_round_rocks + 1
    # if direction == 'S':
    #     y = closest_cube_rock - num_blocking_round_rocks - 1
    # if direction == 'E':
    #     x = closest_cube_rock - num_blocking_round_rocks - 1
    # if direction == 'W':
    #     x = closest_cube_rock + num_blocking_round_rocks + 1
    # return [y, x, rock_type]
        
def tilt(direction, rocks, length, width, plate):
    new_rocks = []
    for rock in rocks:
        if rock[2] == 'O':
            new_rocks.append(move(direction, rock, length, width, plate))
        else:
            new_rocks.append(rock)
    plate, load = construct_plate(new_rocks, length, width)
    return new_rocks, plate, load

def plate_load(length, rocks):
    total_load = 0
    for rock in rocks:
        if rock[2] == 'O':
            total_load += length - rock[0]
    return total_load

# def print_plate(length, width, rocks):
#     plate = []
#     for y in range(length):
#         row = []
#         for x in range(width):
#             is_rock = False
#             for rock in rocks:
#                 if rock[1][0] == y and rock[1][1] == x:
#                     if rock[1][2] == 'O':
#                         row.append(str(rock[0]))
#                     if rock[1][2] == '#':
#                         row.append('X')
#                     is_rock = True
#             if not is_rock: row.append('.')
#         plate.append(row)
#     print('************************')
#     for row in plate:
#         print('\t'.join(row))
#     print('************************')

def construct_plate(rocks, length, width):
    new_plate = []
    load = 0
    for i in range(length):
        row = ''
        for j in range(width):
            is_rock = False
            for rock in rocks:
                if rock[0] == i and rock[1] == j:
                    row += rock[2]
                    if rock[2] == 'O':
                        load += length - rock[0]
                    is_rock = True
            if not is_rock:
                row += '.'
        new_plate.append(row)
    return new_plate, load

def find_repeating_pattern(weights, length):
    for i in range(length):
        for j in range(2, length):
            if weights[i:i + j] == weights[i + j: i + j * 2]:
                return weights[i:i + j], i
    return [], False

def simulate():
    length, width, rocks, plate = parse_input()[-4:]
    new_rocks = rocks.copy()
    num_cycles = 1000000000
    weights = []
    weights_length = 0
    recorded_positions = dict()
    for i in range(num_cycles):
        load = plate_load(length, new_rocks)
        weights.append(load)
        weights_length += 1
        stabilized_weights, stabilized_offset = find_repeating_pattern(weights, weights_length)
        if stabilized_weights:
            return stabilized_weights[(num_cycles - stabilized_offset) % len(stabilized_weights)]
        new_rocks, plate, load = tilt('N', new_rocks, length, width, plate)
        # pp.pprint(plate)
        new_rocks, plate, load = tilt('W', new_rocks, length, width, plate)
        # pp.pprint(plate)
        new_rocks, plate, load = tilt('S', new_rocks, length, width, plate)
        # pp.pprint(plate)
        new_rocks, plate, load = tilt('E', new_rocks, length, width, plate)
        # pp.pprint(plate)
        # print(f'finished cycle {i} {load}')
        # current_plate_key = ''.join(plate)
        # if current_plate_key in recorded_positions:
        #     cycles_left = (num_cycles - i) % (i - recorded_positions[current_plate_key])
        #     for i in range(cycles_left):
        #         new_rocks, plate, load = tilt('N', new_rocks, length, width, plate)
        #         new_rocks, plate, load = tilt('W', new_rocks, length, width, plate)
        #         new_rocks, plate, load = tilt('S', new_rocks, length, width, plate)
        #         new_rocks, plate, load = tilt('E', new_rocks, length, width, plate)
        #     return load
        # else:
        #     recorded_positions[current_plate_key] = i
    return plate_load(length, new_rocks)
    
print(simulate())