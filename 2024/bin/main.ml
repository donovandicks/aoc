let read_data (file: string) : string =
  let in_chan = open_in file in
  try
    let contents = really_input_string in_chan (in_channel_length in_chan) in
    close_in in_chan;
    String.trim contents
  with e ->
    close_in_noerr in_chan; (* Still close channel in case error *)
    raise e

let re = Str.regexp "   "

let split_line (line: string): string list =
  Str.split re line

let d1_get_lists (data: string): int =
  let left, right = String.split_on_char '\n' data
  |> List.map split_line
  |> List.fold_left (
    fun (left, right) sublist ->
      match sublist with
      | [x; y] -> (int_of_string x :: left, int_of_string y :: right)
      | _ -> failwith "incorrect sublist length")
    ([], []) in

  let sorted_left = List.sort compare left in
  let sorted_right = List.sort compare right in

  List.mapi
    (fun i x -> (Int.abs(x - List.nth sorted_right i)))
    sorted_left
  |> List.fold_left ( + ) 0

let () = read_data "./inputs/d1p1.txt"
  |> d1_get_lists
  |> string_of_int
  |> print_endline
