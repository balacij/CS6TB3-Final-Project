type String = SCons(ch: integer, tail: String)
            | SNil


procedure strlen(s: String) -> (n: integer)
    case s of {
        SCons:
            n := 1 + strlen(s.tail)
        default:
            n := 0
    }

procedure strcopy(s: String) -> (r: String)
    case s of {
        SCons:
            r := SCons(s.ch, strcopy(s.tail))
        default:
            r := SNil()
    }


procedure strconcat(l: String, r: String) -> (m: String)
    case l of {
        SCons:
            m := SCons(l.ch, strconcat(l.tail, r))
        default:
            m := strcopy(r)
    }


procedure strreverse(s: String) -> (r: String)
    case s of {
        SCons:
            r := strconcat(strreverse(s.tail), SCons(s.ch, SNil()))
        default:
            r := SNil()
    }


procedure printStr(s: String, ln: boolean)
    case s of {
        SCons:
            writeChar(s.ch)
            printStr(s.tail, ln)
        default:
            if ln then writeNewLine()
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
    var caps, lowers, numbers: String
    caps := genAlphabetsBetween('A', 'Z')
    lowers := genAlphabetsBetween('a', 'z')
    numbers := genAlphabetsBetween('0', '9')

    printStr(caps, true)                                // print capital letters
    printStr(lowers, true)                              // print lowercase letters
    printStr(numbers, true)                             // print numbers 0-9
    
    printStr(genAlphabetsBetween(67648, 67679), true)   // print Aramaic letters
    printStr(genAlphabetsBetween('𐡀','𐡟'), true)       // print Aramaic letters again
                                                        // Aramaic is R->L and it looks like VSCode tries to accomodate this... nice! :)
                                                        // (note that '𐡀' is displayed in the seemingly other argument but it is really the 67648 argument -- R->L changes this in rendering)
    
    printStr(strreverse(caps), true)                    // print reversed capital letters
    writeln(strlen(caps))
    printStr(strconcat(caps, lowers), true)
    writeln(strlen(strconcat(caps, lowers)))

    // NOTE: If we _really_ wanted to do, we can make `""` also a syntactic sugar for a built-in String type
    // e.g., "abcd" becomes syntactic sugar for SCons('a', SCons('b', SCons('c', SCons('d', SNil()))))
    //       and we don't create a new `char` type on purpose (because arithmetic on characters is frequent and not harmful -- so we think of it as a positive thing)
