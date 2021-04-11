type Colour = R | G | Unknown

procedure printCol(col: Colour)
    case col of {
        nil: writeCharLn('?')
        R: writeCharLn('R')
        G: writeCharLn('G')
        default: writeCharLn('?')
    }

program Main
    var s: Colour
    s <- R()

    printCol(s)

