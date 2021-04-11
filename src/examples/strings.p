type String = SCons(ch: integer, tail: String)
            | SNil


procedure single(ch: integer) -> (s: String)
    s := SCons(ch, SNil())


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

procedure strequals(l: String, r: String) -> (b: boolean)
    case l of {
        SCons:
            case r of {
                SCons: 
                    if l.ch = r.ch then b := strequals(l.tail, r.tail) 
                    else b := false
                default: b := false
            }
        SNil:
            case r of {
                SNil: b := true
                default: b := false
            }
        
        default: b := false
    }


procedure printStr(s: String, ln: boolean)
    case s of {
        SCons: writeChar(s.ch); printStr(s.tail, ln)
        default: if ln then writeNewLine()
    }

// inclusively generating alphabets in a range
procedure genAlphabetsBetween(start: integer, end: integer) -> (s: String)
    var ch: integer
    ch := end
    s := SNil()
    
    while start <= end do
        s, start, ch := SCons(ch, s), start + 1, ch - 1


program Main
    printStr(genAlphabetsBetween('A', 'Z'), true)  // print capital letters
    printStr(genAlphabetsBetween('a', 'z'), true)  // print lowercase letters
    printStr(genAlphabetsBetween('0', '9'), true)  // print numbers 0-9
    
    printStr(genAlphabetsBetween(67648, 67679), true)   // print Aramaic letters
    printStr(genAlphabetsBetween('𐡀','𐡟'), true)       // print Aramaic letters again
                                                        // Aramaic is R->L and it looks like VSCode tries to accommodate this... nice! :)
                                                        // (note that '𐡀' is displayed in the seemingly other argument but it is really the 67648 argument -- R->L changes this in rendering)
