type List = Cons(head: integer, tail: List) | Nil

procedure uptoList(n: integer) → (l: List)
    var tail: List
    if n < 1 then l ← Nil() else tail ← uptoList(n-1); writeln(n); l ← Cons(n, tail)

procedure consumeList(l: List)
    var r: List
    case l of {
        Cons:
            writeln(l.head)
            r := l.tail
            consumeList(r)
    }

procedure sumList(l: List) → (n: integer)
    case l of {
        Cons:
            n ← sumList(l.tail)
            n := n + l.head
        Nil:
            n := 0
    }

program Main
    var x: integer
    var mylist: List

    mylist ← uptoList(5)

    consumeList(mylist)
    x ← sumList(mylist)
    writeln(x)
