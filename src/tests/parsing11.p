type Maybe = Just(value: integer) | Nothing

program Main
    var m: Maybe
    m := Just(20)
    
    case m of {}
        nil: writeln(1)
        Just: writeln(m.value)
    }
