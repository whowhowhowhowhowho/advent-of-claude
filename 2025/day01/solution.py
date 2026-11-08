def parse(text: str) -> list:
    return [(line[0], int(line[1:])) for line in text.splitlines() if line]


def get_password(comb):
    # comb: list of tuples (L|R, amount)
    current = 50
    part1 = 0
    part2 = 0

    for direction, amount in comb:
        assert current >= 0

        if direction == 'L':
            amount *= -1

        # ----- part 2 -----------------------------------------------------------------

        # we cross 0 amount // 100 times and maybe one more
        part2 += (abs(amount) // 100)
        amount_rest = amount % 100
        if amount < 0 and amount_rest > 0:
            amount_rest -= 100

        # do we cross 0 after all?
        if current != 0 and current + amount_rest <= 0 or current + amount_rest >= 100:
            part2 += 1

        # ----- end part 2 -------------------------------------------------------------

        # ----- part 1 -----------------------------------------------------------------
        current = (current + amount) % 100
        if current == 0:
            part1 += 1
        # ----- end part 1 -------------------------------------------------------------

    return part1, part2


def part1(text: str) -> int:
    return get_password(parse(text))[0]


def part2(text: str) -> int:
    return get_password(parse(text))[1]
