from functools import total_ordering
from dataclasses import dataclass


def parse(text: str):
    fresh_ranges = []
    avail_ids = []

    for line in text.splitlines():
        if line == '':
            continue
        elif '-' in line:
            start, end = map(int, line.split('-'))
            fresh_ranges.append((start, end))
        else:
            avail_ids.append(int(line))

    return fresh_ranges, avail_ids


def part1(text: str) -> int:
    fresh_ranges, avail_ids = parse(text)
    result = 0
    for id in avail_ids:
        for start, end in fresh_ranges:
            if start <= id <= end:
                result += 1
                break  # ignore overlapping ranges

    return result


@dataclass
@total_ordering
class Range:
    start: int
    end: int  # inclusive

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __lt__(self, other):
        if self.start == other.start:
            return self.end < other.end
        return self.start < other.start

    def size(self):
        return self.end - self.start + 1

    def intersects(self, other):
        return not (self.end < other.start or other.end < self.start)

    def contains(self, other):
        return self.start <= other.start and self.end >= other.end

    def merge(self, other):
        if not self.intersects(other):
            raise ValueError(f"Ranges {self} and {other} don't intersect")

        return Range(min(self.start, other.start), max(self.end, other.end))

    def intersect(self, other):
        if not self.intersects(other):
            raise ValueError(f"Ranges {self} and {other} don't intersect")

        A, B = sorted((self, other))

        if A.contains(B):
            return B  # Range(B.start, B.end)

        return Range(B.start, A.end)


def part2(text: str) -> int:
    fresh_ranges = parse(text)[0]

    # convert to Range instances
    ranges = map(lambda r: Range(*r), fresh_ranges)

    result = []  # contains the merged ranges

    def merge_ranges():
        result.sort()
        i = 0

        while i < len(result) - 1:
            if result[i].intersects(result[i + 1]):
                # substitute this and the following range by their union,
                # causing len(result)--, thus no increment for i
                result[i: i + 2] = [result[i].merge(result[i + 1])]
            else:
                i += 1

    for r in ranges:
        result.append(r)
        merge_ranges()

    return sum(map(lambda r: r.size(), result))
