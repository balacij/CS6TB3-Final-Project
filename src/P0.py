# ## The P0 Compiler
# #### COMP SCI 4TB3/6TB3, McMaster University
# #### Original Author: Emil Sekerinski, revised March 2021
#
# This collection of _Jupyter notebooks_ develops a compiler for P0, a programming langauge inspired by Pascal, a language designed for ease of compilation. The compiler currently generates WebAssembly and MIPS code, but is modularized to facilitate other targets. WebAssembly is representative of stack-based virtual machines while the MIPS architecture is representative of Reduced Instruction Set Computing (RISC) processors.
#
# ### The P0 Language
# The main syntactic elements of P0 are *statements*, *declarations*, *types*, and *expressions*.
#
# #### Statements
# * _Assignment statement_ (`x₁`, `x₂`, … variable identifers, `d` selector, `e`, `e₁`, `e₂`, … expressions):
#       x₁, x₂, … := e₁, e₂, …
#       x d := e
# * _Procedure call_ (`p` procedure identifier, `e₁`, `e₂`, … expressions, `x₁`, `x₂`, … variable identifiers):
#       p(e₁, e₂, …)
#       x₁, x₂, … ← p(e₁, e₂, …)
# * _Sequential composition_ (`S₁`, `S₂`, … statements):
#       S₁; S₂; …
# * _If-statements_ (`B` Boolean expression, `S`, `T` statements):
# 	  if B then S
#       if B then S else T
# * _While-statements_ (`B` Boolean expression, `S` statement):
#       while B do S
#
# #### Declarations
# * _Constant declaration_ (`c` constant identifier, `e` constant expression):
#       const c =  e
# * _Type declaration_ (`t` type identifier, `T` type):
#       type t = T
# * _Variable declaration_ (`x₁`, `x₂`, … variable identifiers, `T` type):
#       var x₁, x₂, …: T
# * _Procedure declaration_ (`p` procedure identifier, `v₁`, `v₂`, … variable identifiers, `T₁`, `T₂`, …, `U₁`, `U₂`, … types, `D₁`, `D₂`, … declarations, `S` statement):
#       procedure p (v₁: T₁, v₂: T₂, …) → (r₁: U₁, r₂: U₂, …)
#           D₁
#           D₂
#           …
#               S
#
# #### Types
# * _Elementary Types:_
#       integer, boolean
# * _Arrays_ (`m`, `n` integer expressions, `T` type):
#       [m .. n] → T
# * _Records_ (`f₁`, `f₂`, … field identifiers, `T₁`, `T₂`, …, types):
#       (f₁: T₁, f₂: T₂, …)
# * _Sets_ (`m`, `n` integer expressions)
#       set [m .. n]
#
# #### Expressions:
# * _Constants:_
# 	  number, identifier
# * _Selectors_ (`i` index expression, `f` field identifier):
#       [i]
#       .f
# * _Operators,_ in order of their binding power (e, e₁, e₂ are expressions):
# 	  (e), ¬ e, #e, ∁ e
#       e₁ × e₂, e₁ div e₂, e₁ mod e₂, e₁ ∩ e₂, e₁ and e₂
#       + e, – e, e₁ + e₂, e₁ – e₂, e₁ ∪ e₂, e₁ or e₂
#       e₁ = e₂, e₁ ≠ e₂, e₁ < e₂, e₁ ≤ e₂, e₁ > e₂, e₁ ≥ e₂, e₁ ∈ e₂, e₁ ⊆ e₂, e₁ ⊇ e₂
#
# Types `integer`, `boolean`, constants `true`, `false`, and procedures `read`, `write`, `writeln` are not symbols of the grammar; they are _standard identifiers_ (*predefined identifiers*).

# ### P0 Examples
#
# ```Pascal
# procedure quotrem(x, y: integer) → (q, r: integer)
#     q, r := 0, x
#     while r ≥ y do // q × y + r = x ∧ r ≥ y
#         r, q := r - y, q + 1
#
# program arithmetic
#     var x, y, q, r: integer
#       x ← read(); y ← read()
#       q, r ← quotrem(x, y)
#       write(q); write(r)
# ```

# ```Pascal
# procedure fact(n: integer) → (f: integer)
#     if n = 0 then f := 1
#     else
#         f ← fact(n - 1); f := f × n
#
# program factorial;
#     var y, z: integer
#         y ← read(); z ← fact(y); write(z)
# ```

# ```Pascal
# const N = 10
# var a: [0 .. N - 1] → integer
#
# procedure has(x: integer) → (r: boolean)
#     var i: integer
#         i := 0
#         while (i < N) and (a[i] ≠ x) do i := i + 1
#         r := i < N
# ```

# ### The P0 Grammar
#
#     selector ::= { "[" expression "]" | "." ident}
#     factor ::= ident selector | integer | "(" expression ")" | "{" [expression {"," expression}] "}" | ("¬" | "#" | "∁") factor
#     term ::= factor {("×" | "div" | "mod" | "∩" | "and") factor}
#     simpleExpression ::= ["+" | "-"] term {("+" | "-" | "∪" | "or") term}
#     expression ::= simpleExpression
#         {("=" | "≠" | "<" | "≤" | ">" | "≥" | "∈" | "⊆" | "⊇") simpleExpression}
#     statementList ::= statement {";" statement}
#     statementBlock ::= statementList {statementList}
#     statementSuite ::= statementList | INDENT statementBlock DEDENT
#     statement ::=
#         ident selector ":=" expression |
#         ident {"," ident} (":=" expression {"," expression} |
#             "←" ident "(" [expression {"," expression}] ")") |
#         "if" expression "then" statementSuite ["else" statementSuite] |
#         "while" expression "do" statementSuite
#     type ::=
#         ident |
#         "[" expression ".." expression "]" "→" type |
#         "(" typedIds ")" |
#         "set" "[" expression ".." expression "]"
#     typedIds ::= ident {"," ident} ":" type {"," ident {"," ident} ":" type}.
#     declarations ::=
#         {"const" ident "=" expression}
#         {"type" ident "=" type}
#         {"var" typedIds}
#         {"procedure" ident "(" [typedIds] ")" [ "→" "(" typedIds ")" ] body}
#     body ::= INDENT declarations (statementBlock | INDENT statementBlock DEDENT) DEDENT
#     program ::= declarations "program" ident body

# ### Modularization
# <div><span style="float:right"><img width="60%" src="./img/modularization.svg"/></span></div>
#
# - The parser, `P0`, parses the source text, type-checks it, evaluates constant expressions, and generates target code, in one pass over the source text.
# - The scanner, `SC`, reads characters of the source text and provides the next symbol to the parser; it allows errors to be reported at the current position in the source text.
# - The symbol table, `ST`, stores all currently valid declarations, as needed for type-checking.
# - The code generator, `CG`, provides the parser with procedures for generating code for P0 expressions, statements, and variable declarations, and procedure declarations.
#
# The parser is the main program that calls the scanner, symbol table, and code generator. All call the scanner for error reporting. The code generator augments the entries in the the symbol table, for example with the size and location of variables. There are three code generators: `CCGwat` generates WebAssembly code, `CGmips` generates MIPS code, and `CGast` generates only an abstract syntax tree.

# ### The Parser
# The scanner and symbol table are always imported. Depending on the selected target, a different code generator is imported when compilation starts.


import SC  #  used for SC.init, SC.sym, SC.val, SC.error
from SC import (
    TIMES,
    DIV,
    MOD,
    AND,
    PLUS,
    MINUS,
    OR,
    EQ,
    NE,
    LT,
    GT,
    LE,
    GE,
    PERIOD,
    COMMA,
    COLON,
    NOT,
    LPAREN,
    RPAREN,
    LBRAK,
    RBRAK,
    LARROW,
    RARROW,
    LBRACE,
    RBRACE,
    CARD,
    COMPLEMENT,
    UNION,
    INTERSECTION,
    ELEMENT,
    SUBSET,
    SUPERSET,
    DOTDOT,
    THEN,
    DO,
    BECOMES,
    NUMBER,
    IDENT,
    SEMICOLON,
    ELSE,
    IF,
    WHILE,
    CONST,
    TYPE,
    VAR,
    SET,
    PROCEDURE,
    PROGRAM,
    INDENT,
    DEDENT,
    EOF,
    getSym,
    mark,
    ADT_SEP,
    CASE,
    OF,
    DEFAULT,
    NIL,
)

import ST  #  used for ST.init
from ST import (
    Var,
    Ref,
    Const,
    Type,
    Proc,
    StdProc,
    Int,
    Bool,
    Record,
    Array,
    Set,
    ADT,
    ADTKind,
    ADTSelfRef,
    newDecl,
    safeFind,
    find,
    getAllADTKinds,
    openScope,
    topScope,
    closeScope,
)


# The parser type-checks the source code; the code generators are supposed to compile all type-correct code, but may impose restrictions. Procedure `compatible` checks for structural compatibility. In case of sets, lower and upper bound of sets are not checked.


def compatible(xt, yt):
    # print('checking compatibility between')
    # print(xt)
    # print(yt)
    return (
        xt == yt
        or type(xt) == Set == type(yt)
        or (type(xt) == Array == type(yt) and xt.length == yt.length and compatible(xt.base, yt.base))
        or (type(xt) == Record == type(yt) and all(compatible(xf.tp, yf.tp) for xf, yf in zip(xt.fields, yt.fields)))
        or (type(xt) == ADT == type(yt) and xt.name == yt.name)
        or (type(xt) == ADTSelfRef and compatible(xt.tp.val, yt))
        or (type(yt) == ADTSelfRef and compatible(yt.tp.val, xt))
    )


# The first sets for recursive descent parsing are:


FIRSTSELECTOR = {LBRAK, PERIOD}
FIRSTFACTOR = {IDENT, NUMBER, LPAREN, NOT, CARD, COMPLEMENT}
FIRSTEXPRESSION = {PLUS, MINUS, IDENT, NUMBER, LPAREN, NOT, CARD, COMPLEMENT}
FIRSTSTATEMENT = {IDENT, IF, WHILE, CASE}
FIRSTTYPE = {IDENT, LPAREN}
FIRSTDECL = {CONST, TYPE, VAR, PROCEDURE}


# Procedure `selector()` parses
#
#     selector ::= { "[" expression "]" | "." ident }
#
# and generates code for the selector if not error is reported.


def selector(x, right=True):
    while SC.sym in {LBRAK, PERIOD}:
        if SC.sym == LBRAK:  #  x[y]
            getSym()
            y = expression()
            if type(x.tp) == Array:
                if y.tp == Int:
                    if type(y) == Const and (y.val < x.tp.lower or y.val >= x.tp.lower + x.tp.length):
                        mark("index out of bounds")
                    else:
                        x = CG.genIndex(x, y)
                else:
                    mark("index not integer")
            else:
                mark("not an array")
            if SC.sym == RBRAK:
                getSym()
            else:
                mark("] expected")
        else:  #  x.f
            getSym()
            if SC.sym == IDENT:
                if type(x.tp) == Record:
                    for f in x.tp.fields:
                        if f.name == SC.val:
                            x = CG.genSelect(x, f, right=right)
                            break
                    else:
                        mark("not a field")
                    getSym()
                else:
                    print(str(x))
                    mark("not a record")
            else:
                mark("identifier expected")
    return x


# Procedure `factor()` parses
#
#     factor ::= ident selector | integer | "(" expression ")" | "{" [expression {"," expression}] "}" | ("¬" | "#" | "∁") factor
#
# and generates code for the factor if no error is reported. If the factor is a constant, a `Const` item is returned (and code may not be generated); if the factor is not a constant, the location of the result is returned.


def factor():
    if SC.sym == IDENT:
        x = find(SC.val)

        # Jason: if we find an ADTKind, it's likely a constructor, so we find it's related procedure
        if type(x) == ADTKind:
            x = find(f"__mk_{x.name}")

        if type(x) == Var:
            x = CG.genVar(x)
            getSym()
        elif type(x) == Const:
            x = Const(x.tp, x.val)
            x = CG.genConst(x)
            getSym()
        elif (
            type(x) in {Proc, StdProc} and len(x.res) == 1
        ):  # JASON: allow procedure in-place IF it has a single return value only!!!
            getSym()
            x = funcCall([], x, x)
        else:
            mark(f"variable or constant identifier expected; got '{SC.val}' of type '{str(type(x))}'")
        x = selector(x)
    elif SC.sym == NUMBER:
        x = Const(Int, SC.val)
        x = CG.genConst(x)
        getSym()
    elif SC.sym == LPAREN:
        getSym()
        x = expression()
        if SC.sym == RPAREN:
            getSym()
        else:
            mark(") expected")
    elif SC.sym == LBRACE:
        getSym()
        if SC.sym in FIRSTEXPRESSION:
            y = expression()
            if y.tp == Int:
                x = CG.genUnaryOp(SET, y)
            else:
                mark("not integer")
            while SC.sym == COMMA:
                getSym()
                y = expression()
                if y.tp == Int:
                    y = CG.genUnaryOp(SET, y)
                else:
                    mark("not integer")
                x = CG.genBinaryOp(UNION, x, y)
        else:
            x = Const(Set(0, 32), 0)
            x = CG.genConst(x)
        if SC.sym == RBRACE:
            getSym()
        else:
            mark("} expected")
    elif SC.sym == NOT:
        getSym()
        x = factor()
        if x.tp != Bool:
            mark("not boolean")
        elif type(x) == Const:
            x.val = 1 - x.val  # constant folding
        else:
            x = CG.genUnaryOp(NOT, x)
    elif SC.sym in {CARD, COMPLEMENT}:
        op = SC.sym
        getSym()
        x = factor()
        if type(x.tp) == Set:
            x = CG.genUnaryOp(op, x)
        else:
            mark("set expected")
    else:
        mark("expression expected")
    return x


# Procedure `term()` parses
#
#     term ::= factor {("×" | "div" | "mod" | "∩" | "and") factor}
#
# and generates code for the term if no error is reported. If the term is a constant, a `Const` item is returned (and code may not be generated); if the term is not a constant, the location of the result is returned.


def term():
    x = factor()
    while SC.sym in {TIMES, DIV, MOD, INTERSECTION, AND}:
        op = SC.sym
        getSym()
        if op == AND and type(x) != Const:
            x = CG.genUnaryOp(AND, x)
        y = factor()  # x op y
        if op in {TIMES, DIV, MOD} and x.tp == Int == y.tp:
            if type(x) == Const == type(y):  # constant folding
                if op == TIMES:
                    x.val = x.val * y.val
                elif op == DIV:
                    x.val = x.val // y.val
                elif op == MOD:
                    x.val = x.val % y.val
            else:
                x = CG.genBinaryOp(op, x, y)
        elif op == INTERSECTION and type(x.tp) == Set == type(y.tp):
            x = CG.genBinaryOp(op, x, y)
        elif op == AND and x.tp == Bool == y.tp:
            if type(x) == Const:  # constant folding
                if x.val:
                    x = y  # if x is true, take y, else x
            else:
                x = CG.genBinaryOp(AND, x, y)
        else:
            mark("bad type")
    return x


# Procedure `simpleExpression()` parses
#
#     simpleExpression ::= ["+" | "-"] term {("+" | "-" | "∪" | "or") term}
#
# and generates code for the simple expression if no error is reported. If the simple expression is a constant, a `Const` item is returned (and code may not be generated); if the simple expression is not constant, the location of the result is returned.


def simpleExpression():
    if SC.sym == PLUS:
        getSym()
        x = term()
    elif SC.sym == MINUS:
        getSym()
        x = term()
        if x.tp != Int:
            mark("bad type")
        elif type(x) == Const:
            x.val = -x.val  # constant folding
        else:
            x = CG.genUnaryOp(MINUS, x)
    else:
        x = term()
    while SC.sym in {PLUS, MINUS, UNION, OR}:
        op = SC.sym
        getSym()
        if op == OR and type(x) != Const:
            x = CG.genUnaryOp(OR, x)
        y = term()  # x op y
        if op in {PLUS, MINUS} and x.tp == Int == y.tp:
            if type(x) == Const == type(y):  # constant folding
                if op == PLUS:
                    x.val = x.val + y.val
                elif op == MINUS:
                    x.val = x.val - y.val
            else:
                x = CG.genBinaryOp(op, x, y)
        elif op == UNION and type(x.tp) == Set == type(y.tp):
            x = CG.genBinaryOp(UNION, x, y)
        elif op == OR and x.tp == Bool == y.tp:
            if type(x) == Const:  # constant folding
                if not x.val:
                    x = y  # if x is false, take y, else x
            else:
                x = CG.genBinaryOp(OR, x, y)
        else:
            # print(x, y)
            mark("bad type")
    return x


# Procedure `expression()` parses
#
#     expression ::= simpleExpression
#         {("=" | "≠" | "<" | "≤" | ">" | "≥" | "∈" | "⊆" | "⊇") simpleExpression}
#
# and generates code for the expression if no error is reported. If the expression is a constant, a `Const` item is returned (and code may not be generated); if the expression is not constant, the location of the result is returned.


def expression():
    x = simpleExpression()
    while SC.sym in {EQ, NE, LT, LE, GT, GE, ELEMENT, SUBSET, SUPERSET}:
        op = SC.sym
        getSym()
        if op in (EQ, NE, LT, LE, GT, GE):
            y = simpleExpression()  # x op y
            if x.tp == y.tp in (Int, Bool):
                if type(x) == Const == type(y):  # constant folding
                    if op == EQ:
                        x.val = int(x.val == y.val)
                    elif op == NE:
                        x.val = int(x.val != y.val)
                    elif op == LT:
                        x.val = int(x.val < y.val)
                    elif op == LE:
                        x.val = int(x.val <= y.val)
                    elif op == GT:
                        x.val = int(x.val > y.val)
                    elif op == GE:
                        x.val = int(x.val >= y.val)
                    x.tp = Bool
                else:
                    x = CG.genRelation(op, x, y)
            else:
                mark("bad type")
        elif (op == ELEMENT and x.tp == Int) or (op in (SUBSET, SUPERSET) and type(x.tp) == Set):
            x = CG.genUnaryOp(op, x)
            y = simpleExpression()
            if type(y.tp) == Set:
                x = CG.genRelation(op, x, y)
            else:
                mark("set expected")
        else:
            mark("bad type")
    return x


# Procedure `statementList()` parses
#
#     statementList ::= statement {";" statement}
#
# and generates code for the statement list if no error is reported.


def statementList():
    x = statement()
    while SC.sym == SEMICOLON:
        getSym()
        y = statement()
        x = CG.genSeq(x, y)
    return x


# Procedure `statementBlock()` parses
#
#     statementBlock ::= statementList {statementList}
#
# and generates code for the statement block if no error is reported. Each statement list has to start on a new line.


def statementBlock():
    x = statementList()
    while SC.sym in FIRSTSTATEMENT:
        if not SC.newline:
            mark("new line expected")
        y = statementList()
        x = CG.genSeq(x, y)
    return x


# Procedure `statementSuite()` parses
#
#     statementSuite ::= statementList | INDENT statementBlock DEDENT
#
# and generates code for the statement suite if no error is reported.


def statementSuite():
    if SC.sym in FIRSTSTATEMENT:
        x = statementList()
    elif SC.sym == INDENT:
        getSym()
        x = statementBlock()
        if SC.sym == DEDENT:
            getSym()
        else:
            mark("dedent or new line expected")
    else:
        mark("indented statement expected")
    return x


# Procedure `statement()` parses
#
#     statement ::=
#         ident selector ":=" expression |
#         ident "." ident
#         ident {"," ident} (":=" expression {"," expression} |
#             "←" ident "(" [expression {"," expression}] ")") |
#         "if" expression "then" statementSuite ["else" statementSuite] |
#         "while" expression "do" statementSuite
#
# and generates code for the statement if no error is reported.


def cases(x, casedOn):
    """
    "<ADTKind>: <statementSuite>
    {<ADTKind>: <statementSuite> \n}"
    """
    # TODO: if SC.sym == DEFAULT  -- "catch all"
    # TODO: if SC.sym == NIL      -- uninitialized ones
    if SC.sym == IDENT:
        kind = SC.val
        if SC.val in casedOn:
            mark(f"duplicate cases for '{SC.val}'")
        y = find(kind)
        if type(y) != ADTKind:
            mark(f"'{SC.val}' is not an ADT Kind identifier name")
        if y not in x.tp.kinds:
            mark(f"'{SC.val}' is not an ADT Kind that belongs to ADT '{x.tp.name}'")
        getSym()
        CG.genCaseStart(x, y.index)
        if SC.sym == COLON:
            getSym()
        else:
            mark("':' expected after ADT kind identifier")
        openScope()
        oldXTp = None
        if y.record is not None:
            oldXTp = x.tp
            x.tp = y.record.val
        x.isAdtSelector = True
        newDecl(x.name, x, overwriteLev=False, errOnDup=False)
        # TODO: rather disappointing results... if a var is a global variable, this simply does not work nicely...
        statementSuite()
        if y.record is not None:
            x.tp = oldXTp
        closeScope()
        x.isAdtSelector = False
        if SC.sym in {IDENT, NIL, DEFAULT}:
            CG.genCaseElse()
            casedOn.append(y.name)  # TODO: for default, nil, this needs to be different :)
            cases(x, casedOn)
        CG.genCaseEnd()


def funcCall(xs, x, y):  # call y(ap) or xs ← y(ap)
    fp, ap, i = y.par, [], 0  #  list of formals, list of actuals
    if SC.sym == LPAREN:
        getSym()
    else:
        mark(f"'(' expected; got {SC.sym}")
    if SC.sym in FIRSTEXPRESSION:
        a = expression()
        if i < len(fp):
            if compatible(fp[i].tp, a.tp):
                ap.append(CG.genActualPara(a, fp[i], i))
            else:
                mark("incompatible parameter")
        else:
            mark("extra parameter")
        i = i + 1
        while SC.sym == COMMA:
            getSym()
            a = expression()
            if i < len(fp):
                if compatible(fp[i].tp, a.tp):
                    ap.append(CG.genActualPara(a, fp[i], i))
                else:
                    mark("incompatible parameter")
            else:
                mark("extra parameter")
            i = i + 1
    if SC.sym == RPAREN:
        getSym()
    else:
        mark("')' expected")
    if i < len(fp):
        mark("too few parameters")
    elif type(y) == StdProc:
        if y.name == "read":
            x = CG.genRead(x)
        elif y.name == "write":
            x = CG.genWrite(a)
        elif y.name == "writeln":
            x = CG.genWriteln()
        elif y.name == "writeAscii":
            x = CG.genWriteAscii()
        elif y.name == "writeAsciiLn":
            x = CG.genWriteAsciiLn()
        elif y.name == "writeNewLine":
            x = CG.genWriteNewLine()
        else:
            mark(f'unknown StdProc; {y.name}')
    else:
        x = CG.genCall(xs, y, ap)
    return x


def statement():
    if SC.sym == IDENT:  # x := y, y(...), x ← y(...)
        # type(x) == Proc, StdProc: check no result parameters needed; call, y := true, x
        # type(x) ≠ Proc, StdProc: x := selector():
        #   sym == BECOMES: assignment; call := false
        #   sym == LARROW: check result parameter match, type(y) is Proc, StdProc,
        x = find(SC.val)
        if type(x) in {Proc, StdProc}:  # procedure call without result
            if x.res != []:
                mark("variable for result expected")
            getSym()
            call, xs, y = True, [], x
        elif type(x) == Var:  # assignment or procedure call with result
            x = find(SC.val)
            x = CG.genVar(x)
            getSym()
            if SC.sym in FIRSTSELECTOR:
                xs = [CG.genLeftAssign(selector(x, False))]  # array or field update
            else:  # multiple assignment or procedure call with result
                xs = [CG.genLeftAssign(x)]
                while SC.sym == COMMA:
                    getSym()
                    if SC.sym == IDENT:
                        x = find(SC.val)
                        if x.name not in {x.name for x in xs}:
                            if type(x) == Var:
                                xs += [CG.genLeftAssign(CG.genVar(x))]
                                getSym()
                            else:
                                mark("variable identifier expected")
                        else:
                            mark("duplicate variable identifier")
                    else:
                        mark("identifier expected")
            if SC.sym == BECOMES:
                getSym()
                call = False
                ys = [CG.genRightAssign(expression())]  # xs := ys
                while SC.sym == COMMA:
                    getSym()
                    ys += [CG.genRightAssign(expression())]
                if len(xs) == len(ys):
                    for x, y in zip(reversed(xs), reversed(ys)):
                        if compatible(x.tp, y.tp):
                            x = CG.genAssign(x, y)
                        else:
                            mark("incompatible assignment")
                else:
                    mark("unbalanced assignment")
            elif SC.sym == LARROW:  # x ← y(...)
                getSym()
                if SC.sym == IDENT:
                    y = find(SC.val)
                    getSym()
                    call = True
                else:
                    mark("procedure identifier expected")

                # JASON: Added "ADTKind" function helper lookup
                if type(y) == ADTKind:
                    y = find(f"__mk_{y.name}")

                if type(y) in {Proc, StdProc}:
                    if len(xs) == len(y.res):
                        for x, r in zip(xs, y.res):
                            if not compatible(x.tp, r.tp):
                                mark("incompatible call")
                    else:
                        mark("unbalanced call")
                else:
                    mark("procedure expected")
            else:
                mark(":= or ← expected")
        else:
            mark("variable or procedure expected")
        if call:
            x = funcCall(xs, x, y)  # TODO
    elif SC.sym == IF:
        getSym()
        x = expression()
        if x.tp == Bool:
            x = CG.genThen(x)
        else:
            mark("boolean expected")
        if SC.sym == THEN:
            getSym()
        else:
            mark("'then' expected")
        y = statementSuite()
        if SC.sym == ELSE:
            getSym()
            y = CG.genElse(x, y)
            z = statementSuite()
            x = CG.genIfElse(x, y, z)
        else:
            x = CG.genIfThen(x, y)
    elif SC.sym == WHILE:
        getSym()
        t = CG.genWhile()
        x = expression()
        if x.tp == Bool:
            x = CG.genDo(x)
        else:
            mark("boolean expected")
        if SC.sym == DO:
            getSym()
        else:
            mark("'do' expected")
        y = statementSuite()
        x = CG.genWhileDo(t, x, y)
    elif SC.sym == CASE:
        getSym()
        x = expression()
        if type(x) != Var and len(x.name) == 0:
            mark('expected variable name to `case` on')

        if type(x.tp) != ADT:
            mark('ADT variable expected in `case`')

        if SC.sym == OF:
            getSym()
        else:
            mark("'of' expected")

        if SC.sym == LBRACE:
            getSym()
        else:
            mark("'{' expected")
        if SC.sym == INDENT:
            getSym()
        else:
            mark('indent expected when casing')
        cases(x, [])
        if SC.sym == DEDENT:
            getSym()
        else:
            mark('dedent expected when cases exhausted')
        if SC.sym == RBRACE:
            getSym()
        else:
            mark("'}' expected")
    else:
        mark("statement expected")
    return x


# Procedure `typ` parses
#
#     type ::=
#         ident |
#         "[" expression ".." expression "]" "→" type |
#         "(" typedIds ")" |
#         "set" "[" expression ".." expression "]"
#
# and returns a type descriptor if not error is reported. The array bound are checked to be constants; the lower bound must be smaller or equal to the upper bound.


def adtKind(index, adtName):
    name = SC.val
    getSym()

    record = None
    if SC.sym == LPAREN:
        record = typ(adtName=adtName)

    x = CG.genADTKind(ADTKind(index=index, name=name, record=record))
    newDecl(name, x)
    return x


def typ(adtName=None, parsingTypedIds=False):
    if SC.sym == IDENT:
        ident = SC.val
        exists, x = safeFind(ident)
        if exists:
            if type(x) == Type:
                x = Type(x.val)
                getSym()
            else:
                mark("type identifier expected")
        elif adtName is not None:
            if parsingTypedIds and SC.val == adtName:
                getSym()
                return Type(CG.genADTSelfRef(ADTSelfRef()))

            i = 1
            kinds = [adtKind(index=i, adtName=adtName)]
            while SC.sym in {INDENT, DEDENT}:  # consume whitespace
                getSym()
            while SC.sym == ADT_SEP:
                getSym()
                i += 1
                kinds.append(adtKind(index=i, adtName=adtName))
                while SC.sym in {INDENT, DEDENT}:  # consume whitespace
                    getSym()

            x = Type(CG.genADT(ADT(name=adtName, kinds=kinds)))

            for kind in kinds:
                kind.tp = x
                if kind.record is not None:
                    for field in kind.record.val.fields:
                        field = field.tp
                        if type(field) == ADTSelfRef:
                            field.tp = x

            # JASON: generate helper functions for ADT Kind generation, and register them all as functions
            adtKinds = kinds  # getAllADTKinds()
            CG.genADTKindMkFuncs(adtKinds)
            for kind in adtKinds:
                newDecl(
                    f"__mk_{kind.name}",
                    Proc(
                        [] if kind.record is None else [field for field in kind.record.val.fields], [Var(kind.tp.val)]
                    ),
                )
        else:
            mark("type identifier expected")
    elif SC.sym == LBRAK:
        getSym()
        x = expression()
        if SC.sym == DOTDOT:
            getSym()
        else:
            mark("'..' expected")
        y = expression()
        if SC.sym == RBRAK:
            getSym()
        else:
            mark("']' expected")
        if SC.sym == RARROW:
            getSym()
        else:
            mark("'→' expected")
        z = typ().val
        if type(x) != Const or x.val < 0:
            mark("bad lower bound")
        elif type(y) != Const or y.val < x.val:
            mark("bad upper bound")
        else:
            x = Type(CG.genArray(Array(z, x.val, y.val - x.val + 1)))
    elif SC.sym == LPAREN:
        getSym()
        openScope()
        typedIds(adtName=adtName)
        if SC.sym == RPAREN:
            getSym()
        else:
            mark("')' expected")
        r = topScope()
        closeScope()
        x = Type(CG.genRec(Record(r)))
    elif SC.sym == SET:
        getSym()
        if SC.sym == LBRAK:
            getSym()
        else:
            mark("'[' expected")
        x = expression()
        if SC.sym == DOTDOT:
            getSym()
        else:
            mark("'..' expected")
        y = expression()
        if SC.sym == RBRAK:
            getSym()
        else:
            mark("']' expected")
        if type(x) != Const:
            mark("bad lower bound")
        elif type(y) != Const or y.val < x.val:
            mark("bad upper bound")
        else:
            x = Type(CG.genSet(Set(x.val, y.val - x.val + 1)))
    else:
        mark("type expected")
    return x


# Procedure `typeIds()` parses
#
#     typedIds ::= ident {"," ident} ":" type {"," ident {"," ident} ":" type}.
#
# and updates the top scope of symbol table; an error is reported if an identifier is already in the top scope.


def typedIds(adtName=None):
    if SC.sym == IDENT:
        tid = [SC.val]
        getSym()
    else:
        mark("identifier expected")
    while SC.sym == COMMA:
        getSym()
        if SC.sym == IDENT:
            tid.append(SC.val)
            getSym()
        else:
            mark("identifier expected")
    if SC.sym == COLON:
        getSym()
    else:
        mark("':' expected")
    tp = typ(adtName=adtName, parsingTypedIds=True).val
    for i in tid:
        newDecl(i, Var(tp))
    while SC.sym == COMMA:
        getSym()
        if SC.sym == IDENT:
            tid = [SC.val]
            getSym()
        else:
            mark("identifier expected")
        while SC.sym == COMMA:
            getSym()
            if SC.sym == IDENT:
                tid.append(SC.val)
                getSym()
            else:
                mark("identifier expected")
        if SC.sym == COLON:
            getSym()
        else:
            mark("':' expected")
        tp = typ(adtName=adtName, parsingTypedIds=True).val
        for i in tid:
            newDecl(i, Var(tp))


# Procedure `declarations(allocVar)` parses
#
#     declarations ::=
#         {"const" ident "=" expression}
#         {"type" ident "=" type}
#         {"var" typedIds}
#         {"procedure" ["(" ident ":" type ")"] ident "(" [typedIds] ")" [ "→" "(" typedIds ")" ] body}
#
# and updates the top scope of symbol table; an error is reported if an identifier is already in the top scope. An error is also reported if the expression of a constant declarations is not constant. For each procedure, a new scope is opened for its formal parameters and local declarations, the formal parameters and added to the symbol table, and code is generated for the body. The size of the variable declarations is returned, as determined by calling paramater `allocVar`.


def declarations(allocVar):
    while SC.sym == CONST:
        getSym()
        if SC.sym == IDENT:
            ident = SC.val
            getSym()
        else:
            mark("constant name expected")
        if SC.sym == EQ:
            getSym()
        else:
            mark("= expected")
        x = expression()
        if type(x) == Const:
            newDecl(ident, x)
        else:
            mark("expression not constant")
    while SC.sym == TYPE:
        getSym()
        if SC.sym == IDENT:
            ident = SC.val
            getSym()
        else:
            mark("type name expected")
        if SC.sym == EQ:
            getSym()
        else:
            mark("= expected")
        x = typ(ident)
        newDecl(ident, x)  #  x is of type ST.Type
    start = len(topScope())
    while SC.sym == VAR:
        getSym()
        typedIds()
    var = allocVar(topScope(), start)
    while SC.sym == PROCEDURE:
        getSym()
        if SC.sym == LPAREN:
            getSym()
            if SC.sym == IDENT:
                r = SC.val
                getSym()
            else:
                mark("identifier expected")
            if SC.sym == COLON:
                getSym()
            else:
                mark("':' expected")
            tp = typ().val
            if SC.sym == RPAREN:
                getSym()
            else:
                mark(") expected")
        else:
            r = None
        if SC.sym == IDENT:
            ident = SC.val
            getSym()
        else:
            mark("procedure name expected")
        newDecl(ident, Proc([], []))  #  entered without parameters
        sc = topScope()
        openScope()  # new scope for parameters and body
        if r:
            newDecl(r, Var(tp))
        if SC.sym == LPAREN:
            getSym()
        else:
            mark("( expected")
        if SC.sym == IDENT:
            typedIds()
        fp = topScope()
        if SC.sym == RPAREN:
            getSym()
        else:
            mark(") expected")
        d = len(fp)
        if SC.sym == RARROW:
            getSym()
            if SC.sym == LPAREN:
                getSym()
            else:
                mark("( expected")
            typedIds()
            if SC.sym == RPAREN:
                getSym()
            else:
                mark(") expected")
        sc[-1].par, sc[-1].res = fp[:d], fp[d:]  #  procedure parameters updated
        para = CG.genProcStart(ident, fp[:d], fp[d:])
        body(ident, para)
        closeScope()  #  scope for parameters and body closed
    return var


# Procedure `body` parses
#
#     body ::= INDENT declarationBlock (statementBlock | INDENT statementBlock DEDENT) DEDENT
#
# and returns the generated code if no error is reported.


def body(ident, para):
    if SC.sym == INDENT:
        getSym()
    else:
        mark("indent expected")
    start = len(topScope())
    local = declarations(CG.genLocalVars)
    CG.genProcEntry(ident, para, local)
    if SC.sym in FIRSTSTATEMENT:
        x = statementBlock()
    elif SC.sym == INDENT:
        getSym()
        x = statementBlock()
        if SC.sym == DEDENT:
            getSym()
        else:
            mark("dedent or new line expected")
    else:
        mark("statement expected")
    CG.genProcExit(x, para, local)
    if SC.sym == DEDENT:
        getSym()
    else:
        mark("dedent or new line expected")
    return x


# Procedure `program` parses
#
#     program ::= declarations "program" ident body
#
# and returns the generated code if no error is reported. The standard identifiers are entered initially in the symbol table.


def program():
    newDecl("boolean", Type(CG.genBool(Bool)))
    newDecl("integer", Type(CG.genInt(Int)))
    newDecl("true", Const(Bool, 1))
    newDecl("false", Const(Bool, 0))
    newDecl("read", StdProc([], [Var(Int)]))
    newDecl("write", StdProc([Var(Int)], []))
    newDecl("writeAscii", StdProc([Var(Int)], []))
    newDecl("writeAsciiLn", StdProc([Var(Int)], []))
    newDecl("writeln", StdProc([Var(Int)], []))
    newDecl("writeNewLine", StdProc([], []))
    CG.genProgStart()
    declarations(CG.genGlobalVars)
    if SC.sym == PROGRAM:
        getSym()
    else:
        print(SC.sym, SC.val)
        mark("'program' expected")
    ident = SC.val
    if SC.sym == IDENT:
        getSym()
    else:
        mark("program name expected")
    openScope()
    CG.genProgEntry(ident)
    x = body(ident, 0)
    closeScope()
    x = CG.genProgExit(x)
    return x


# Procedure `compileString(src, dstfn, target)` compiles the source as given by string `src`; if `dstfn` is provided, the code is written to a file by that name, otherwise printed on the screen. If `target` is omitted, MIPS code is generated.


def compileString(src, dstfn=None, target="wat") -> Bool:
    global CG
    if target == "wat":
        import CGwat as CG
    else:
        print("unknown target")
        return
    try:
        SC.init(src)
        ST.init()
        p = program()
        if dstfn == None:
            print(p)
        else:
            with open(dstfn, "w") as f:
                f.write(p)
    except Exception as msg:
        # raise Exception(str(msg))
        print(msg)
        return False
    return True
