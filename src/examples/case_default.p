type Colour = R | G | B

procedure printCol(col: Colour)
    case col of {
        R: writeCharLn('R')
        G: writeCharLn('G')
        B: writeCharLn('B')
    }

program Main
    var s: Colour

    s <- R()
    case s of {
        nil: writeCharLn('N')
        default: writeCharLn('D'); printCol(s)
    }

