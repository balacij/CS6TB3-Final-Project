type Something = A(value: integer)
               | B
               | C
               | D
               | E
               | F

type Maybe = Just(value: integer)
           | Nothing

type Something2 = Something

type P = [0 .. 10] → Something

procedure doubler(x: integer) -> (r: integer)
    r := x * 2

procedure doubler2(x: integer) -> (y: integer, z: integer)
    const N = 10
    y, z := x, N

program Main
    var m: Maybe
    var q: (i: integer, m: Maybe)
    q.i := 10
    q.m := Just(20)
    m := Just(20)

    case q.m of {
        Just:
            writeln(r.value)
        default nothing
    }