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
    }

procedure ops(e: Expr) -> (n: integer)
    case e of {
        Add: n := 1 + ops(e.left) + ops(e.right)
        Sub: n := 1 + ops(e.left) + ops(e.right)
        Mul: n := 1 + ops(e.left) + ops(e.right)
        Div: n := 1 + ops(e.num) + ops(e.den)
        Pow: n := 1 + ops(e.base) + ops(e.exponent)
        Int: n := 0
    }

procedure printExpr(e: Expr)
    var ch: integer
    var left, right: Expr

    case e of {
        Add: ch := 43; left := e.left; right := e.right
        Sub: ch := 45; left := e.left; right := e.right
        Mul: ch := 42; left := e.left; right := e.right
        Div: ch := 47; left := e.num; right := e.den
        Pow: ch := 94; left := e.base; right := e.exponent
        Int: write(e.value)
    }

    if ch > 0 then
        writeChar(40)
        printExpr(left)
        writeChar(41)
        writeChar(32)
        writeChar(ch)
        writeChar(32)
        writeChar(40)
        printExpr(right)
        writeChar(41)


program Main
    var e: Expr
    e := Mul(Mul(Add(Int(1), Int(2)), Int(1)), Pow(Int(2), Int(3)))
    
    writeln(eval(e))

    printExpr(e)
    writeNewLine()
    
    writeln(ops(e))
