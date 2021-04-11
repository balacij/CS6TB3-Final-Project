# Examples

The following are a select group of examples that I found interesting:
* Colours
```
type RainbowColour = Red | Orange | Yellow | Green | Blue | Indigo | Violet
```
* Either
```
type Either = Left(value: integer) | Right(value: boolean)
```
* Maybe
```
type Maybe = Just(value: integer) | Nothing
```
* Lists
```
type List = Cons(head: integer, tail: List)
          | Nil
```
* Strings
```
type String = SCons(ch: integer, tail: String) | SNil
```
* Expressions
```
type Expr = Add(left: Expr, right: Expr)
          | Sub(left: Expr, right: Expr)
          | Mul(left: Expr, right: Expr)
          | Div(num: Expr, den: Expr)
          | Pow(base: Expr, exponent: Expr)
          | Int(value: integer)
```
* Trees
```
type Tree = Branch(left: Tree, right: Tree)
          | Leaf(value: integer)
```
* Maps
```
type StringIntMap = SIMCons(key: String, value: integer, tail: StringIntMap)
                  | SIMEmpty
```