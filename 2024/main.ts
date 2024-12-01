import { parseArgs } from "jsr:@std/cli/parse-args";

const d1GetLists = (data: string): [number[], number[]] => {
  const [l, r]: [number[], number[]] = [[], []];

  data.split("\n").map((line) => {
    const [ln, rn] = line.split("   ");
    l.push(Number(ln));
    r.push(Number(rn));
  });

  return [l, r];
};

function d1p1(data: string): number {
  const [left, right] = d1GetLists(data);
  const [ls, rs] = [left.toSorted(), right.toSorted()];
  return ls.map((l, i) => Math.abs(l - rs[i])).reduce((acc, n) => acc + n, 0);
}

const makeCounter = (data: number[]): Map<number, number> => {
  const counter = new Map();

  for (const n of data) {
    counter.set(n, (counter.get(n) || 0) + 1);
  }

  return counter;
};

function d1p2(data: string): number {
  const [left, right] = d1GetLists(data);
  const rightCounts = makeCounter(right);
  return left
    .map((l) => l * (rightCounts.get(l) || 0))
    .reduce((acc, n) => acc + n, 0);
}

type ProblemName = `d${1 | 2}p${1 | 2}`;

type Solution = (data: string) => number;

const Registry: Map<ProblemName, Solution> = new Map([
  ["d1p1", d1p1],
  ["d1p2", d1p2],
]);

async function loadData(problem: string): Promise<string> {
  const decoder = new TextDecoder("utf-8");
  return decoder
    .decode(await Deno.readFile(`./2024/inputs/${problem}.txt`))
    .trim();
}

if (import.meta.main) {
  const flags = parseArgs(Deno.args, {
    default: { day: 1, part: 1 },
  });
  const problem: ProblemName = `d${flags.day}p${flags.part}`;

  console.log(Registry.get(problem)!(await loadData(problem)));
}
