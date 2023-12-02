export const load = (day: number) =>
  Deno.readTextFileSync(`./inputs/day_${day}.txt`);

type ProcessorFunc = (data: string) => number;

const DIGIT = RegExp("\\d", "g");

function firstAndLast<T>(xs: T[]): [T, T] {
  return [xs.at(0) as T, xs.at(-1) as T];
}

const processD1P1 = (data: string): number => {
  return data.trim().split("\n").map((line) =>
    Number(firstAndLast([...line.matchAll(DIGIT)]).join(""))
  ).reduce((n, a) => n + a, 0);
};

const processD1P2 = (data: string): number => {
  const clean = data
    .replaceAll("one", "o1e")
    .replaceAll("two", "t2o")
    .replaceAll("three", "t3e")
    .replaceAll("four", "f4r")
    .replaceAll("five", "f5e")
    .replaceAll("six", "s6x")
    .replaceAll("seven", "s7n")
    .replaceAll("eight", "e8t")
    .replaceAll("nine", "n9e")
    .trim().split("\n");

  return clean.map((line) =>
    Number(firstAndLast([...line.matchAll(DIGIT)]).join(""))
  ).reduce((n, a) => n + a, 0);
};

export const getProcessor = (day: number, part: number): ProcessorFunc => {
  if (day === 1 && part === 1) {
    return processD1P1;
  }

  if (day === 1 && part === 2) {
    return processD1P2;
  }

  throw Error(`Unsupported day=${day} or part=${part}`);
};
