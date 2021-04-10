# coding: utf-8

# ### P0 Parsing Tests
#
# #### Original Author: Emil Sekerinski, McMaster University, revised March 2021


from P0 import compileString
from ST import printSymTab


# #### Error "] expected"


compileString(
    """
var a: [1..10] → integer
var x: integer
program p
    x := a[4
"""
)


# #### Error ") expected"


compileString(
    """
program p
  var x: integer
    x := (5
"""
)


# #### Error "expression expected"


compileString(
    """
program p
  var x: integer
    x := +
"""
)


# #### Error "new line expected"


compileString(
    """
program p
  writeln(5) writeln(7)
"""
)


# #### Error "dedent or new line expected"


compileString(
    """
program p
  writeln(5)
    writeln(7)
"""
)


# #### Error "indented statement expected"


compileString(
    """
procedure p()
  if 3 > 4 then
writeln()
"""
)


# #### Error "variable for result expected"


compileString(
    """
program p
  read()
"""
)


# #### Error ":= or ← expected"


compileString(
    """
var a: [5 .. 7] → integer
program p
  var b: boolean
    a[5] +
"""
)


# #### Error "'(' expected"


compileString(
    """
program p
  writeln
"""
)


# #### Error "')' expected"


compileString(
    """
program p
  writeln(
"""
)


# #### Error "'then' expected"


compileString(
    """
program p
  if true writeln(5)
"""
)


# #### Error "'do' expected"


compileString(
    """
program p
  while true writeln(5)
"""
)


# #### Error "statement expected"


compileString(
    """
program p
  writeln(3); const c = 5
"""
)


# #### Error "'..' expected"


compileString(
    """
var a: [5 → integer
program p
  writeln()
"""
)


# #### Error "']' expected"


compileString(
    """
var a: [5..7 → integer
program p
  writeln()
"""
)


# #### Error "'→' expected"


compileString(
    """
var a: [3 .. 7] integer
program p
  writeln()
"""
)


# #### Error "type expected"


compileString(
    """
program p
  var x: if
"""
)


# #### Error "identifier expected"


compileString(
    """
program p
  var if: integer
"""
)


# #### Error "identifier expected"


compileString(
    """
program p
  var if: integer
"""
)


# #### Error "identifier expected"


compileString(
    """
program p
  var x, if: integer
"""
)


#
# #### Error "':' expected"


compileString(
    """
program p
  var x integer
"""
)


# #### Error "identifier expected"


compileString(
    """
program p
  var i, j: integer, if: boolean
"""
)


# #### Error "identifier expected"


compileString(
    """
program p
  var i, j: integer, b, if: boolean
"""
)


# #### Error "constant name expected"


compileString(
    """
program p
  const 5 = 7
  writeln(3)
"""
)


# #### Error "= expected"


compileString(
    """
program p
  const c: 5
  writeln(5)
"""
)


# #### Error "type name expected"


compileString(
    """
program p
  type 5 = integer
  writeln(3)
"""
)


# #### Error "= expected"


compileString(
    """
program p
  type T: integer
  writeln()
"""
)


# #### Error  "procedure name expected"


compileString(
    """
procedure
  writeln()
program p
  writeln()
"""
)


# #### Error  "( expected"


compileString(
    """
procedure q
  writeln()
program p
  writeln()
"""
)


# #### Error  ") expected"


compileString(
    """
procedure q(
  writeln()
program p
  writeln()
"""
)


# #### Error  "( expected"


compileString(
    """
procedure q(x: integer) → boolean
  writeln()
program p
  writeln()
"""
)


# #### Error  ") expected"


compileString(
    """
procedure q(x: integer) → (y: boolean
  writeln()
program p
  writeln()
"""
)


# #### Error  "indent or new line expected"


compileString(
    """
program p
writeNewLine()
"""
)


# #### Error "dedent or new line expected"


compileString(
    """
program p
  const c = 5
    writeNewLine()
      writeNewLine()
"""
)


# #### Error "statement expected"


compileString(
    """
program p
  program q
"""
)


# #### Error "dedent or new line expected"


compileString(
    """
program p
  writeNewLine()
    writeNewLine()
"""
)


# #### Error "'program' expected'"


compileString(
    """
var x: integer
"""
)


# #### Error "program name expected"


compileString(
    """
program
  writeNewLine()
"""
)


# #### Multiple Indentations
#
# ```
# (module
# (import "P0lib" "write" (func $write (param i32)))
# (import "P0lib" "writeln" (func $writeln))
# (import "P0lib" "read" (func $read (result i32)))
# (func $q
# (local $b i32)
# i32.const 1
# local.set $b
# local.get $b
# if
# i32.const 3
# call $writeln
# else
# i32.const 5
# call $writeln
# end
# local.get $b
# i32.eqz
# if
# i32.const 5
# call $writeln
# else
# local.get $b
# if
# i32.const 7
# call $writeln
# else
# i32.const 9
# call $writeln
# end
# end
# loop
# local.get $b
# if
# local.get $b
# if
# i32.const 0
# local.set $b
# i32.const 1
# call $writeln
# end
# br 1
# end
# end
# )
# (func $program
# i32.const False
# if
# call $writeNewLine
# else
# call $q
# end
# )
# (memory 1)
# (start $program)
# )
# ```


compileString(
    """
procedure q()
  var b: boolean
    b := true
    if b then writeln(3)
    else writeln(5)
    if ¬b then writeln(5)
    else if b then writeln(7)
    else writeln(9)
    while b do
      if b then
        b := false; writeln(1)
program p
  if 3 > 4 then writeNewLine() else
    q()
"""
)
