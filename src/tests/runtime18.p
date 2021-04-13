type String = SCons(ch: integer, tail: String)
            | SNil

// Flat maps, can be optimized if we chose to!
// But let's keep it simple... it's good to think of this as a list of tuple pairs
type StringIntMap = SIMCons(key: String, value: integer, tail: StringIntMap)
                  | SIMEmpty

// String-related functions
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


procedure printStr(s: String, ln: boolean)
    case s of {
        SCons:
            writeChar(s.ch)
            printStr(s.tail, ln)
        default:
            if ln then writeNewLine()
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

// Map-related functions
// Recall our map construction...
// type StringIntMap = SIMCons(key: String, value: integer, tail: StringIntMap)
//                   | SIMEmpty

procedure mapHasKey(key: String, map: StringIntMap) -> (b: boolean)
    case map of {
        SIMCons: 
            if strequals(key, map.key) then b := true
            else b := mapHasKey(key, map.tail)
        default: b := false
    }

procedure mapInsert(key: String, value: integer, map: StringIntMap) -> (resultant: StringIntMap)
    resultant := SIMCons(key, value, map)

procedure mapGet(key: String, map: StringIntMap) -> (exists: boolean, value: integer)
    case map of {
        SIMCons:
            if strequals(key, map.key) then exists, value := true, map.value
            else exists, value <- mapGet(key, map.tail)
        default:
            exists := false
    }

program Main
    var l, r: String
    var map: StringIntMap

    l := single('a')
    r := SCons('a', single('b'))

    printStr(l, true)
    printStr(r, true)

    if strequals(l, r) then writeln(1)
    else writeln(0)
