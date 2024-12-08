import argparse
import itertools
import re
from collections import defaultdict
from functools import cmp_to_key, partial, reduce
from operator import mul
from typing import Callable, Counter, TypeAlias

Solution: TypeAlias = Callable[[str], int]

# DAY 1


def sum_diffs(ls: list[int], rs: list[int]) -> int:
    return sum(abs(ls[i] - rs[i]) for i in range(len(ls)))


def mul_counts(ls: list[int], rs: list[int]) -> int:
    counter = Counter(rs)
    return sum(l * counter.get(l, 0) for l in ls)


def d1(data: str, func: Callable[[list[int], list[int]], int]) -> int:
    return func(
        *[
            sorted(ls)
            for ls in [
                list(tup)
                for tup in zip(
                    *(
                        tuple(int(i) for i in line.split("   "))
                        for line in data.splitlines()
                    )
                )
            ]
        ]
    )


# DAY 2

neg_diffs = {-1, -2, -3}
pos_diffs = {1, 2, 3}


def is_safe(line: list[int]) -> bool:
    diffs = set([b - a for a, b in itertools.pairwise(line)])
    return diffs.issubset(neg_diffs) or diffs.issubset(pos_diffs)


def could_be_safe(line: list[int]) -> bool:
    return any(is_safe(line[:i] + line[i + 1 :]) for i in range(len(line)))


def d2(data: str, func: Callable[[list[int]], bool]) -> int:
    return len(
        list(
            filter(
                func,
                [[int(i) for i in line.split(" ")] for line in data.splitlines()],
            )
        )
    )


# DAY 3

pattern = r"(do\(\)|don\'t\(\)|mul\((\d{1,3},\d{1,3})\))"


def d3(data: str, check_do: bool) -> int:
    do, sum = True, 0
    for group, val in re.compile(pattern, re.MULTILINE).findall(data):
        if check_do:
            do = True if group == "do()" else False if group == "don't()" else do

        if group.startswith("m") and do:
            sum += reduce(mul, [int(i) for i in val.split(",")])

    return sum


# DAY 4

dirs = [
    (0, 1),  # up
    (1, 1),  # up right
    (1, 0),  # right
    (1, -1),  # down right
    (0, -1),  # down
    (-1, -1),  # down left
    (-1, 0),  # left
    (-1, 1),  # up left
]

diags = {
    "ur": (1, 1),  # up right
    "dl": (-1, -1),  # down left
    "ul": (-1, 1),  # up left
    "dr": (1, -1),  # down right
}

word = "XMAS"
maso = ord("M") * 2 + ord("S") * 2


def find_xmas(
    word_search: list[str],
    check_bounds: Callable[[int, int], bool],
    pos: tuple[int, int],
) -> int:
    def check_match(dir: tuple[int, int]) -> bool:
        for i in range(len(word)):
            x, y = (pos[0] + dir[0] * i, pos[1] + dir[1] * i)
            if not check_bounds(x, y):
                return False

            if word_search[x][y] != word[i]:
                return False

        return True

    return sum(1 for dir in dirs if check_match(dir))


def find_mas(
    word_search: list[str],
    check_bounds: Callable[[int, int], bool],
    pos: tuple[int, int],
) -> int:
    if word_search[pos[0]][pos[1]] != "A":
        return 0

    counter = {"ur": "", "dl": "", "ul": "", "dr": ""}
    for name, dir in diags.items():
        x, y = (pos[0] + dir[0], pos[1] + dir[1])
        if not check_bounds(x, y):
            return 0

        char = word_search[x][y]
        if char not in ["M", "S"]:
            return 0

        counter[name] = char

    if (
        counter["ur"] != counter["dl"]
        and counter["ul"] != counter["dr"]
        and sum(ord(c) for c in counter.values()) == maso
    ):
        return 1

    return 0


def d4(
    data: str,
    func: Callable[
        [
            list[str],
            Callable[[int, int], bool],
            tuple[int, int],
        ],
        int,
    ],
) -> int:
    count = 0
    word_search = data.splitlines()
    nrows, ncols = len(word_search), len(word_search[0])

    def check_bounds(r: int, c: int) -> bool:
        return (r >= 0 and r < nrows) and (c >= 0 and c < ncols)

    for r in range(nrows):
        for c in range(ncols):
            count += func(word_search, check_bounds, (r, c))

    return count


# DAY 5


def make_rules_and_updates(
    data: str,
) -> tuple[defaultdict[str, set[str]], list[list[str]]]:
    rules = defaultdict(set)

    updates: list[list[str]] = []
    for line in data.splitlines():
        if line in ["\n", ""]:
            continue

        if "|" in line:
            x, y = line.split("|")
            rules[x].add(y)
            continue

        updates.append(line.split(","))

    return rules, updates


def count_correct(rules: defaultdict[str, set[str]], updates: list[list[str]]) -> int:
    return sum(
        int(update[len(update) // 2])
        for update in updates
        if all(
            not set(update[:i]).intersection(rules.get(num, set()))
            for i, num in enumerate(update)
        )
    )


def fix_and_count_incorrect(
    rules: defaultdict[str, set[str]], updates: list[list[str]]
) -> int:
    incorrect: list[list[str]] = []
    for update in updates:
        if any(
            set(update[:i]).intersection(rules.get(num, set()))
            for i, num in enumerate(update)
        ):
            incorrect.append(update)

    ruleset = set()
    for x, ys in rules.items():
        for y in ys:
            ruleset.add((x, y))

    def sort_(a: str, b: str) -> int:
        if (a, b) in ruleset:
            return -1
        elif (b, a) in ruleset:
            return 1
        else:
            return 0

    for update in incorrect:
        update.sort(key=cmp_to_key(sort_))

    return sum(int(update[len(update) // 2]) for update in incorrect)


def d5(
    data: str, func: Callable[[defaultdict[str, set[str]], list[list[str]]], int]
) -> int:
    rules, updates = make_rules_and_updates(data)
    return func(rules, updates)


# END

registry: dict[str, Solution] = {
    "d1p1": partial(d1, func=sum_diffs),
    "d1p2": partial(d1, func=mul_counts),
    "d2p1": partial(d2, func=is_safe),
    "d2p2": partial(d2, func=could_be_safe),
    "d3p1": partial(d3, check_do=False),
    "d3p2": partial(d3, check_do=True),
    "d4p1": partial(d4, func=find_xmas),
    "d4p2": partial(d4, func=find_mas),
    "d5p1": partial(d5, func=count_correct),
    "d5p2": partial(d5, func=fix_and_count_incorrect),
}


def load_data(problem: str) -> str:
    """Load problem input data.

    Expects to be called from the parent directory.
    """
    with open(f"./2024/inputs/{problem}.txt") as f:
        return f.read().strip()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--day", default=1, type=int)
    parser.add_argument("--part", default=1, type=int)

    args = parser.parse_args()
    problem = f"d{args.day}p{args.part}"

    print(registry[problem](load_data(f"d{args.day}")))
