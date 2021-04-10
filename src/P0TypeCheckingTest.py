# coding: utf-8

# ### P0 Type-Checking Tests
#
# #### Original Author: Emil Sekerinski, McMaster University, revised March 2021


from P0 import compileString
from ST import printSymTab


# #### Error "index out of bounds"


compileString(
    """
var x: [5 .. 7] → integer
program p
  x[4] := 3
"""
)


# #### Error "index not integer"


compileString(
    """
var x: [5 .. 7] → integer
program p
  x[x] := 3
"""
)


# #### Error "not an array"


compileString(
    """
program p
  var x: integer
    x[9] := 3
"""
)


# #### Error "not a field"


compileString(
    """
var v: (f: integer)
program p
    v.g := 4
"""
)


# #### Error "not a record"


compileString(
    """
program p
  var v: integer
    v.g := 4
"""
)


# #### Error "identifier expected"


compileString(
    """
var v: (f: integer)
program p
    v.3 := 4
"""
)


# #### Error: "'write' may not be used as an expression -- must have exactly 1 return value but 'write' has 0"


compileString(
    """
program p
  var x: integer
    x := write
"""
)


# #### Error "not boolean"


compileString(
    """
program p
  var b: boolean
    b := ¬ 3
"""
)


# #### Error "bad type"


compileString(
    """
program p
  var b: boolean
    b := 3 and true
"""
)


# #### Error "bad type"


compileString(
    """
program p
  var x: integer
    x := - true
"""
)


# #### Error "bad type"


compileString(
    """
program p
  var x: integer
    x := 3 + true
"""
)


# #### Error "bad type"


compileString(
    """
program p
  var b: boolean
    b := 3 > true
"""
)


# #### Error "variable for result expected"


compileString(
    """
program p
  read()
"""
)


# #### Error "variable identifier expected"


compileString(
    """
program p
  const c = 3
  var x: integer
    x, c := 5, 7
"""
)


# #### Error "duplicate variable identifier"


compileString(
    """
program p
  var x: integer
    x, x := 5, 7
"""
)


# #### Error "incompatible assignment"


compileString(
    """
program p
  var b: boolean
    b := 3
"""
)


# #### Error "unbalanced assignment"


compileString(
    """
program p
  var b: boolean
    b := true, false
"""
)


# #### Error "procedure identifier expected"


compileString(
    """
program p
  var x: integer
    x ← 3
"""
)


# #### Error "procedure expected"


compileString(
    """
program p
  var b: boolean
    b ← true
"""
)


# #### Error "incompatible call"


compileString(
    """
program p
  var b: boolean
    b ← read()
"""
)


# #### Error "unbalanced call"


compileString(
    """
procedure q()→(r, s: integer)
  r, s := 3, 5
program p
  var x: integer
    x ← q()
"""
)


# #### Error "procedure expected"


compileString(
    """
program p
  var b: boolean
    b ← integer()
"""
)


# #### Error "variable or procedure expected"


compileString(
    """
program p
  const c = 7
    c := 4
"""
)


# #### Error "incompatible parameter"


compileString(
    """
program p
  write(true)
"""
)


# #### Error "extra parameter"


compileString(
    """
program p
  writeNewLine(5)
"""
)


# #### Error "too few parameters"


compileString(
    """
procedure q(x, y: integer)
  writeln()
program p
  q(3, true)
"""
)


# #### Error "extra parameter"


compileString(
    """
program p
  write(5, 7)
"""
)


# #### Error "too few parameters"


compileString(
    """
program p
  write()
"""
)


# #### Error "boolean expected"


compileString(
    """
program p
  if 5 then writeln()
"""
)


# #### Error "boolean expected"


compileString(
    """
program p
  while 5 do writeln()
"""
)


# #### Error "type identifier expected"


compileString(
    """
type T = writeln
program p
  writeln()
"""
)


# #### Error "bad lower bound"


compileString(
    """
const l = -1
const u = 5
var a: [l .. u] → integer
program p
  writeln()
"""
)


# #### Error "bad upper bound"


compileString(
    """
const l = 7
const u = 5
var a: [l .. u] → integer
program p
  writeln()
"""
)


# #### Error "expression not constant"


compileString(
    """
var v: integer
program p
  const c = v
  writeln()
"""
)

# TODO: Add ADT-related, case-related cases
