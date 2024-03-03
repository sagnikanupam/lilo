(* Libraries Needed *)
open Core
open Poly
open Pars
open Str

(* Custom .ml files needed *)
open Type

type program =
  | Index of int
  | Abstraction of program
  | Apply of program*program
  | Primitive of tp * string * (unit ref)
  | Invented of tp * program

let tfullstr = make_ground "tfullstr";;
let tsubstr = make_ground "tsubstr";;

let primitive_rdot = primitive "_rdot" tsubstr ".";;
let primitive_emptystr = primitive "_rempty" tsubstr "";;
let primitive_rnot = primitive "_rnot" (tsubstr @> tsubstr) (fun s -> "[^" ^ s ^ "]");;

let primitive_ror = primitive "_ror" (tsubstr @> tsubstr @> tsubstr) (fun s1 s2 -> "(("^ s1 ^ ")|("^ s2 ^"))");;

let primitive_rconcat = primitive "_rconcat" (tsubstr @> tsubstr @> tsubstr) (fun s1 s2 -> s1 ^ s2);;
et primitive_rmatch = primitive "_rmatch" (tsubstr @> tsubstr @> tboolean) (fun s1 s2 ->
  try
    let regex = Re2.create_exn ("^" ^ s1 ^ "$") in
    Re2.matches regex s2
  with _ -> false
  );;

(** Flattens list of substrings back into a string *)
let primitive_rflatten = primitive "_rflatten" ((tlist tsubstr) @> tfullstr) (fun l -> String.concat ~sep:"" l);;
let primitive_rtail = primitive "_rtail" ((tlist tsubstr) @> tsubstr) (fun l ->
  let arr = Array.of_list l in arr.(Array.length arr - 1)
  );;

(** Splits s2 on regex s1 as delimiter, including the matches *)
let not_empty str = (String.length str) > 0;;
let primitive_rsplit = primitive "_rsplit" (tsubstr @> tfullstr @> (tlist tsubstr)) (fun s1 s2 ->
  try
    let regex = Re2.create_exn s1 in
    let init_split = Re2.split ~include_matches:true regex s2 in
    (List.filter init_split not_empty)
  with _ -> [s2]
  );;

let primitive_rappend = primitive "_rappend" (tsubstr @> (tlist tsubstr) @> (tlist tsubstr)) (fun x l -> l @ [x]);;
let primitive_rrevcdr = primitive "_rrevcdr" ((tlist tsubstr) @> (tlist tsubstr)) (fun l ->
  let arr = Array.of_list l in
  let slice = Array.sub arr 0 (Array.length arr - 1) in
  Array.to_list slice
  );;

let primitive_if = primitive "if" (tboolean @> t0 @> t0 @> t0)
  ~manualLaziness:true
  (fun p x y -> if Lazy.force p then Lazy.force x else Lazy.force y);;

let primitive_cons = primitive "cons" (t0 @> tlist t0 @> tlist t0) (fun x xs -> x :: xs);;
let primitive_car = primitive "car" (tlist t0 @> t0) (fun xs -> List.hd_exn xs);;
let primitive_cdr = primitive "cdr" (tlist t0 @> tlist t0) (fun xs -> List.tl_exn xs);;

let primitive_map = primitive "map" ((t0 @> t1) @> (tlist t0) @> (tlist t1)) (fun f l -> List.map ~f:f l);;
(* Constants *)
let primitive_ra = primitive "_a" tsubstr "a";;
let primitive_rb = primitive "_b" tsubstr "b";;
let primitive_rc = primitive "_c" tsubstr "c";;
let primitive_rd = primitive "_d" tsubstr "d";;
let primitive_re = primitive "_e" tsubstr "e";;
let primitive_rf = primitive "_f" tsubstr "f";;
let primitive_rg = primitive "_g" tsubstr "g";;
let primitive_rh = primitive "_h" tsubstr "h";;
let primitive_ri = primitive "_i" tsubstr "i";;
let primitive_rj = primitive "_j" tsubstr "j";;
let primitive_rk = primitive "_k" tsubstr "k";;
let primitive_rl = primitive "_l" tsubstr "l";;
let primitive_rm = primitive "_m" tsubstr "m";;
let primitive_rn = primitive "_n" tsubstr "n";;
let primitive_ro = primitive "_o" tsubstr "o";;
let primitive_rp = primitive "_p" tsubstr "p";;
let primitive_rq = primitive "_q" tsubstr "q";;
let primitive_rr = primitive "_r" tsubstr "r";;
let primitive_rs = primitive "_s" tsubstr "s";;
let primitive_rt = primitive "_t" tsubstr "t";;
let primitive_ru = primitive "_u" tsubstr "u";;
let primitive_rv = primitive "_v" tsubstr "v";;
let primitive_rw = primitive "_w" tsubstr "w";;
let primitive_rx = primitive "_x" tsubstr "x";;
let primitive_ry = primitive "_y" tsubstr "y";;
let primitive_rz = primitive "_z" tsubstr "z";;

