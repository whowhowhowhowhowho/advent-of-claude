def parse(text: str):
    return [tuple(map(int, r.split('-'))) for r in text.split(',')]


def part1(text: str) -> int:
    result = 0
    for start, end in parse(text):
        for i in range(start, end + 1):
            s = str(i)
            if len(s) % 2 != 0:
                continue
            if s[: len(s) // 2] == s[len(s) // 2:]:
                result += i
    return result


def part2(text: str) -> int:
    result = 0
    for start, end in parse(text):
        for i in range(start, end + 1):
            s = str(i)
            # for each possible length of sub ID, test if it repeats
            for l in range(1, len(s)):
                if len(s) % l != 0:
                    continue
                subs = [s[j: j + l] for j in range(0, len(s), l)]
                if len(set(subs)) == 1:
                    result += i
                    break  # only add once

    return result
