import math

def parse_input():
    with open('day8/day8_input.txt') as f:
        instructions = f.read().splitlines()
        directions = instructions[0]
        map_nodes = [connection.split(' = ') for connection in instructions[2:]]
        network = dict((current_node, {'L': next_nodes.split(', ')[0][1:], 'R': next_nodes.split(', ')[1][:-1]}) for current_node, next_nodes in map_nodes)
        return directions, network

# part 1
def follow_map():
    directions, network = parse_input()
    NUM_DIRECTIONS = len(directions)
    current_node = 'AAA'
    current_instruction = 0
    num_steps = 0
    while current_node != 'ZZZ':
        current_node = network[current_node][directions[current_instruction]]
        current_instruction = (current_instruction + 1) % NUM_DIRECTIONS
        num_steps += 1
    return num_steps
print(follow_map())

# part 2
def lcm(numbers):
    num_numbers = len(numbers)
    if num_numbers == 1:
        return numbers[0]
    if num_numbers == 2:
        a, b = numbers
        return a*b // math.gcd(a, b)
    lcm_rest = lcm(numbers[1:])
    return numbers[0]*lcm_rest // math.gcd(numbers[0], lcm_rest)

def get_all_starting_nodes(network):
    return [key for key in network.keys() if key[-1] == 'A']

def num_steps_to_end(directions, num_directions, network, current_node):
    current_node = current_node
    current_instruction = 0
    num_steps = 0
    while current_node[-1] != 'Z':
        current_node = network[current_node][directions[current_instruction]]
        current_instruction = (current_instruction + 1) % num_directions
        num_steps += 1
    return num_steps

def navigate(direction, network, current_nodes):
    return [network[current_node][direction] for current_node in current_nodes]

def follow_ghost_instructions():
    directions, network = parse_input()
    NUM_DIRECTIONS = len(directions)
    current_nodes = get_all_starting_nodes(network)
    num_terminal_steps = [num_steps_to_end(directions, NUM_DIRECTIONS, network, current_node) for current_node in current_nodes]
    return lcm(num_terminal_steps)

print(follow_ghost_instructions())

