type List = Cons(head: integer, tail: List)
          | Nil

procedure upToList(n: integer) → (l: List)
    if n < 1 then l := Nil() else l := Cons(n, upToList(n-1))

procedure printList(l: List)
    case l of {
        Cons: writeln(l.head); printList(l.tail)
        default nothing
    }

procedure sumList(l: List) → (n: integer)
    case l of {
        Cons: n := sumList(l.tail) + l.head
        default: n := 0
    }

program Main
    var myList: List
    myList := upToList(5)
    printList(myList)
    writeln(sumList(myList))
