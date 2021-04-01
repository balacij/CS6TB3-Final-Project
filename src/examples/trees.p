type Tree = Branch(left: Tree, right: Tree)
          | Leaf(value: integer)

procedure sumTree(tree: Tree) -> (total: integer)
    case tree of {
        Branch:
            total := sumTree(tree.left) + sumTree(tree.right)
        Leaf:
            total := tree.value
    }

program Main
    var base: Tree
    base ← Branch(Branch(Leaf(1), Leaf(2)), Branch(Branch(Leaf(3), Leaf(4)), Branch(Leaf(5), Leaf(6))))
    writeln(sumTree(base))
