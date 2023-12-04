# assuming numbers will only be adjacent to one symbol at a time
def get_full_number_with_beginning_coord(x_coordinate, schematic_row):
    width = len(schematic_row)
    number = [schematic_row[x_coordinate]]
    counter_left = 1
    counter_right = 1
    beginning_coord = x_coordinate
    while x_coordinate + counter_right < width and schematic_row[x_coordinate + counter_right].isdigit():
        number.append(schematic_row[x_coordinate + counter_right])
        counter_right += 1
    while x_coordinate - counter_left >= 0 and schematic_row[x_coordinate - counter_left].isdigit():
        beginning_coord -= 1
        number[:0] = [schematic_row[x_coordinate - counter_left]]
        counter_left += 1
    return [beginning_coord, int(''.join(number))]

def get_adjacent_numbers(symbol_coordinates, schematic, adjacent_number_coordinates):
    symbol_y, symbol_x = symbol_coordinates
    length = len(schematic)
    width = len(schematic[0])
    adjacent_numbers = []
    for y in range(-1, 2):
        if symbol_y + y >= 0 and symbol_y + y < length:
            for x in range(-1, 2):
                if symbol_x + x >= 0 and symbol_x + x < width and schematic[symbol_y + y][symbol_x + x].isdigit():
                    beginning_coord, full_number = get_full_number_with_beginning_coord(symbol_x + x, schematic[symbol_y + y])
                    if [symbol_y + y, beginning_coord] not in adjacent_number_coordinates:
                        adjacent_number_coordinates.append([symbol_y + y, beginning_coord])
                        adjacent_numbers.append(full_number)
    return adjacent_number_coordinates, adjacent_numbers

def is_symbol(char):
    return not char.isdigit() and char != '.'

def parse_input():
    with open('day3_input.txt') as f:
        engine_schematic = f.read().splitlines()
        return engine_schematic

def sum_adjacent_numbers():
    engine_schematic = parse_input()
    adjacent_number_coordinates = []
    adjacent_numbers = []
    for y, row in enumerate(engine_schematic):
        for x, char in enumerate(row):
            if is_symbol(char):
                # side effects are not great here, but if it ain't broke, don't touch it (for now)
                local_adjacent_number_coord, local_adjacent_numbers = get_adjacent_numbers([y, x], engine_schematic, adjacent_number_coordinates)
                adjacent_number_coordinates = local_adjacent_number_coord
                adjacent_numbers += local_adjacent_numbers
    return sum(adjacent_numbers)

def sum_gear_ratios():
    engine_schematic = parse_input()
    adjacent_number_coordinates = []
    sum_ratios = 0
    for y, row in enumerate(engine_schematic):
        for x, char in enumerate(row):
            if char == '*':
                local_adjacent_number_coord, local_adjacent_numbers = get_adjacent_numbers([y, x], engine_schematic, adjacent_number_coordinates)
                if len(local_adjacent_numbers) == 2:
                    gear_ratio = local_adjacent_numbers[0] * local_adjacent_numbers[1]
                    sum_ratios += gear_ratio
    return sum_ratios
    

print(sum_gear_ratios())
