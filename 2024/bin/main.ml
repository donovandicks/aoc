let re = Str.regexp "   "

let split_line (line: string): string list = Str.split re line

let read_data (file: string) : string =
  let in_chan = open_in file in
  try
    let contents = really_input_string in_chan (in_channel_length in_chan) in
    close_in in_chan;
    String.trim contents
  with e ->
    close_in_noerr in_chan; (* Still close channel in case error *)
    raise e

let d1_get_lists (data: string): int =
  let left, right = String.split_on_char '\n' data
  |> List.map split_line
  |> List.fold_left (
    fun (left, right) sublist ->
      match sublist with
      | [x; y] -> (int_of_string x :: left, int_of_string y :: right)
      | _ -> failwith "incorrect sublist length")
    ([], []) in

  let sorted_right = List.sort compare right in

  left
  |> List.sort compare
  |> List.mapi
    (fun i x -> (Int.abs(x - List.nth sorted_right i)))
  |> List.fold_left ( + ) 0

let () = 
  let day = ref 1 in
  let part = ref 1 in

  let speclist = [
    ("--day", Arg.Set_int day, "AoC Day");
    ("--part", Arg.Set_int part, "AoC Part");
  ] in

  Arg.parse speclist (fun _ -> ()) "Usage: aoc [--day day] [--part part]";

  Printf.sprintf "./inputs/d%dp%d.txt" !day !part
  |> read_data
  |> d1_get_lists
  |> string_of_int
  |> print_endline
