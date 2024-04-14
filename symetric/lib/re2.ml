(* Libraries Needed *)
open Core
open Re2
open Str
open Std
module P = Program

(*
(* Custom .ml files needed *)
type tp =
  | TID of int
  | TCon of string * tp list * bool

let make_ground g = TCon(g,[],false);;

type program =
  | Index of int
  | Abstraction of program
  | Apply of program*program
  | Primitive of tp * string * (unit ref)
  | Invented of tp * program

type program =
  | Index of int
  | Abstraction of program
  | Apply of program*program
  | Primitive of tp * string * (unit ref)
  | Invented of tp * program

let tfullstr = make_ground "tfullstr";;
let tsubstr = make_ground "tsubstr";; *)

let primitive_rdot = ".";;
let primitive_emptystr = "";;
let primitive_rnot = (fun s -> "[^" ^ s ^ "]");;

let primitive_rvowel = "(a|e|i|o|u)" ;;
let primitive_rconsonant = "[^aeiou]" ;;

let primitive_ror = (fun s1 s2 -> "(("^ s1 ^ ")|("^ s2 ^"))");;

let primitive_rconcat = (fun s1 s2 -> s1 ^ s2);;
let primitive_rmatch = (fun s1 s2 ->
  try
    let regex = Re2.create_exn ("^" ^ s1 ^ "$") in
    Re2.matches regex s2
  with _ -> false
  );;

(** Flattens list of substrings back into a string *)
let primitive_rflatten = (fun l -> String.concat ~sep:"" l);;
let primitive_rtail = (fun l ->
  let arr = Array.of_list l in arr.(Array.length arr - 1)
  );;

(** Splits s2 on regex s1 as delimiter, including the matches *)
let not_empty str = (String.length str) > 0;;
let primitive_rsplit = (fun s1 s2 ->
  try
    let regex = Re2.create_exn s1 in
    let init_split = Re2.split ~include_matches:true regex s2 in
    (List.filter init_split not_empty)
  with _ -> [s2]
  );;

let primitive_rappend = (fun x l -> l @ [x]);;
let primitive_rrevcdr = (fun l ->
  let arr = Array.of_list l in
  let slice = Array.sub arr 0 (Array.length arr - 1) in
  Array.to_list slice
  );;

let primitive_if = (fun p x y -> if Lazy.force p then Lazy.force x else Lazy.force y);;

let primitive_cons = (fun x xs -> x :: xs);;
let primitive_car = (fun xs -> List.hd_exn xs);;
let primitive_cdr = (fun xs -> List.tl_exn xs);;

let primitive_map = (fun f l -> List.map ~f:f l);;
(* Constants *)
let primitive_ra = "a";;
let primitive_rb = "b";;
let primitive_rc = "c";;
let primitive_rd = "d";;
let primitive_re = "e";;
let primitive_rf = "f";;
let primitive_rg = "g";;
let primitive_rh = "h";;
let primitive_ri = "i";;
let primitive_rj = "j";;
let primitive_rk = "k";;
let primitive_rl = "l";;
let primitive_rm = "m";;
let primitive_rn = "n";;
let primitive_ro = "o";;
let primitive_rp = "p";;
let primitive_rq = "q";;
let primitive_rr = "r";;
let primitive_rs = "s";;
let primitive_rt = "t";;
let primitive_ru = "u";;
let primitive_rv = "v";;
let primitive_rw = "w";;
let primitive_rx = "x";;
let primitive_ry = "y";;
let primitive_rz = "z";;

module Type = struct
  type t = String | StringList | Boolean [@@deriving compare, equal, hash, sexp, yojson]
  let default = String
  let output = Boolean
  let pp fmt x = Sexp.pp fmt @@ [%sexp_of: t] x  
end

module Op = struct
  (* Types of Operations *)
  type t =
  | Rdot
  | Emptystr
  | Rvowel
  | Rconsonant 
  | Rnot 
  | Ror
  | Rconcat
  | Rmatch
  | Rflatten
  | Rtail
  | Rsplit
  | Rappend
  | Rrevcdr
  | If
  | Cons
  | Car
  | Cdr
  | Map
  | Ch of char
[@@deriving compare, equal, hash, sexp, yojson]

let default = Ch ('a')
let cost _ = 1

let ret_type : _ -> Type.t = function
  | Rmatch -> Boolean
  | Rappend | Rrevcdr | Rsplit | Cons | Cdr -> StringList
  | _ -> String

  (* Everything below this is copied from Tower *)
let args_type : _ -> Type.t list = function
  | Embed -> [ Tower ]
  | Seq -> [ Tower; Tower ]
  | Move_s _ -> [ Tower ]
  | Move_p _ -> [ Tower ]
  | Loop -> [ Int; Tower ]
  | Drop_v | Drop_h | Int _ -> []
  | _ -> assert false

let arity op = List.length @@ args_type op
let is_commutative _ = false
let pp fmt x = Sexp.pp_hum fmt @@ [%sexp_of: t] x
end

module Value = struct
  
end

