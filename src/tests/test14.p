type Maybe = Just(value: integer) | Nothing

program Main
    var m: Maybe
    m := Nothing()
    
    case m of {
        nil: writeln(1)
        Just: writeln(m.value)
        default nothing
    }