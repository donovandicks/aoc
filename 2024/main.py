import argparse
import itertools
import re
from functools import partial, reduce
from operator import mul
from typing import Callable, Counter, TypeAlias

Solution: TypeAlias = Callable[[str], int]

# DAY 1


def d1_get_lists(data: str) -> tuple[list[int], list[int]]:
    left, right = [], []

    for line in data.splitlines():
        ln, rn = line.split("   ")
        left.append(int(ln))
        right.append(int(rn))

    return left, right


def d1p1(data: str) -> int:
    left, right = d1_get_lists(data)
    ls, rs = sorted(left), sorted(right)
    return sum(abs(ls[i] - rs[i]) for i in range(len(left)))


def d1p2(data: str) -> int:
    left, right = d1_get_lists(data)
    right_counts = Counter(right)
    return sum(l * right_counts.get(l, 0) for l in left)


# DAY 2

neg_diffs = {-1, -2, -3}
pos_diffs = {1, 2, 3}


def is_safe(line: list[int]) -> bool:
    diffs = set([b - a for a, b in itertools.pairwise(line)])
    return diffs.issubset(neg_diffs) or diffs.issubset(pos_diffs)


def could_be_safe(line: list[int]) -> bool:
    return any(is_safe(line[:i] + line[i + 1 :]) for i in range(len(line)))


def d2(data: str, check_could: bool) -> int:
    return len(
        list(
            filter(
                could_be_safe if check_could else is_safe,
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


# END

registry: dict[str, Solution] = {
    "d1p1": d1p1,
    "d1p2": d1p2,
    "d2p1": partial(d2, check_could=False),
    "d2p2": partial(d2, check_could=True),
    "d3p1": partial(d3, check_do=False),
    "d3p2": partial(d3, check_do=True),
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
