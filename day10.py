from collections import namedtuple, defaultdict

Tile = namedtuple('Tile', ['position', 'symbol', 'north', 'east', 'south', 'west'])

def parse_input():
    with open('day10_test2_input.txt') as f: # expected: 20
        tile_pipe = lambda position: {
            '|': Tile(position, '|', True, False, True, False), #[N, E, S, W]
            '-': Tile(position, '-', False, True, False, True),
            'L': Tile(position, 'L', True, True, False, False),
            'J': Tile(position, 'J', True, False, False, True),
            '7': Tile(position, '7', False, False, True, True),
            'F': Tile(position, 'F', False, True, True, False),
            '.': Tile(position, '.', False, False, False, False),
            'S': Tile(position, 'S', True, True, True, True)
        }
        ground = f.read().splitlines()
        ground = [[tile_pipe((y, x))[pipe] for x, pipe in enumerate(row)] for y, row in enumerate(ground)]
        return ground

def is_connecting(tile_1, tile_2):
    tile_1_y, tile_1_x = tile_1.position
    tile_2_y, tile_2_x = tile_2.position
    if tile_1_y != tile_2_y and tile_1_x != tile_2_x:
        return False # two pipes are automatically disconnected if they are not to the direct cardinal direction of each other
    # they are horizontally aligned and the right end of the left pipe touches the left end of the right pipe
    if tile_1_y == tile_2_y and abs(tile_1_x - tile_2_x) == 1:
            return (tile_1_x < tile_2_x and tile_1.east == 1 and tile_2.west) or (tile_2_x < tile_1_x and tile_1.west == 1 and tile_2.east)
    # they are vertically aligned and the bottom end of the top pipe touches the top end of the bottom pipe
    if tile_1_x == tile_2_x and abs(tile_1_y - tile_2_y) == 1:
         return (tile_1_y < tile_2_y and tile_1.south == 1 and tile_2.north) or (tile_2_y < tile_1_y and tile_1.north == 1 and tile_2.south)
    return False

def find_start(ground):
    for row in ground:
         for tile in row:
              if tile.symbol == 'S':
                   return tile

def find_adjacent_connecting_tiles(ground, current_tile, visited):
    width = len(ground[0])
    length = len(ground)
    connecting_tiles = []
    y, x = current_tile.position
    if y > 0 and is_connecting(ground[y - 1][x], current_tile) and ground[y - 1][x].position not in visited:
         connecting_tiles += [ground[y - 1][x]]
    if y < length - 1 and is_connecting(ground[y + 1][x], current_tile) and ground[y + 1][x].position not in visited:
         connecting_tiles += [ground[y + 1][x]]
    if x > 0 and is_connecting(ground[y][x - 1], current_tile) and ground[y][x - 1].position not in visited:
         connecting_tiles += [ground[y][x - 1]]
    if x < width - 1 and is_connecting(ground[y][x + 1], current_tile) and ground[y][x + 1].position not in visited:
         connecting_tiles += [ground[y][x + 1]]
    return connecting_tiles

# use bfs to find max distance; since direction should not matter, then we enter both directions at the same time
def find_max_distance():
    ground = parse_input()
    start_tile = find_start(ground)
    distance = 0
    visited = []
    queued = [start_tile.position]
    next = []
    while queued:
        for tile in queued:
            current_y, current_x = tile
            visited.append((current_y, current_x))
            next += [tile.position for tile in find_adjacent_connecting_tiles(ground, ground[current_y][current_x], visited)]
        distance += 1
        queued = next.copy()
        next = []
    return distance - 1, visited
# print(find_max_distance())

def count_column(pipe_tiles):
    min_y = pipe_tiles[0]
    max_y = pipe_tiles[-1]
    space_count = 0
    tiles_in_loop = 0
    for i in range (min_y, max_y + 1):
        if i not in pipe_tiles and i - 1 in pipe_tiles:
            space_count += 1
        if space_count % 2 == 1 and i not in pipe_tiles:
            tiles_in_loop += 1
    return tiles_in_loop

# pipes only have two ends, so following from the start will yield the loop path
def count_area(loop_path):
    tiles = defaultdict(lambda: [])
    loop_path.sort()
    num_open_spaces = 0
    for y, x in loop_path:
        tiles[x] += [y]
    for x in sorted(tiles.keys()):
        num_open_spaces += count_column(tiles[x])
    return num_open_spaces

def get_loop_area():
    ground = parse_input()
    paths_from_start = list(set(find_max_distance()[1]))
    print(count_area(paths_from_start))
get_loop_area()