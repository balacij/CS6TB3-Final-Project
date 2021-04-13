type Rec = (a: integer, b: boolean, c: integer)
type Maybe = Just(value: integer, r: Rec) | Nothing


program Main
    var r: Rec
    var m: Maybe
    r.a := 10
    r.b := true
    r.c := 5000
    m := Just(20, r)
    
    case m of {
        nil: writeln(1)
        Just: 
            writeln(m.value)
            writeln(m.r.a)
            if m.r.b then
                writeCharLn('T')
            else
                writeCharLn('F')
            writeln(m.r.c)
        default nothing
    }
