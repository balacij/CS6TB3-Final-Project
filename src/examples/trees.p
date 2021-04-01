type Tree = Branch(left: Tree, right: Tree) | Leaf(value: integer)

program Main
    var left, right: Tree
    left ← Leaf(1)
    right ← Leaf(2)
    tree ← Branch(left, right)
