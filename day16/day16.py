from enum import Flag
from functools import reduce
import pprint
pp = pprint.PrettyPrinter(indent=4)

class Direction(Flag):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

def parse_input():
    with open('day16_input.txt') as f:
        grid = [list(row) for row in f.read().splitlines()]
        return grid

def is_mirror(symbol):
    return not symbol == '.'

def move(position, direction, grid, mirror_locations, visited_grid):
    y, x = position
    length = len(grid)
    width = len(grid[0])
    visited_grid[y][x] = 1
    match direction:
        case Direction.UP:
            y -= 1
            while y > -1 and ((y, x) not in mirror_locations or grid[y][x] == '|'):
                visited_grid[y][x] = 1
                y -= 1
        case Direction.DOWN:
            y += 1
            while y < length and ((y, x) not in mirror_locations or grid[y][x] == '|'):
                visited_grid[y][x] = 1
                y += 1
        case Direction.RIGHT:
            x += 1
            while x < width and ((y, x) not in mirror_locations or grid[y][x] == '-'):
                visited_grid[y][x] = 1
                x += 1
        case Direction.LEFT:
            x -= 1
            while x > -1 and ((y, x) not in mirror_locations or grid[y][x] == '-'):
                visited_grid[y][x] = 1
                x -= 1
    if (y, x) in mirror_locations:
        mirror = mirror_locations[(y, x)]
        if not mirror[(direction.value + 2) % 4 + 1]:
            mirror_locations[(y, x)][(direction.value + 2) % 4 + 1] = True
            if mirror[0] == '|':
                mirror_locations[(y, x)][direction.value + 1] = True
                return [([y, x], Direction.UP), ([y, x], Direction.DOWN)]
            if mirror[0] == '-':
                mirror_locations[(y, x)][direction.value + 1] = True
                return [([y, x], Direction.RIGHT), ([y, x], Direction.LEFT)]
            match direction:
                case Direction.UP:
                    return [([y, x], Direction.RIGHT)] if mirror[0] == '/' else [([y, x], Direction.LEFT)]
                case Direction.DOWN:
                    return [([y, x], Direction.LEFT)] if mirror[0] == '/' else [([y, x], Direction.RIGHT)]
                case Direction.LEFT:
                    return [([y, x], Direction.DOWN)] if mirror[0] == '/' else [([y, x], Direction.UP)]
                case Direction.RIGHT:
                    return [([y, x], Direction.UP)] if mirror[0] == '/' else [([y, x], Direction.DOWN)]
    return []

def initialize_mirrors(grid):
    mirror_locations = dict()
    for y, row in enumerate(grid):
        for x, col in enumerate(row):
            if col != '.':
                mirror_locations[(y, x)] = [col, False, False, False, False]
    return mirror_locations

def energize_grid():
    grid = parse_input()
    width = len(grid[0])
    length = len(grid)
    visited_grid = [[0] * width for i in range(length)]
    mirror_locations = initialize_mirrors(grid)
    
    if grid[0][0] == '|' or grid[0][0] == '\\':
        beam_positions = [([0, 0], Direction.DOWN)]
        mirror_locations[(0, 0)] = [grid[0][0], False, False, False, True]
    elif grid[0][0] == '/':
        beam_positions = [([0, 0], Direction.UP)]
        mirror_locations[(0, 0)] = [grid[0][0], False, False, False, True]
    else:
        beam_positions = [([0, 0], Direction.RIGHT)]
    while beam_positions:
        position, direction = beam_positions.pop()
        next_positions = move(position, direction, grid, mirror_locations, visited_grid)
        beam_positions += next_positions
    return sum([sum(row) for row in visited_grid])
    
print(energize_grid())

# part 2
# copy/pasting this for others to see the initial approach and the second approach
def get_num_energized_spaces(initial_beams, grid, width, length):
    mirror_locations = initialize_mirrors(grid)
    visited_grid = [[0] * width for i in range(length)]
    beam_positions = initial_beams.copy()
    while beam_positions:
        position, direction = beam_positions.pop()
        next_positions = move(position, direction, grid, mirror_locations, visited_grid)
        beam_positions += next_positions
    # pp.pprint(visited_grid)
    return sum([sum(row) for row in visited_grid])

def initialize_beam(position, direction, grid):
    mirror = grid[position[0]][position[1]]
    if not is_mirror(mirror):
        return [(position, direction)]
    if mirror == '|':
        if direction == Direction.RIGHT or direction == Direction.LEFT:
            return [(position, Direction.UP), (position, Direction.DOWN)]
        else: return [(position, direction)]
    if mirror == '-':
        if direction == Direction.UP or direction == Direction.DOWN:
            return [(position, Direction.LEFT), (position, Direction.RIGHT)]
        else: return [(position, direction)]
    match direction:
        case Direction.UP:
            return [(position, Direction.RIGHT)] if mirror == '/' else [(position, Direction.LEFT)]
        case Direction.RIGHT:
            return [(position, Direction.UP)] if mirror == '/' else [(position,Direction.DOWN)]
        case Direction.DOWN:
            return [(position, Direction.LEFT)] if mirror == '/' else [(position,Direction.RIGHT)]
        case Direction.LEFT:
            return [(position, Direction.DOWN)] if mirror == '/' else [(position,Direction.UP)]
    return [(position, direction)]

def get_starting_beams(width, length):
    top_row = [([0, x], Direction.DOWN) for x in range(width)]
    right_column = [([y, width - 1], Direction.LEFT) for y in range(length)]
    bottom_row = [([length - 1, x], Direction.UP) for x in range(width)]
    left_column = [([y, 0], Direction.RIGHT) for y in range(length)]
    return bottom_row + top_row + right_column + left_column

def energize_grid_2():
    grid = parse_input()
    width = len(grid[0])
    length = len(grid)
    starting_beams = get_starting_beams(width, length)
    max_energized_spaces = 0
    for position, direction in starting_beams:
        beam_positions = initialize_beam(position, direction, grid)
        num_energized_spaces = get_num_energized_spaces(beam_positions, grid, width, length)
        if num_energized_spaces > max_energized_spaces:
            max_energized_spaces = num_energized_spaces
    return max_energized_spaces

print(energize_grid_2())