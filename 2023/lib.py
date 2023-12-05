import re
from collections import defaultdict
from io import TextIOWrapper
from typing import Callable

DIGIT = re.compile(r"\d")
DIGITW = re.compile(r"\d+")
ADJS = [
    [-1, -1],  # tl
    [-1, 0],  # tm
    [-1, 1],  # tr
    [0, 1],  # r
    [1, 1],  # br
    [1, 0],  # bm
    [1, -1],  # bl
    [0, -1],  # l
]


def load(day: int) -> TextIOWrapper:
    return open(f"./inputs/day_{day}.txt", encoding="utf-8")


def first_and_last[T](xs: list[T]) -> tuple[T, T]:
    return xs[0], xs[-1]


def process_d1_p1(data: TextIOWrapper) -> int:
    return sum(
        int("".join(first_and_last(DIGIT.findall(line)))) for line in data.readlines()
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
        int("".join(first_and_last(DIGIT.findall(line)))) for line in clean_lines
    )


def process_d2_p1(data: TextIOWrapper) -> int:
    CUBES = {
        "red": 12,
        "green": 13,
        "blue": 14,
    }

    def is_possible(words: list[str]) -> bool:
        return all(
            int(words[i]) <= CUBES[words[i + 1]] for i in range(0, len(words), 2)
        )

    return sum(
        int(line.split(":")[0].split(" ")[1])
        for line in data.readlines()
        if is_possible(
            line.split(":")[1].strip().replace(",", "").replace(";", "").split(" ")
        )
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

        return maxes["blue"] * maxes["green"] * maxes["red"]

    return sum(
        make_power(
            line.split(":")[1].strip().replace(",", "").replace(";", "").split(" ")
        )
        for line in data.readlines()
    )


def process_d3_p1(data: TextIOWrapper) -> int:
    matrix = [line.strip() for line in data.readlines()]

    def check_adj(r: int, c: int) -> bool:
        return any(
            r + r_off < len(matrix)
            and c + c_off < len(matrix[r + r_off])
            and not matrix[r + r_off][c + c_off].isnumeric()
            and matrix[r + r_off][c + c_off] != "."
            for (r_off, c_off) in ADJS
        )

    tot = 0
    for r, row in enumerate(matrix):
        c = 0
        num = ""
        adj_to_sym = False
        while c < len(row):
            if not row[c].isnumeric():
                c += 1
                continue

            while (char := row[c]).isnumeric():
                num += char
                if check_adj(r, c):
                    adj_to_sym = True

                if (next := c + 1) < len(row):
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

    def get_num_from_pos(row: str, c: int) -> tuple[int, int, int]:
        i, j = c - 1, c + 1
        num = row[c]
        while i >= 0 and (n := row[i]).isnumeric():
            num = n + num
            i -= 1

        while j < len(row) and (n := row[j]).isnumeric():
            num += n
            j += 1

        return int(num), i, j

    def get_ratio(r: int, c: int) -> int:
        nums = []
        ps = {}

        for offset in ADJS:
            new_r, new_c = r + offset[0], c + offset[1]
            if (
                new_r > len(matrix)
                or new_c > len(matrix[new_r])
                or not matrix[new_r][new_c].isnumeric()
                or any(
                    new_c in range(start, stop + 1)
                    for start, stop in ps.get(new_r, set())
                )
            ):
                continue

            num, start, stop = get_num_from_pos(matrix[new_r], new_c)
            ps.setdefault(new_r, set()).add((start, stop))
            nums.append(num)

        if len(nums) != 2:
            return 0

        return nums[0] * nums[1]

    return sum(
        get_ratio(r, c)
        for r in range(len(matrix))
        for c in range(len(matrix[r]))
        if matrix[r][c] == "*"
    )


def process_d4_p1(data: TextIOWrapper) -> int:
    return sum(
        pow(2, matches - 1)
        if (
            matches := len(
                set(
                    DIGITW.findall(line.split(":")[1].strip().split("|")[0])
                ).intersection(
                    set(DIGITW.findall(line.split(":")[1].strip().split("|")[1]))
                )
            )
        )
        >= 1
        else 0
        for line in data.readlines()
    )


def process_d4_p2(data: TextIOWrapper) -> int:
    original = list(map(lambda line: line.split(":")[1].strip(), data.readlines()))
    copies = defaultdict(int)

    for i, line in enumerate(original):
        want, have = line.split("|")
        matches = len(set(DIGITW.findall(want)).intersection(set(DIGITW.findall(have))))
        for card in range(i + 2, i + 2 + matches):
            copies[card] += 1 + (1 * copies.get(i + 1, 0))

    return sum(copies.values()) + len(original)


def process_d5_p1(data: TextIOWrapper) -> int:
    alamanac = data.read().split("\n\n")
    seeds = alamanac[0].split(":")[1].strip().split(" ")

    maps = []

    for section in alamanac[1:]:
        mappings = section.split("\n")[1:]
        m = {}
        for mapping in mappings:
            d_start, s_start, length = mapping.split(" ")

        maps.append(section.split("\n")[1:])

    # print(alamanac)
    print(seeds)
    print(maps)


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
        case 4, 1:
            return process_d4_p1
        case 4, 2:
            return process_d4_p2
        case 5, 1:
            return process_d5_p1
        case _:
            raise Exception(f"Unknown day:part pair {day=} {part=}")
