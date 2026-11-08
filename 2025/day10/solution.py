from functools import lru_cache
import itertools
from typing import Dict, List, Tuple


def parse_line(line: str) -> Tuple[Tuple[int, ...], List[Tuple[int, ...]], Tuple[int, ...]]:
    parts = line.split()
    lights = tuple(1 if c == '#' else 0 for c in parts[0][1:-1])
    buttons = [tuple(int(i) for i in part[1:-1].split(',')) for part in parts[1:-1]]
    joltages = tuple(int(i) for i in parts[-1][1:-1].split(','))
    return lights, buttons, joltages


def subset_effects(buttons: List[Tuple[int, ...]], n: int) -> Dict[Tuple[int, ...], List[Tuple[int, Tuple[int, ...]]]]:
    """Map each parity pattern to the (press count, counter increase) of every button subset producing it."""
    effects = {}
    for k in range(len(buttons) + 1):
        for combo in itertools.combinations(buttons, k):
            counts = [0] * n
            for button in combo:
                for i in button:
                    counts[i] += 1
            parity = tuple(c % 2 for c in counts)
            effects.setdefault(parity, []).append((k, tuple(counts)))
    return effects


def fewest_light_presses(lights: Tuple[int, ...], buttons: List[Tuple[int, ...]]) -> int:
    # pressing a button twice cancels out, so each button is pressed 0 or 1 times
    return min(k for k, _ in subset_effects(buttons, len(lights))[lights])


def fewest_joltage_presses(buttons: List[Tuple[int, ...]], joltages: Tuple[int, ...]) -> int:
    effects = subset_effects(buttons, len(joltages))

    # the buttons pressed an odd number of times must match the parity of the target;
    # after pressing those once, every counter is even and the rest is two times a smaller problem
    @lru_cache(maxsize=None)
    def solve(target: Tuple[int, ...]) -> float:
        if not any(target):
            return 0
        best = float('inf')
        for k, counts in effects.get(tuple(t % 2 for t in target), []):
            if all(c <= t for c, t in zip(counts, target)):
                rest = tuple((t - c) // 2 for c, t in zip(counts, target))
                best = min(best, k + 2 * solve(rest))
        return best

    return int(solve(joltages))


def part1(text: str) -> int:
    total = 0
    for line in text.split('\n'):
        lights, buttons, _ = parse_line(line)
        total += fewest_light_presses(lights, buttons)
    return total


def part2(text: str) -> int:
    total = 0
    for line in text.split('\n'):
        _, buttons, joltages = parse_line(line)
        total += fewest_joltage_presses(buttons, joltages)
    return total
