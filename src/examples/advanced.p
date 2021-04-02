type Maybe = Just(value: integer)
           | Nothing


var m: Maybe

program Main
    m <- Just(32)

    m <- Nothing()
    
    m <- Just(22)

    case m of {
        Just:
            writeln(m.value)
        default:
            writeCharLn('F')
    }

