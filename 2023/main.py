from io import TextIOWrapper
from typing import Callable
import re
import sys

DIGIT = re.compile(r"\d")


def load(day: int) -> TextIOWrapper:
    return open(f"./inputs/day_{day}.txt", encoding="utf-8")


def find_at(regex: re.Pattern, target: str, pos: int) -> str:
    return regex.findall(target)[pos]


def process_day_1(data: TextIOWrapper):
    tot = sum(
        [
            int(f"{find_at(DIGIT, line, 0)}{find_at(DIGIT, line, -1)}")
            for line in data.readlines()
        ]
    )

    print(f"Answer: {tot}")


def get_processor(day: int) -> Callable:
    match day:
        case 1:
            return process_day_1
        case _:
            raise


def main(day: int):
    data = load(day)
    proc = get_processor(day)

    proc(data)

    data.close()


if __name__ == "__main__":
    day = int(sys.argv[1])
    main(day)
