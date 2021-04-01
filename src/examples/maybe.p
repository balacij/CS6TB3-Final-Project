type Maybe = Just(value: integer)
           | Nothing

procedure valOr(v: Maybe, n: integer) -> (r: integer)
    case v of {
        Just:
            r := v.value
        Nothing:
            r := n
    }

program Main
    var maybe: Maybe

    var x: integer

    maybe <- Nothing()
    maybe <- Just(1111)

    case maybe of {
        Just: 
            x := maybe.value
            maybe.value := 100
            writeln(maybe.value)
            writeln(x)
        Nothing: x := 1000
    }
