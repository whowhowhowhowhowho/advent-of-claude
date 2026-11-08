from dataclasses import dataclass
import itertools
from typing import List, Set, Tuple


@dataclass(frozen=True)
class Tile:
    x: int
    y: int

    def __repr__(self):
        return f'({self.x}, {self.y})'

    def area_with(self, other):
        return (abs(self.x - other.x) + 1) * (abs(self.y - other.y) + 1)


class Rectangle(object):
    a: Tile
    b: Tile

    # props for iteration logic
    pos: Tile
    orientation: Tuple[int]
    stop: bool

    def corners(self) -> Tuple[Tile]:
        return (
            self.a,
            Tile(self.a.x, self.b.y),
            self.b,
            Tile(self.b.x, self.a.y)
        )

    def sides(self) -> Tuple[Tuple[Tile]]:
        a, b, c, d = self.corners()
        return (
            (a, b),
            (b, c),
            (c, d),
            (d, a)
        )

    def __repr__(self):
        return f'{self.a} - {self.b}'

    def area(self):
        return self.a.area_with(self.b)

    def __iter__(self):
        return self

    def next(self):
        if self.stop:
            raise StopIteration()

        if self.pos == self.b:
            self.stop = True
            return self.pos

        else:
            result = self.pos

            if self.pos.y == self.b.y:
                self.pos = Tile(self.pos.x + self.orientation[0], self.a.y)
            else:
                self.pos = Tile(self.pos.x, self.pos.y + self.orientation[1])

            return result

    def __next__(self):
        return self.next()

    def make_orientation(self):
        o_x, o_y = 0, 0

        if self.a.x < self.b.x:
            o_x = 1
        elif self.a.x > self.b.x:
            o_x = -1

        if self.a.y < self.b.y:
            o_y = 1
        elif self.a.y > self.b.y:
            o_y = -1

        return (o_x, o_y)

    def __init__(self, a: Tile, b: Tile):
        self.a = a
        self.b = b

        self.pos = a
        self.orientation = self.make_orientation()
        self.stop = False


def parse(text: str):
    return [Tile(*map(int, line.split(','))) for line in text.splitlines()]


def part1(text: str) -> int:
    red_tiles = parse(text)
    return max(map(lambda pair: Rectangle(*pair).area(), itertools.combinations(red_tiles, 2)))


def get_borders(red_tiles):
    borders = set()
    for i in range(len(red_tiles)):
        borders |= set(
            Rectangle(red_tiles[i], red_tiles[(i + 1) % len(red_tiles)])
        )

    return borders


class Polygon:
    red_tiles: List[Tile]
    borders: Set[Tile]
    boundaries: Tuple[Tile]

    def __init__(self, red_tiles: List[Tile]):
        self.red_tiles = red_tiles
        self.borders = get_borders(red_tiles)
        self.boundaries = (
            Tile(min(map(lambda t: t.x, red_tiles)),
                 min(map(lambda t: t.y, red_tiles))),
            Tile(max(map(lambda t: t.x, red_tiles)),
                 max(map(lambda t: t.y, red_tiles)))
        )

    def contains(self, t: Tile):
        if t in self.borders:
            return True

        # cast a ray horizontally through this polygon
        ray = Tile(self.boundaries[0].x, t.y)

        border_hits = 0
        while ray.x < t.x:
            if ray in self.borders:
                border_hits += 1
                while ray in self.borders:
                    ray = Tile(ray.x + 1, ray.y)
            else:
                ray = Tile(ray.x + 1, ray.y)

        # must hit odd number of times
        return bool(border_hits > 0 and (border_hits & 1))

    def is_legal(self, r: Rectangle):
        def ray(start: Tile, end: Tile):
            if start == end:
                return

            orientation = [0, 0]
            if start.x < end.x:
                orientation[0] = 1
            elif start.x > end.x:
                orientation[0] = -1
            if start.y < end.y:
                orientation[1] = 1
            elif start.y > end.y:
                orientation[1] = -1

            assert (orientation[0] == 0) ^ (orientation[1] == 0)
            assert start != end

            while start != end:
                start = Tile(
                    start.x + orientation[0], start.y + orientation[1])
                yield start  # excludes first tile

            return

        def ray_stays_in_polygon(start: Tile, end: Tile):
            if start == end:
                return True

            ray_iter = ray(start, end)

            while True:
                try:
                    t = next(ray_iter)
                    if t in self.borders:  # we hit a border --> walk along
                        try:
                            while t in self.borders:
                                t = next(ray_iter)
                        except StopIteration:  # we hit end without leaving border
                            return True
                except StopIteration:
                    return True

                if not self.contains(t):  # first tile after leaving border
                    return False

                # we are still inside, move to next border
                try:
                    while t not in self.borders:
                        t = next(ray_iter)
                    continue
                except StopIteration:
                    # we did not hit a border
                    return True

        # walk this rectangle's sides
        # --> when we first leave the polygon's border, we determine whether we're inside or outside the polygon
        # --> if outside --> false
        # --> if inside --> make sure that we never cross the border again
        for side in r.sides():
            if not ray_stays_in_polygon(*side):
                return False

        return True


def part2(text: str) -> int:
    red_tiles = parse(text)
    p = Polygon(red_tiles)

    results = []
    for comb in itertools.combinations(red_tiles, 2):
        r = Rectangle(*comb)
        if p.is_legal(r):
            results.append(r.area())

    return max(results)
