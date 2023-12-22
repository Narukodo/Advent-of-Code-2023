def parse_input():
    with open('day9/day9_input.txt') as f:
        histories = [[int(value) for value in line.split()] for line in f.read().splitlines()]
        return histories
    
def extrapolate():
    histories = parse_input()
    extrapolated_values = []
    for history in histories:
        differentials = [[value for value in history]]
        while any([differential != 0 for differential in differentials[0]]):
            differentials = [[value - differentials[0][index] for index, value in enumerate(differentials[0][1:])]] + differentials
        for index, differential in enumerate(differentials):
            if index == 0:
                differentials[index] += [0]
            else:
                differentials[index] += [differentials[index - 1][-1] + differential[-1]]
        extrapolated_values += [differentials[-1][-1]]
    return sum(extrapolated_values)

print(extrapolate())

def extrapolate_backwards():
    histories = parse_input()
    extrapolated_values = []
    for history in histories:
        differentials = [[value for value in history]]
        while any([differential != 0 for differential in differentials[0]]):
            differentials = [[value - differentials[0][index] for index, value in enumerate(differentials[0][1:])]] + differentials
        for index, differential in enumerate(differentials):
            if index == 0:
                differentials[index] = [0] + differentials[index]
            else:
                differentials[index] = [differential[0] - differentials[index - 1][0]] + differentials[index]
        print(differentials)
        extrapolated_values += [differentials[-1][0]]
    return sum(extrapolated_values)

print(extrapolate_backwards())