from copy import deepcopy


def parse(text: str):
    return [list(line) for line in text.splitlines()]


def count_adj(x, y, arr):
    max_x = len(arr[0]) - 1
    max_y = len(arr) - 1
    adj = 0
    for i in (-1, 0, 1):
        for j in (-1, 0, 1):
            if i == 0 and j == 0:
                continue
            d_x = x + i
            d_y = y + j
            if d_x < 0 or d_x > max_x or d_y < 0 or d_y > max_y:
                continue

            if arr[d_x][d_y] == '@':
                adj += 1

    return adj


def part1(text: str) -> int:
    arr = parse(text)
    result = 0
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            if arr[i][j] == '.':
                continue
            if count_adj(i, j, arr) < 4:
                result += 1

    return result


def remove_rolls(arr):
    # remove all possible rolls
    # --> first determine for every roll whether it can be removed
    # --> then remove all of those at once
    # return new array and number of removed rolls

    new_arr = deepcopy(arr)
    n_removed = 0

    for x in range(len(new_arr)):
        for y in range(len(new_arr[x])):
            if arr[x][y] == '.':
                continue
            if count_adj(x, y, arr) < 4:
                new_arr[x][y] = '.'
                n_removed += 1

    return new_arr, n_removed


def part2(text: str) -> int:
    arr = parse(text)
    new_arr = arr
    result = 0

    while True:
        new_arr, n_removed = remove_rolls(new_arr)
        if n_removed == 0:
            break
        result += n_removed

    return result
