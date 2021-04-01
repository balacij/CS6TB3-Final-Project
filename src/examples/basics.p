type Something = A(value: integer)
               | B
               | C
               | D
               | E
               | F

type Maybe = Just(value: integer)
           | Nothing

procedure doubler(x: integer) -> (r: integer)
    r := x * 2

procedure doubler2(x: integer) -> (y: integer, z: integer)
    y, z := x, x

program Main
    var a: Something
    var x: integer

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
    }
