import math
def parse_input():
    with open('day13/day13_input.txt') as f:
        patterns = [pattern.split() for pattern in f.read().split('\n\n')]
        return patterns

def find_reflection(pattern):
    width = len(pattern[0])
    length = len(pattern)
    rotated_pattern = [''.join(row) for row in list(zip(*pattern))]
    for i in range(1, width):
        if all([row[:i][-(width - i):] == row[i:][:i][::-1] for row in pattern]):
            return i
    for i in range(1, length):
        if all([row[:i][-(length - i):] == row[i:][:i][::-1] for row in rotated_pattern]):
            return 100 * i

def find_reflection_2(pattern):
    width = len(pattern[0])
    length = len(pattern)
    rotated_pattern = [''.join(row) for row in list(zip(*pattern))]
    for i in range(1, width):
        left = ''.join([row[:i][-(width - i):] for row in pattern])
        right = ''.join([row[i:][:i][::-1] for row in pattern])
        if sum(1 for index, char in enumerate(left) if char != right[index]) == 1:
            return i
    for i in range(1, length):
        top = ''.join([row[:i][-(length - i):] for row in rotated_pattern])
        bottom = ''.join([row[i:][:i][::-1] for row in rotated_pattern])
        if sum(1 for index, char in enumerate(top) if char != bottom[index]) == 1:
            return 100 * i

def count_reflection_ranks():
    patterns = parse_input()
    total_ranks = 0
    for pattern in patterns:
        # total_ranks += find_reflection(pattern) # part 1
        total_ranks += find_reflection_2(pattern) # part 2
    return total_ranks

print(count_reflection_ranks())
