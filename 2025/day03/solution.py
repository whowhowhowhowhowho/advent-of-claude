import itertools


def prepare_bank(bank, n_batteries):
    # reduce the bank's length and thus the combinations as far as possible
    new_bank = ''
    pos = 0

    while pos + n_batteries < len(bank):
        digit = 9
        while digit > 0:
            while True:
                next_pos = bank.find(str(digit), pos)
                if next_pos < 0 or (next_pos + n_batteries > len(bank) + len(new_bank)):
                    digit -= 1
                    break
                new_bank += str(digit)
                pos = next_pos + 1
                digit = 9  # next char, start over

    return new_bank + bank[pos:]


def solve(banks, n_batteries):
    def max_joltage(bank, n_batteries):
        return max(map(lambda comb: int(''.join(comb)), itertools.combinations(bank, n_batteries)))

    banks = [prepare_bank(bank, n_batteries) for bank in banks]
    return sum(map(lambda bank: max_joltage(bank, n_batteries), banks))


def part1(text: str) -> int:
    return solve(text.splitlines(), 2)


def part2(text: str) -> int:
    return solve(text.splitlines(), 12)
