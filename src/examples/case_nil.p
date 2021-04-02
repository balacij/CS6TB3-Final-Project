type Something = A | B | C

program Main
    var s: Something
    s <- A()
    case s of {
        nil: writeCharLn('N')
        A: writeCharLn('A')
        B: writeCharLn('B')
        C: writeCharLn('C')
    }

