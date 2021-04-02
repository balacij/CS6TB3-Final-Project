type Tree = Branch(left: Tree, right: Tree)
          | Leaf(value: integer)

type List = Cons(value: integer, tail: List)
          | Nil

procedure sumTree(tree: Tree) -> (total: integer)
    case tree of {
        Branch:
            total := sumTree(tree.left) + sumTree(tree.right)
        Leaf:
            total := tree.value
    }

procedure dupList(l: List) -> (r: List)
    case l of {
        Cons:
            r := Cons(l.value, dupList(l.tail))
        Nil:
            r := Nil()
    }

procedure concatLists(l: List, r: List) -> (res: List)
    case l of {
        Cons:
            res := Cons(l.value, concatLists(l.tail, r))
        Nil:
            // res := r    // works but it's BAD !!!!!! We re-create the left list, as such, we should do the same with the right list!!!!
            res := dupList(r)
    }

procedure flattenTree(tree: Tree) -> (l: List)
    case tree of {
        Branch:
            l := concatLists(flattenTree(tree.left), flattenTree(tree.right))
        Leaf:
            l := Cons(tree.value, Nil())
    }

procedure printList(l: List)
    case l of {
        Cons:
            write(l.value)
            writeChar(' ')      // 32 = ' '
            writeChar('-')      // 45 = '-'
            writeChar('>')      // 62 = '>'
            writeChar(' ')      // 32 = ' '
            printList(l.tail)
        Nil:
            writeCharLn('⊥')    // 8869 = '⊥'
    }


program Main
    var base: Tree
    var l: List
    var a, b, c: List

    a <- Cons(1, Cons(2, Nil()))
    b <- Cons(3, Cons(4, Nil()))
    c <- concatLists(a, b)

    printList(a)
    printList(b)
    printList(c)

    base <- Branch(Branch(Leaf(1), Leaf(2)), Branch(Branch(Leaf(3), Leaf(4)), Branch(Leaf(5), Leaf(6))))

    writeln(sumTree(base))

    printList(flattenTree(base))
