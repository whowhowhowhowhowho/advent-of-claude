from functools import cache
import re


def part1(text: str) -> int:
    input = text.splitlines()
    tachyons = {input[0].find('S')}

    n_splits = 0
    for line in input[1:]:
        for splitter in map(lambda m: m.start(), re.finditer(r'\^', line)):
            # is there a tachyon beam at this splitter ?
            if splitter in tachyons:
                n_splits += 1
                tachyons.remove(splitter)
                tachyons |= {splitter - 1, splitter + 1}

    return n_splits


def part2(text: str) -> int:
    input = text.splitlines()

    # memoized function to compute the timelines originating from a certain point
    @cache
    def timelines(row, col):
        # step downwards to next splitter
        while row < len(input) and input[row][col] != '^':
            row += 1

        if row >= len(input):
            return 1
        else:
            return timelines(row + 1, col - 1) + timelines(row + 1, col + 1)

    return timelines(1, input[0].find('S'))
