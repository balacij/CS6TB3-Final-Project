# Examples

The following are a select group of examples that I found interesting. However, to view full program implementations making full use of these disjoint union types, please visit the `../src/examples/` folder.

* Colours
```
type RainbowColour = Red | Orange | Yellow | Green | Blue | Indigo | Violet

procedure printColourCode(rbwCol: RainbowColour)
    case rbwCol of {
        Red:     writeCharLn('R')
        Orange:  writeCharLn('O')
        Yellow:  writeCharLn('Y')
        Green:   writeCharLn('G')
        Blue:    writeCharLn('B')
        Indigo:  writeCharLn('I')
        Violet:  writeCharLn('V')
        default: writeCharLn('?')
    }
```
* Either
```
type Either = Left(value: integer) | Right(value: boolean)
```
* Maybe
```
type Maybe = Just(value: integer) | Nothing

procedure valOr(v: Maybe, n: integer) -> (r: integer)
    case v of {
        Just:
            r := v.value
        default:
            r := n
    }
```
* Lists
```
type List = Cons(head: integer, tail: List)
          | Nil

procedure sumList(l: List) → (n: integer)
    case l of {
        Cons:
            n := sumList(l.tail) + l.head
        default:
            n := 0
    }
```
* Strings
```
type String = SCons(ch: integer, tail: String) | SNil

procedure printStr(s: String, ln: boolean)
    case s of {
        SCons:
            writeChar(s.ch)
            printStr(s.tail, ln)
        default:
            if ln then writeNewLine()
    }
```
* Expressions
```
type Expr = Add(left: Expr, right: Expr)
          | Sub(left: Expr, right: Expr)
          | Mul(left: Expr, right: Expr)
          | Div(num: Expr, den: Expr)
          | Pow(base: Expr, exponent: Expr)
          | Int(value: integer)

procedure pow(base: integer, exponent: integer) -> (res: integer)
    res := base
    while exponent > 1 do
        res := res * base
        exponent := exponent - 1


procedure eval(e: Expr) -> (res: integer)
    case e of {
        Add: res := eval(e.left) + eval(e.right)
        Sub: res := eval(e.left) - eval(e.right)
        Mul: res := eval(e.left) * eval(e.right)
        Div: res := eval(e.num) / eval(e.den)
        Pow: res := pow(eval(e.base), eval(e.exponent))
        Int: res := e.value
        default: res := 0
    }
```
* Trees
```
type Tree = Branch(left: Tree, right: Tree)
          | Leaf(value: integer)

procedure flattenTree(tree: Tree) -> (l: List)
    case tree of {
        Branch:
            l := concatLists(flattenTree(tree.left), flattenTree(tree.right))
        Leaf:
            l := Cons(tree.value, Nil())
        default:
            l := Nil()
    }
```
* Maps
```
type StringIntMap = SIMCons(key: String, value: integer, tail: StringIntMap)
                  | SIMEmpty

procedure mapHasKey(key: String, map: StringIntMap) -> (b: boolean)
    case map of {
        SIMCons: 
            if strequals(key, map.key) then b := true
            else b := mapHasKey(key, map.tail)
        default: b := false
    }

procedure mapInsert(key: String, value: integer, map: StringIntMap) -> (resultant: StringIntMap)
    resultant := SIMCons(key, value, map)

procedure mapGet(key: String, map: StringIntMap) -> (exists: boolean, value: integer)
    case map of {
        SIMCons:
            if strequals(key, map.key) then exists, value := true, map.value
            else exists, value <- mapGet(key, map.tail)
        default:
            exists := false
    }
```