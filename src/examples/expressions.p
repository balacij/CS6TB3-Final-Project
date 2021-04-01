type Expr = Add(left: Expr, right: Expr) | Sub(left: Expr, right: Expr) | Mul(left: Expr, right: Expr) | Div(num: Expr, den: Expr) | Pow(base: Expr, exponent: Expr) | Int(value: integer)

program Main
    write(1)
