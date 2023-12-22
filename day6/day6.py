import math

def parse_input():
    with open('day6/day6_input.txt') as f:
        game_record = f.read().splitlines()
        current_best_results = [[int(value) for value in line.split()[1:]] for line in game_record]
        single_game_results = [int(''.join(line.split()[1:])) for line in game_record]
        return zip(*current_best_results), single_game_results

def distance(time_limit, time_held):
    return -time_held**2 + time_limit*time_held

def winning_holding_times(time_limit, best_record):
    min_time = math.ceil(time_limit/2 - math.sqrt(time_limit**2 - 4*best_record)/2)
    max_time = math.floor(time_limit/2 + math.sqrt(time_limit**2 - 4*best_record)/2)
    if distance(time_limit, min_time) == best_record:
        min_time += 1
    if distance(time_limit, max_time) == best_record:
        max_time -= 1
    return (min_time, max_time)

# part 1
def win_all_games():
    best_records = parse_input()[0]
    win_methods_product = 1
    for time_limit, best_record in best_records:
        min_time, max_time = winning_holding_times(time_limit, best_record)
        num_winning_methods =  max_time - min_time + 1
        win_methods_product *= num_winning_methods
    return win_methods_product

print(win_all_games())

# part 2
def win_big_game():
    time_limit, best_record = parse_input()[1]
    min_winning_time,  max_winning_time = winning_holding_times(time_limit, best_record)
    return max_winning_time - min_winning_time + 1

print(win_big_game())
