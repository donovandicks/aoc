import re
from functools import reduce
from io import TextIOWrapper
from typing import Callable

DIGIT = re.compile(r"\d")


def load(day: int) -> TextIOWrapper:
    return open(f"./inputs/day_{day}.txt", encoding="utf-8")


def first_and_last[T](xs: list[T]) -> tuple[T, T]:
    return xs[0], xs[-1]


def process_d1_p1(data: TextIOWrapper) -> int:
    return sum(
        [int("".join(first_and_last(DIGIT.findall(line)))) for line in data.readlines()]
    )


def process_d1_p2(data: TextIOWrapper) -> int:
    clean_lines = (
        data.read()
        .replace("one", "o1e")
        .replace("two", "t2o")
        .replace("three", "t3e")
        .replace("four", "f4r")
        .replace("five", "f5e")
        .replace("six", "s6x")
        .replace("seven", "s7n")
        .replace("eight", "e8t")
        .replace("nine", "n9e")
        .strip()
        .split("\n")
    )

    return sum(
        [int("".join(first_and_last(DIGIT.findall(line)))) for line in clean_lines]
    )


def process_d2_p1(data: TextIOWrapper) -> int:
    CUBES = {
        "red": 12,
        "green": 13,
        "blue": 14,
    }

    def is_possible(words: list[str]) -> bool:
        for i in range(0, len(words), 2):
            if int(words[i]) > CUBES[words[i + 1]]:
                return False

        return True

    return sum(
        [
            int(line.split(":")[0].split(" ")[1])
            for line in data.readlines()
            if is_possible(
                line.split(":")[1].strip().replace(",", "").replace(";", "").split(" ")
            )
        ]
    )


def process_d2_p2(data: TextIOWrapper) -> int:
    def make_power(words: list[str]) -> int:
        maxes = {
            "red": 0,
            "green": 0,
            "blue": 0,
        }

        for i in range(0, len(words), 2):
            maxes[words[i + 1]] = max(int(words[i]), maxes[words[i + 1]])

        return reduce(lambda x, y: x * y, maxes.values(), 1)

    return sum(
        [
            make_power(
                line.split(":")[1].strip().replace(",", "").replace(";", "").split(" ")
            )
            for line in data.readlines()
        ]
    )


def process_d3_p1(data: TextIOWrapper) -> int:
    matrix = [line.strip() for line in data.readlines()]

    def check_adj(r: int, c: int) -> bool:
        cycle = [
            [-1, -1],  # tl
            [-1, 0],  # tm
            [-1, 1],  # tr
            [0, 1],  # r
            [1, 1],  # br
            [1, 0],  # bm
            [1, -1],  # bl
            [0, -1],  # l
        ]

        for offset in cycle:
            try:
                sym = matrix[r + offset[0]][c + offset[1]]
                if not sym.isnumeric() and sym != ".":
                    return True
            except IndexError:
                continue

        return False

    tot = 0
    for r in range(len(matrix)):
        c = 0
        num = ""
        adj_to_sym = False
        while c < len(matrix[r]):
            if not matrix[r][c].isnumeric():
                c += 1
                continue

            while (char := matrix[r][c]).isnumeric():
                num += char
                if check_adj(r, c):
                    adj_to_sym = True

                if (next := c + 1) < len(matrix[r]):
                    c = next
                else:
                    break

            if adj_to_sym:
                tot += int(num)

            adj_to_sym = False
            num = ""
            c += 1

    return tot


def process_d3_p2(data: TextIOWrapper) -> int:
    matrix = [line.strip() for line in data.readlines()]

    def get_num_from_pos(r: int, c: int) -> tuple[int, int, int]:
        i, j = c - 1, c + 1
        num = matrix[r][c]
        stop_i, stop_j = False, False
        while True:
            if not stop_i:
                try:
                    if (n := matrix[r][i]).isnumeric():
                        num = n + num
                        i -= 1
                    else:
                        stop_i = True
                except IndexError:
                    stop_i = True

            if not stop_j:
                try:
                    if (n := matrix[r][j]).isnumeric():
                        num += n
                        j += 1
                    else:
                        stop_j = True
                except IndexError:
                    stop_j = True

            if stop_i and stop_j:
                break

        return int(num), i, j

    def get_ratio(r: int, c: int) -> int:
        cycle = [
            [0, -1],  # l
            [-1, -1],  # tl
            [-1, 0],  # tm
            [-1, 1],  # tr
            [1, -1],  # bl
            [1, 0],  # bm
            [1, 1],  # br
            [0, 1],  # r
        ]

        nums = []
        ps = {}

        for offset in cycle:
            try:
                new_r, new_c = r + offset[0], c + offset[1]
                if any(
                    new_c in range(start, stop + 1)
                    for start, stop in ps.get(new_r, set())
                ):
                    continue

                sym = matrix[new_r][new_c]
                if sym.isnumeric():
                    num, start, stop = get_num_from_pos(new_r, new_c)
                    if len(nums) == 2:
                        return 0  # exit early if we find more than 2

                    ps.setdefault(new_r, set()).add((start, stop))
                    nums.append(num)
            except IndexError:
                continue

        if len(nums) == 2:
            return nums[0] * nums[1]

        return 0

    return sum(
        get_ratio(r, c)
        for r in range(len(matrix))
        for c in range(len(matrix[r]))
        if matrix[r][c] == "*"
    )


def get_processor(day: int, part: int) -> Callable[[TextIOWrapper], int]:
    match day, part:
        case 1, 1:
            return process_d1_p1
        case 1, 2:
            return process_d1_p2
        case 2, 1:
            return process_d2_p1
        case 2, 2:
            return process_d2_p2
        case 3, 1:
            return process_d3_p1
        case 3, 2:
            return process_d3_p2
        case _:
            raise Exception(f"Unknown day:part pair {day=} {part=}")
