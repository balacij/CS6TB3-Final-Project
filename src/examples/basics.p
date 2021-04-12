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

var a: Something
var b: Something
var c: Something

procedure doubler(x: integer) -> (r: integer)
    r := x * 2

procedure doubler2(x: integer) -> (y: integer, z: integer)
    const N = 10
    y, z := x, N

program Main
    var a: Something
    var x: integer
    var y: Something2
    var q: P

    q[0] := A(1)
    y := q[0]
    case y of {
        nil: writeCharLn('?')
        A: writeln(y.value)
        B: writeCharLn('B')
        C: writeCharLn('C')
        D: writeCharLn('D')
        E: writeCharLn('E')
        F: writeCharLn('F')
        default: writeln(0)
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
