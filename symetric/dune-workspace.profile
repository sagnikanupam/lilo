(lang dune 2.9)

(context default)

(context 
  (default 
    (name profiling-auto)
    (instrument_with landmarks) 
    (env 
      (_ (env-vars ("OCAML_LANDMARKS" "auto")))
    )
  )
)
