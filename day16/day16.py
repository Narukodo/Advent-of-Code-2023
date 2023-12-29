from enum import Flag
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

def energize_grid():
    grid = parse_input()
    width = len(grid[0])
    length = len(grid)
    visited_grid = [[0] * width for i in range(length)]
    mirror_locations = dict()
    for y, row in enumerate(grid):
        for x, col in enumerate(row):
            if col != '.':
                mirror_locations[(y, x)] = [col, False, False, False, False]
    
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
