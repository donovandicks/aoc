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


neg_diffs = {-1, -2, -3}
pos_diffs = {1, 2, 3}


def is_safe(line: list[int]) -> bool:
    diffs = set([b - a for a, b in itertools.pairwise(line)])
    return diffs.issubset(neg_diffs) or diffs.issubset(pos_diffs)


def d2p1(data: str) -> int:
    return len(
        list(
            filter(
                is_safe,
                [[int(i) for i in line.split(" ")] for line in data.splitlines()],
            )
        )
    )


def could_be_safe(line: list[int]) -> bool:
    return any(is_safe(line[:i] + line[i + 1 :]) for i in range(len(line)))


def d2p2(data: str) -> int:
    return len(
        list(
            filter(
                could_be_safe,
                [[int(i) for i in line.split(" ")] for line in data.splitlines()],
            )
        )
    )


registry: dict[str, Solution] = {
    "d1p1": d1p1,
    "d1p2": d1p2,
    "d2p1": d2p1,
    "d2p2": d2p2,
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
