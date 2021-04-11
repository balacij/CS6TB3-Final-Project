type String = SCons(ch: integer, tail: String)
            | SNil

procedure printStr(s: String, ln: boolean)
    case s of {
        SCons: writeChar(s.ch); printStr(s.tail, ln)
        default: if ln then writeNewLine()
    }

// inclusively generating alphabets in a range
procedure genBetwn(start: integer, end: integer) -> (s: String)
    var ch: integer
    ch := end
    s := SNil()
    
    while start <= end do
        s, start, ch := SCons(ch, s), start + 1, ch - 1

program Main
    // print capital letters
    printStr(genBetwn('A', 'Z'), true)
    
    // print lowercase letters
    printStr(genBetwn('a', 'z'), true)
    
    // print numbers 0-9
    printStr(genBetwn('0', '9'), true)
    
    // print Greek alphabets
    printStr(genBetwn('α', 'ω'), true)
