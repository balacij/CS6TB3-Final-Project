type Maybe = Just(value: integer)
           | Nothing


var m: Maybe

procedure doubleJusts(may: Maybe)
    case may of {
        Just: 
            may.value := may.value * 2

        default nothing
    }

program Main
    m <- Just(32)

    m <- Nothing()
    
    m <- Just(22)

    doubleJusts(m)

    case m of {
        Just:
            writeln(m.value)
        default:
            writeCharLn('F')
    }

