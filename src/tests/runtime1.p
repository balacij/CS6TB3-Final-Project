type Maybe = Just(value: integer) | Nothing

procedure changeValIfJust(m: Maybe, value: integer)
    case m of {
        Just:
            m.value := value
        default nothing
    }

program Main
    var m: Maybe
    m := Just(20)

    changeValIfJust(m, 10000)
    
    case m of {
        nil: writeln(1)
        Just: writeln(m.value)
        default nothing
    }
