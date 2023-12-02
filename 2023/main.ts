const load = (day: number) => Deno.readTextFileSync(`./inputs/day_${day}.txt`);

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

const getProcessor = (day: number, part: number): ProcessorFunc => {
  if (day === 1 && part === 1) {
    return processD1P1;
  }

  throw Error(`Unsupported day=${day} or part=${part}`);
};

const main = (day: number, part: number) => {
  const data = load(day);
  const func = getProcessor(day, part);

  const ans = func(data);

  console.log(`Answer: ${ans}`);
};

if (import.meta.main) {
  const [day, part] = Deno.args;
  console.log(`Processing day ${day} part ${part}`);
  main(Number(day), Number(part));
}
