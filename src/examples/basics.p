type Something = A
  | B
  | C
  | D
  | E
  | F

type Maybe = Just(value: integer)
           | Nothing

program Main
    var a: Something
    
    a <- A()

    case a of {
        A:
            writeln(0)
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
