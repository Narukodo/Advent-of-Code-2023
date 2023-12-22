import pprint
pp = pprint.PrettyPrinter(indent=4)

def parse_input():
    with open('day11/day11_input.txt') as f:
        space_image = f.read().splitlines()
        rotated_space_image = list(zip(*space_image))
        empty_rows = {index for index, row in enumerate(space_image) if '#' not in row}
        empty_cols = {index for index, col in enumerate(rotated_space_image) if '#' not in col}
        galaxies = sorted([(y, x) for y in range(len(space_image)) for x in range(len(rotated_space_image)) if space_image[y][x] == '#'])
        return galaxies, empty_rows, empty_cols

def count_distance(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

def sum_distances():
    galaxies, empty_rows, empty_cols = parse_input()
    total_distance = 0
    for index, galaxy in enumerate(galaxies):
        for galaxy2 in galaxies[index + 1:]:
            rows = set(list(range(*sorted([galaxy[0], galaxy2[0]]))))
            cols = set(list(range(*sorted([galaxy[1], galaxy2[1]]))))
            row_offset = len(rows.intersection(empty_rows)) * 999999
            col_offset = len(cols.intersection(empty_cols)) * 999999
            distance = abs(galaxy[0] - galaxy2[0]) + abs(galaxy[1] - galaxy2[1]) + row_offset + col_offset
            total_distance += distance
    return total_distance

pp.pprint(sum_distances())