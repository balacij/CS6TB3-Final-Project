type Maybe = Just(value: integer) | Nothing
type Maybes = [0 .. 10] -> Maybe

program Main
    var m: Maybe
    var maybes: Maybes
    var i: integer

    maybes[0] := Nothing()
    maybes[1] := Just(1)
    maybes[2] := Nothing()
    maybes[3] := Just(3)
    maybes[4] := Nothing()
    maybes[5] := Just(5)
    maybes[6] := Nothing()
    maybes[7] := Just(7)
    maybes[8] := Nothing()
    maybes[9] := Just(9)

    while i < 10 do
        m := maybes[i]
        case m of {
            Just: writeln(m.value)
            Nothing: writeln(-1)
            default nothing
        }
        i := i + 1
