def parse_input():
    with open('day12_test_input.txt') as f:
        return [(line.split()[0], [int(number) for number in line.split()[1].split(',')]) for line in f.read().splitlines()]

def split_record(record):
    count = 1
    num_symbols = len(record)
    blocks = []
    while count < num_symbols:
        block = record[count - 1]
        while count < num_symbols and record[count] == record[count - 1]:
            block += record[count]
            count += 1
        blocks.append(block)
        count += 1
    return blocks

print(split_record(parse_input()[0][0]))

