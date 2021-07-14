type Maybe = Just(value: integer)
           | Nothing

procedure ifJustThenFive(m: Maybe)
    case m of {
        Just:
            m.value := 5
        default nothing
    }

procedure ifJustThenPrint(m: Maybe)
    case m of {
        Just:
            writeln(m.value)
        default nothing
    }

program Main
    var maybe: Maybe

    // instantiate the value of `maybe` to Just(value = 1111)
    maybe <- Just(1111)

    ifJustThenPrint(maybe)

    // procedure that mutates the value of `maybe`
    ifJustThenFive(maybe)

    ifJustThenPrint(maybe)

