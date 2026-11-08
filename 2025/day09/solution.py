import itertools
from typing import List, Tuple


def parse(text: str) -> List[Tuple[int, int]]:
    return [tuple(int(v) for v in line.split(',')) for line in text.split('\n')]


def area(a: Tuple[int, int], b: Tuple[int, int]) -> int:
    return (abs(a[0] - b[0]) + 1) * (abs(a[1] - b[1]) + 1)


def part1(text: str) -> int:
    return max(area(a, b) for a, b in itertools.combinations(parse(text), 2))


def compress(values: List[int]) -> dict:
    """Map each coordinate to a grid index, keeping a cell for every non-empty gap between coordinates."""
    index = {}
    i = 1  # index 0 is a border of outside cells
    for k, v in enumerate(values):
        index[v] = i
        i += 1
        if k + 1 < len(values) and values[k + 1] - v > 1:
            i += 1
    return index


def part2(text: str) -> int:
    tiles = parse(text)
    xs = compress(sorted({x for x, _ in tiles}))
    ys = compress(sorted({y for _, y in tiles}))
    width = max(xs.values()) + 2
    height = max(ys.values()) + 2

    # 0 = unknown, 1 = loop, 2 = outside
    grid = [[0] * width for _ in range(height)]
    for (ax, ay), (bx, by) in zip(tiles, tiles[1:] + tiles[:1]):
        x0, x1 = sorted((xs[ax], xs[bx]))
        y0, y1 = sorted((ys[ay], ys[by]))
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                grid[y][x] = 1

    stack = [(0, 0)]
    grid[0][0] = 2
    while stack:
        x, y = stack.pop()
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < width and 0 <= ny < height and grid[ny][nx] == 0:
                grid[ny][nx] = 2
                stack.append((nx, ny))

    # prefix sums of outside cells
    outside = [[0] * (width + 1) for _ in range(height + 1)]
    for y in range(height):
        for x in range(width):
            outside[y + 1][x + 1] = (outside[y][x + 1] + outside[y + 1][x] - outside[y][x]
                                     + (grid[y][x] == 2))

    best = 0
    for a, b in itertools.combinations(tiles, 2):
        size = area(a, b)
        if size <= best:
            continue
        x0, x1 = sorted((xs[a[0]], xs[b[0]]))
        y0, y1 = sorted((ys[a[1]], ys[b[1]]))
        bad = outside[y1 + 1][x1 + 1] - outside[y0][x1 + 1] - outside[y1 + 1][x0] + outside[y0][x0]
        if bad == 0:
            best = size
    return best
