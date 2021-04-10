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
    var a: Something
    var x: integer
    var y: Something2
    var q: (i: integer, m: Maybe)
    q.i := 10
    q.m := Just(20)

    case q.m of {
        Just:
            writeln(q.m.value)
        default nothing
    }

    y <- F()

    a <- A(doubler(4))

    case a of {
        A:
            writeln(a.value)
        B:
            writeln(1)
        C:
            writeln(2)
        D:
            writeln(3)
        E:
            writeln(4)
        F:
            writeln(5)
        default nothing
    }
