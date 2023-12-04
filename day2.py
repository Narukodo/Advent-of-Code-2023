def sanitize_handful(handful):
    colours = ['red', 'green', 'blue']
    new_handful = [0, 0, 0]
    for ball_count in handful:
        number, colour = ball_count.split(' ')
        new_handful[colours.index(colour)] = int(number)
    return new_handful

# part 1
def is_handful_possible(handful):
    MAX_CUBES = [12, 13, 14] # [RED, GREEN, BLUE]
    return all([ball_type <= MAX_CUBES[ball_colour_number] for ball_colour_number, ball_type in enumerate(handful)])

def is_game_possible(game):
    return all([is_handful_possible(handful) for handful in game])

def evaluate_possible_games(game_results):
    return [is_game_possible(game) for game in game_results]

def parse_input():
    with open('day2_input.txt') as f:
        game_results = f.read().splitlines()
        game_results = [game.split(': ')[1] for game in game_results]
        handfuls_by_game = [game.split('; ') for game in game_results]
        handfuls_by_game = [[handful.split(', ') for handful in game] for game in handfuls_by_game]
        for game in handfuls_by_game:
            for index, handful in enumerate(game):
                game[index] = sanitize_handful(handful)
        return handfuls_by_game

def sum_ids_for_possible_games():
    results = 0
    game_results = parse_input()
    game_feasibility = evaluate_possible_games(game_results)
    for game_id, game_is_possible in enumerate(game_feasibility):
        if game_is_possible:
            results += game_id + 1
    return results

print(sum_ids_for_possible_games())

# part 2
def cube_power(cube_set):
    red, green, blue = cube_set
    return red * green * blue

def fewest_possible_cubes_by_colour_in_game(game):
    sets_by_colour = zip(*game)
    return [max(colour) for colour in sets_by_colour]

def sum_of_power_of_min_cube_sets():
    game_results = parse_input()
    return sum([cube_power(fewest_possible_cubes_by_colour_in_game(game)) for game in game_results])
    
print(sum_of_power_of_min_cube_sets())