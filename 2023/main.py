import sys
from lib import load, get_processor


def main(day: int, part: int):
    data = load(day)
    proc = get_processor(day, part)

    ans = proc(data)

    print(f"Answer: {ans}")

    data.close()


if __name__ == "__main__":
    day = int(sys.argv[1])
    part = int(sys.argv[2])
    main(day, part)
