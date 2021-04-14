type Maybe = Just(value: integer)
           | Nothing

procedure valOr(v: Maybe, n: integer) → (r: integer)
    case v of {
        Just:
            r := v.value
        default:
            r := n
    }

program Main
    var maybe: Maybe

    maybe <- Nothing()
    writeln(valOr(maybe, -1))

    maybe <- Just(1111)
    writeln(valOr(maybe, 0))
