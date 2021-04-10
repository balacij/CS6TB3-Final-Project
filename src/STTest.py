# coding: utf-8

# ### P0 Symbol Table Tests
#
# #### Original Author: Emil Sekerinski, McMaster University, revised March 2021


from P0 import compileString
from ST import printSymTab


# #### Error "multiple definition"
print('EXPECTING: multiple definition error')

compileString(
    """
program p
  const x = 9
  var x : integer
    x := 7
"""
)


# #### Error "undefined identifier"
print('EXPECTING: undefined identifier error')

compileString(
    """
program p
  var y: bool
    y := true
"""
)


# #### Symbol Table Dump
#
# ```
# Type(name = boolean, val = <class 'ST.Bool'>)
# Type(name = integer, val = <class 'ST.Int'>)
# Const(name = true, tp = <class 'ST.Bool'>, val = 1)
# Const(name = false, tp = <class 'ST.Bool'>, val = 0)
# StdProc(name = read, lib = P0lib, lev = 0, par = [], res = [Var(name = , lev = , tp = <class 'ST.Int'>)])
# StdProc(name = write, lib = P0lib, lev = 0, par = [Var(name = , lev = , tp = <class 'ST.Int'>)], res = [])
# StdProc(name = writeChar, lib = P0lib, lev = 0, par = [Var(name = , lev = , tp = <class 'ST.Int'>)], res = [])
# StdProc(name = writeCharLn, lib = P0lib, lev = 0, par = [Var(name = , lev = , tp = <class 'ST.Int'>)], res = [])
# StdProc(name = writeln, lib = P0lib, lev = 0, par = [Var(name = , lev = , tp = <class 'ST.Int'>)], res = [])
# StdProc(name = writeNewLine, lib = P0lib, lev = 0, par = [], res = [])
# Const(name = N, tp = <class 'ST.Int'>, val = 10)
# Type(name = T, val = Array(lower = 1, length = 10, base = <class 'ST.Int'>))
# ADTKind(index = 1, name = Just, record = Type(name = , val = Record(fields = [Var(name = value, lev = 1, tp = <class 'ST.Int'>)])))
# ADTKind(index = 2, name = Nothing, record = None)
# Proc(name = __mk_Just, lev = 0, par = [Var(name = value, lev = 1, tp = <class 'ST.Int'>)], res = [Var(name = , lev = , tp = ADT(name = Maybe, kinds = [ADTKind(index = 1, name = Just, record = Type(name = , val = Record(fields = [Var(name = value, lev = 1, tp = <class 'ST.Int'>)]))), ADTKind(index = 2, name = Nothing, record = None)]))])
# Proc(name = __mk_Nothing, lev = 0, par = [], res = [Var(name = , lev = , tp = ADT(name = Maybe, kinds = [ADTKind(index = 1, name = Just, record = Type(name = , val = Record(fields = [Var(name = value, lev = 1, tp = <class 'ST.Int'>)]))), ADTKind(index = 2, name = Nothing, record = None)]))])
# Type(name = Maybe, val = ADT(name = Maybe, kinds = [ADTKind(index = 1, name = Just, record = Type(name = , val = Record(fields = [Var(name = value, lev = 1, tp = <class 'ST.Int'>)]))), ADTKind(index = 2, name = Nothing, record = None)]))
# Var(name = x, lev = -3, tp = Array(lower = 1, length = 10, base = <class 'ST.Int'>))
# Var(name = maybe, lev = 0, tp = ADT(name = Maybe, kinds = [ADTKind(index = 1, name = Just, record = Type(name = , val = Record(fields = [Var(name = value, lev = 1, tp = <class 'ST.Int'>)]))), ADTKind(index = 2, name = Nothing, record = None)]))
# Var(name = y, lev = 0, tp = <class 'ST.Bool'>)
# Var(name = z, lev = -3, tp = Record(fields = [Var(name = f, lev = 1, tp = <class 'ST.Int'>), Var(name = g, lev = 1, tp = <class 'ST.Bool'>)]))
# Proc(name = q, lev = 0, par = [Var(name = v, lev = 1, tp = <class 'ST.Bool'>)], res = [Var(name = r, lev = 1, tp = <class 'ST.Int'>)])
# ```


compileString(
    """
const N = 10
type T =  [1 .. N] → integer
type Maybe = Just(value: integer) | Nothing
var x: T
var maybe: Maybe
var y: boolean
var z: (f: integer, g: boolean)
procedure q(v: boolean) → (r: integer)
  var z: boolean
    z := false
program p
  var maybe: Maybe
  y := true
""",
    "/dev/null",
)  # discard target code
printSymTab()
