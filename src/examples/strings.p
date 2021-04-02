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
            writeChar(s.ch)
            printStr(s.tail, ln)
        SNil:
            writeNewLine()
    }


// inclusively generating alphabets between a range
procedure genAlphabetsBetween(start: integer, end: integer) -> (s: String)
    var ch: integer
    ch := end
    s := SNil()
    
    while start <= end do
        s := SCons(ch, s)
        start := start + 1
        ch := ch - 1


program Main
    printStr(genAlphabetsBetween('A', 'Z'), true)       // print capital letters
    printStr(genAlphabetsBetween('a', 'z'), true)       // print lowercase letters
    printStr(genAlphabetsBetween('0', '9'), true)       // print numbers 0-9

    printStr(genAlphabetsBetween(67648, 67679), true)   // print Aramaic letters
    printStr(genAlphabetsBetween('𐡀','𐡟'), true)       // print Aramaic letters again
                                                        // Aramaic is R->L and it looks like VSCode tries to accomodate this... nice! :)
                                                        // (note that '𐡀' is displayed in the seemingly other argument but it is really the 67648 argument -- R->L changes this in rendering)

    // NOTE: If we _really_ wanted to do, we can make `""` also a syntactic sugar for a built-in String type
    // e.g., "abcd" becomes syntactic sugar for SCons('a', SCons('b', SCons('c', SCons('d', SNil()))))
    //       and we don't create a new `char` type on purpose (because arithmetic on characters is frequent and not harmful -- so we think of it as a positive thing)
