type Maybe = Just(value: integer) | Nothing
type Rec = (a: integer, b: boolean, m: Maybe)

program Main
    var r: Rec
    var m: Maybe
    var rm: Maybe

    m := Just(20)

    r.a := 10
    r.b := true
    r.m := m
    
    rm := r.m

    case rm of {
        nil: writeln(1)
        Just: 
            writeln(rm.value)
        default nothing
    }
