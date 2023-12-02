import { getProcessor, load } from "./lib.ts";

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
