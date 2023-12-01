from io import TextIOWrapper
from typing import Callable
import re
import sys

DIGIT = re.compile(r"\d")


def load(day: int) -> TextIOWrapper:
    return open(f"./inputs/day_{day}.txt", encoding="utf-8")


def find_at(regex: re.Pattern, target: str, pos: int) -> str:
    return regex.findall(target)[pos]


def process_d1_p1(data: TextIOWrapper):
    tot = sum(
        [
            int(f"{find_at(DIGIT, line, 0)}{find_at(DIGIT, line, -1)}")
            for line in data.readlines()
        ]
    )

    print(f"Answer: {tot}")


def process_d1_p2(data: TextIOWrapper):
    clean = (
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
    )

    tot = sum(
        [
            int(f"{find_at(DIGIT, line, 0)}{find_at(DIGIT, line, -1)}")
            for line in clean.split("\n")
            if line != ""
        ]
    )

    print(f"Answer: {tot}")


def get_processor(day: int, part: int) -> Callable:
    match day, part:
        case 1, 1:
            return process_d1_p1
        case 1, 2:
            return process_d1_p2
        case _:
            raise


def main(day: int, part: int):
    data = load(day)
    proc = get_processor(day, part)

    proc(data)

    data.close()


if __name__ == "__main__":
    day = int(sys.argv[1])
    part = int(sys.argv[2])
    main(day, part)
