from io import TextIOWrapper
from functools import reduce
from typing import Callable
import re

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
        case _:
            raise
