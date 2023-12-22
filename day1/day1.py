import re

with open('day1_input.txt') as f:
    fancy_values = f.read().splitlines()

    # day 1
    number_values = filter(lambda x: x != '', [''.join(re.split(r'[\D]+', line)) for line in fancy_values])
    values = [int(f'{number_value[0]}{number_value[-1]}') for number_value in number_values]
    print(sum(values))

    # day 2
    str_to_number= {
        'one': '1',
        'two': '2',
        'three': '3',
        'four': '4',
        'five': '5',
        'six': '6',
        'seven': '7',
        'eight': '8',
        'nine': '9'
    }

    word_number_patterns = [
        r'one',
        r'two',
        r'three',
        r'four',
        r'five',
        r'six',
        r'seven',
        r'eight',
        r'nine']
    
    number_values = []
    for fancy_value in fancy_values:
        match_indices = []
        for i in range(9):
            matches = re.finditer(word_number_patterns[i], fancy_value)
            match_indices += [[match.start(), match.end()] for match in matches]
        matches = re.finditer('\d+', fancy_value)
        match_indices += [[match.start(), match.end()] for match in matches]
        match_indices.sort(key=lambda x: x[0])
        number_list = [fancy_value[idx[0]: idx[1]] for idx in match_indices]
        number_list = [str_to_number[value] if value in str_to_number else value for value in number_list]
        clean_digits = ''.join(number_list)
        number_values.append(int(f'{clean_digits[0]}{clean_digits[-1]}'))
    print(sum(number_values))
        