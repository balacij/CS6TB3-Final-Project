type Colour = R | G | B

procedure printCol(col: Colour)
    case col of {
        R: writeCharLn('R')
        G: writeCharLn('G')
    }

program Main
    var s: Colour

    s <- R()
    case s of {
        default: writeCharLn('F'); printCol(s)
    }

    case s of {
        default nothing
    }

