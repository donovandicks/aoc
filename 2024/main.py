import argparse
from typing import Callable, Counter


def d1_get_lists(data: str) -> tuple[list[int], list[int]]:
    left, right = [], []

    for line in data.split("\n"):
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


registry: dict[str, Callable[[str], int]] = {
    "d1p1": d1p1,
    "d1p2": d1p2,
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
