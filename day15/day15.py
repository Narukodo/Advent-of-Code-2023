def parse_input():
    with open('day15/day15_input.txt') as f:
        return f.read().split(',')
    
def get_box_number(string):
    current_hash = 0
    for char in string:
        current_hash = ((current_hash + ord(char)) * 17) % 256
    return current_hash

def sum_of_hashes():
    initialization_sequence = parse_input()
    return sum(map(get_box_number, initialization_sequence))

print(sum_of_hashes())

def parse_lens(lens):
    if '=' in lens:
        label, focal_length = lens.split('=')
        return [label, int(focal_length)]
    else:
        label, focal_length = lens.split('-')
        return [label, 0] # min is 1

def focusing_power(focal_length, box_number, slot_number):
    return (1 + box_number) * slot_number * focal_length

def apply_lens(box_line, box_number, lens):
    label, focal_length = lens
    if box_number in box_line:
        if focal_length > 0:
            box_line[box_number][label] = focal_length
        else:
            box_line[box_number].pop(label, None)
    if box_number not in box_line and focal_length > 0:
        box_line[box_number] = {label: focal_length}

def total_focusing_power():
    initialization_sequence = parse_input()
    box_line = dict()
    for step in initialization_sequence:
        label, focal_length = parse_lens(step)
        apply_lens(box_line, get_box_number(label), [label, focal_length])
    total_power = 0
    for box_number in box_line:
        for slot_number, lens_label in enumerate(box_line[box_number].keys(), 1):
            focal_length = box_line[box_number][lens_label]
            total_power += focusing_power(focal_length, box_number, slot_number)
    return total_power

print(total_focusing_power())