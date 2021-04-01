type String = SCons(ch: integer, tail: String)
            | SNil


procedure strlen(s: String) -> (n: integer)
    case s of {
        SCons:
            n := 1 + strlen(s.tail)
        SNil:
            n := 0
    }

procedure printStr(s: String, ln: boolean)
    case s of {
        SCons:
            writeAscii(s.ch)
            printStr(s.tail, ln)
        SNil:
            writeNewLine()
    }

procedure genAlphabetsBetween(start: integer, end: integer) -> (s: String)
    var ch: integer
    ch := end - 1
    s := SNil()
    
    while start < end do
        s := SCons(ch, s)
        start := start + 1
        ch := ch - 1


program Main
    printStr(genAlphabetsBetween(65, 91), true)   // print capital letters
    printStr(genAlphabetsBetween(97, 123), true)  // print lowercase letters
    printStr(genAlphabetsBetween(48, 58), true)

