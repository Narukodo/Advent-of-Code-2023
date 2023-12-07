from collections import defaultdict

def parse_input():
    with open('day7_input.txt') as f:
        hands_and_bids = [[line.split()[0] ,int(line.split()[1])] for line in f.read().splitlines()]
        return hands_and_bids

# part 1 
def hand_score(hand):
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    return sum([numbers.index(card)*(13**index) for index, card in enumerate(hand[::-1])])

def hand_type(hand):
    distinct_card_count = dict()
    for card in hand:
        if card in distinct_card_count:
            distinct_card_count[card] += 1
        else:
            distinct_card_count[card] = 1
    return ''.join(sorted([f'{distinct_card_count[card]}' for card in distinct_card_count]))

def categorize_hands(hands_with_bids):
    hand_types = {
    '11111': [], 
    '1112': [], 
    '122': [], 
    '113': [], 
    '23': [], 
    '14': [], 
    '5': []}
    for hand, bid in hands_with_bids:
        hand_types[hand_type(hand)].append((hand, hand_score(hand), bid))
    return [sorted(hand_types[hand], key=lambda x: x[1]) for hand in hand_types.keys()]

def sort_hands(hands_and_bids):
    return [hand for categorized_hands in categorize_hands(hands_and_bids) for hand in categorized_hands]

def total_winnings():
    hands_and_bids = parse_input()
    sorted_hands = sort_hands(hands_and_bids)
    total_winnings = sum([hands_scores_bids[2] * (index + 1) for index, hands_scores_bids in enumerate(sorted_hands)])
    return total_winnings

print(total_winnings())

# part 2
def hand_score_2(hand):
    numbers = ['0', '1', 'J', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A']
    return sum([numbers.index(card)*(13**index) for index, card in enumerate(hand[::-1])])

def hand_type_2(hand):
    distinct_card_count = dict()
    for card in hand:
        if card in distinct_card_count:
            distinct_card_count[card] += 1
        else:
            distinct_card_count[card] = 1
    if 'J' in distinct_card_count:
        max_card_count = 0
        max_card = ''
        for card in distinct_card_count:
            if distinct_card_count[card] > max_card_count and card != 'J':
                max_card_count = distinct_card_count[card]
                max_card = card
        if max_card:
            distinct_card_count[max_card] += distinct_card_count['J']
            del distinct_card_count['J']
    return ''.join(sorted([f'{distinct_card_count[card]}' for card in distinct_card_count]))

def categorize_hands_2(hands_with_bids):
    hand_types = {
    '11111': [], 
    '1112': [], 
    '122': [], 
    '113': [], 
    '23': [], 
    '14': [], 
    '5': []}
    for hand, bid in hands_with_bids:
        hand_types[hand_type_2(hand)].append((hand, hand_score_2(hand), bid))
    return [sorted(hand_types[hand], key=lambda x: x[1]) for hand in hand_types.keys()]

def sort_hands_2(hands_and_bids):
    return [hand for categorized_hands in categorize_hands_2(hands_and_bids) for hand in categorized_hands]

def total_winnings_2():
    hands_and_bids = parse_input()
    sorted_hands = sort_hands_2(hands_and_bids)
    total_winnings = sum([hands_scores_bids[2] * (index + 1) for index, hands_scores_bids in enumerate(sorted_hands)])
    return total_winnings

print(total_winnings_2())

# alternative, more readable solution.
def hand_type_3(hand):
    hand_types = ['11111', '1112', '122', '113', '23', '14', '5']
    distinct_card_count = defaultdict(lambda: 0)
    for card in hand:
        distinct_card_count[card] += 1
    num_jokers = distinct_card_count.pop('J', 0)
    if num_jokers == 5:
        return 6
    sorted_card_counts = sorted([distinct_card_count[card] for card in distinct_card_count])
    sorted_card_counts[-1] += num_jokers
    return hand_types.index(''.join(str(card_count) for card_count in sorted_card_counts))

def categorize_hands_3(hands_with_bids):
    hand_groups = [[],[],[],[],[],[],[]]
    for hand, bid in hands_with_bids:
        hand_groups[hand_type_3(hand)].append((hand, hand_score_2(hand), bid))
    return [hand for categorized_hands in hand_groups for hand in sorted(categorized_hands, key=lambda x: x[1])]

def total_winnings_3():
    hands_and_bids = parse_input()
    sorted_hands = categorize_hands_3(hands_and_bids)
    total_winnings = sum([hands_scores_bids[2] * (index + 1) for index, hands_scores_bids in enumerate(sorted_hands)])
    return total_winnings

print(total_winnings_3())