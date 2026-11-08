import re


def part1(text: str) -> int:
    sheet = [re.sub(r'\s+', ' ', line.strip()).split(' ') for line in text.splitlines()]
    return sum([eval(sheet[-1][col].join([sheet[row][col] for row in range(len(sheet) - 1)])) for col in range(len(sheet[0]))])


def part2(text: str) -> int:
    sheet = text.splitlines()

    result = 0

    col = 0
    while col < len(sheet[0]):
        if (next_ops := list(map(lambda o: sheet[-1].find(o, col + 1), ('+', '*')))) == [-1, -1]:
            col_size = len(sheet[0]) - col + 1
        elif -1 in next_ops:
            col_size = max(next_ops) - col
        else:
            col_size = min(next_ops) - col

        result += eval(sheet[-1][col].join([''.join([sheet[row][col + i]
                       for row in range(len(sheet) - 1)]) for i in range(col_size - 1)]))

        col += col_size

    return result
