import argparse
import itertools
from typing import Callable, Counter, TypeAlias

Solution: TypeAlias = Callable[[str], int]


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


def is_safe(line: list[int]) -> bool:
    """Line is strictly ordered and all diffs are within [1, 3]"""
    return ((sorted(line) == line) or (sorted(line, reverse=True) == line)) and all(
        (1 <= abs(a - b) <= 3) for a, b in itertools.pairwise(line)
    )


def d2p1(data: str) -> int:
    return len(
        list(
            filter(
                is_safe,
                [[int(i) for i in line.split(" ")] for line in data.splitlines()],
            )
        )
    )


def d2p2(data: str) -> int:
    pass


registry: dict[str, Solution] = {
    "d1p1": d1p1,
    "d1p2": d1p2,
    "d2p1": d2p1,
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

    print(registry[problem](load_data(problem)))
