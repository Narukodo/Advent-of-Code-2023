def parse_input():
    with open('day4/day4_input.txt') as f: 
        cards_info = f.read().splitlines()
        cards_info = [card.split(': ')[1] for card in cards_info]
        card_numbers = [[set([int(number) for number in number_set.lstrip().split()]) for number_set in card.split(' | ')] for card in cards_info]
        return card_numbers

# part 1
def get_num_winning_numbers(winning_numbers, chosen_numbers):
    return len(winning_numbers.intersection(chosen_numbers))

def total_points():
    cards = parse_input()
    total_points = 0
    for card in cards:
        winning_numbers, chosen_numbers = card
        num_winning_chosen_numbers = get_num_winning_numbers(winning_numbers, chosen_numbers)
        if num_winning_chosen_numbers > 0:
            total_points += 2**(num_winning_chosen_numbers - 1)
    return total_points
print(total_points())

# part 2
def num_scratch_cards():
    cards = parse_input()
    final_card_count = [1] * len(cards)
    for card_number, card in enumerate(cards):
        winning_numbers, chosen_numbers = card
        num_winning_chosen_numbers = get_num_winning_numbers(winning_numbers, chosen_numbers)
        if num_winning_chosen_numbers > 0:
            for i in range(1, num_winning_chosen_numbers + 1):
                final_card_count[card_number + i] += final_card_count[card_number]
    return sum(final_card_count)
print(num_scratch_cards())