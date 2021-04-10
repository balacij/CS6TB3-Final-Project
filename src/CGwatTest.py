# coding: utf-8


# ### P0 WebAssembly Code Generator Tests
#
# #### Original Author: Emil Sekerinski, McMaster University, revised March 2021

from P0 import compileString
from ST import printSymTab


compileString(
    """
type A = [2 .. 9] → integer
var a: A
procedure (r: A) q()
  r[2] := 7
program p
  writeNewLine() //a.q()
""", 'assign1.wat', target='wat')


# #### Error: "WASM: no nested procedures"
print("EXPECTING: WASM: no nested procedures")


compileString(
    """
program p
  procedure q()
    writeln(5)
  q()
""",

    target='wat',
)


# #### Error: "WASM: set too large"
print("EXPECTING: WASM: set too large")


compileString(
    """
var s: set [0..100]
program p
  writeNewLine()
"""
)


# #### Assignment
# ```
# (module
# (import "P0lib" "write" (func $write (param i32)))
# (import "P0lib" "writeln" (func $writeln))
# (import "P0lib" "read" (func $read (result i32)))
# (func $program
# (local $x i32)
# call $read
# local.set $x
# i32.const 3
# local.get $x
# i32.mul
# local.set $x
# local.get $x
# call $write
# call $writeln
# local.get $x
# i32.const 5
# i32.mul
# call $write
# )
# (memory 1)
# (start $program)
# )
# ```


compileString(
    """
var a: [2 .. 9] → integer
program p
  var x, y: integer
    a[3] := 5
    x, y := a[3], 7
    x, y := y, x
    writeln(x); writeln(y) // writes 7, 5
""",
    'assign.wat',
    target='wat',
)


# #### Relational Operators
#
# ```
# (module
# (import "P0lib" "write" (func $write (param i32)))
# (import "P0lib" "writeln" (func $writeln))
# (import "P0lib" "read" (func $read (result i32)))
# (func $q (param $b i32)
# local.get $b
# i32.const 0
# i32.eq
# local.set $b
# )
# (func $program
# (local $x i32)
# local.get $x
# i32.const 7
# i32.gt_s
# call $q
# )
# (memory 1)
# (start $program)
# )
# ```


compileString(
    """
procedure q(b: boolean)
  b := b = false
program p
  var x: integer
    q(x > 7)
""",
    'relop.wat',
    target='wat',
)


# #### Input & Output
# ```
# (module
# (import "P0lib" "write" (func $write (param i32)))
# (import "P0lib" "writeln" (func $writeln))
# (import "P0lib" "read" (func $read (result i32)))
# (func $program
# (local $x i32)
# call $read
# local.set $x
# i32.const 3
# local.get $x
# i32.mul
# local.set $x
# local.get $x
# call $write
# call $writeln
# local.get $x
# i32.const 5
# i32.mul
# call $write
# )
# (memory 1)
# (start $program)
# )
# ```

compileString(
    """
program p
  var x: integer
    x ← read(); x := 3 × x
    writeln(x); writeNewLine()
    writeln(x × 5)
""",
    'write.wat',
    target='wat',
)


# #### Parameter Passing
# ```
# (module
# (import "P0lib" "write" (func $write (param i32)))
# (import "P0lib" "writeln" (func $writeln))
# (import "P0lib" "read" (func $read (result i32)))
# (func $q (param $b i32) (param $c i32)
# local.get $b
# call $write
# local.get $c
# call $write
# )
# (func $r  (result i32)
# (local $d i32)
# i32.const 8
# i32.const 9
# i32.store
# i32.const 5
# local.set $d
# local.get $d)
# (func $program
# (local $x i32)
# i32.const 4
# i32.const 7
# i32.store
# i32.const 3
# i32.const 4
# i32.load
# call $q
# call $r
# local.set $x
# local.get $x
# call $write
# i32.const 8
# i32.load
# call $write
# )
# (memory 1)
# (start $program)
# )
# ```

compileString(
    """
type T = [1..10] → integer
var a: T
procedure q(b: integer, c: integer)
    writeln(b); writeln(c)
procedure r() → (d: integer)
    a[3] := 9; d := 5
program p
  var x: integer
  a[2] := 7; q(3, a[2]) // writes 3, 7
  x ← r(); writeln(x); writeln(a[3]) // writes 5, 9
""",
    'params.wat',
    target='wat',
)


# #### Arrays and Records


compileString(
    """
type A = [1 .. 7] → integer
type R = (f: integer, g: A, h: integer)
var v: A
var w: R
var x: integer
program p
  x := 9
  w.h := 12 - 7; writeln(w.h) // writes 5
  v[1] := 3; writeln(v[x - 8]) //writes 3
  w.g[x div 3] := 9; writeln(w.g[3]) // writes 9
  v[x - 2] := 7; w.g[x - 3] := 7
  writeln(v[7]); writeln(w.g[6]) // writes 7, 7
""",
    'arrayrec.wat',
    target='wat',
)



# #### Array Copies

# Following tests copy arrays and records. P0 generates `memory.copy` instructions, which are not supported by pywasm, but are supported by Chrome. For conversion of textual to binary WebAssembly, `wat2wasm` needs the `enable-bulk-memory` flag.


def runwasm(wasmfile):
    from IPython.core.display import display, Javascript

    display(
        Javascript(
            """
    const params = { 
        P0lib: { 
            write: i => this.append_stream({text: '' + i, name: 'stdout'}),
            writeln: () => this.append_stream({text: '\\n', name: 'stdout'}),
            read: () => window.prompt()
        }
    }
    fetch('"""
            + wasmfile
            + """') // asynchronously fetch file, return Response object
      .then(response => response.arrayBuffer()) // read the response to completion and stores it in an ArrayBuffer
      .then(code => WebAssembly.compile(code)) // compile (sharable) code.wasm
      .then(module => WebAssembly.instantiate(module, params)) // create an instance with memory
    // .then(instance => instance.exports.program()); // run the main program; not needed if start function specified
    """
        )
    )


# ```
# (module
# (import "P0lib" "write" (func $write (param i32)))
# (import "P0lib" "writeln" (func $writeln))
# (import "P0lib" "read" (func $read (result i32)))
# (global $_memsize (mut i32) i32.const 72)
# (func $program
# (local $0 i32)
# i32.const 40
# i32.const 3
# i32.store
# i32.const 44
# i32.const 5
# i32.store
# i32.const 8
# i32.const 40
# i32.const 32
# memory.copy
# i32.const 8
# i32.load
# call $write
# i32.const 12
# i32.load
# call $write
# i32.const 16
# i32.load
# call $write
# )
# (memory 1)
# (start $program)
# )
# ```


compileString(
    """
var c: [0 .. 1] → integer
var a, b: [2 .. 9] → integer
program p
  b[2] := 3; b[3] := 5
  a := b
  writeln(a[2]); writeln(a[3]); writeln(a[4]) // writes 3, 5, 0
""",
    'arraycopy.wat',
    target='wat',
)


compileString(
    """
type A = [2 .. 9] → integer
type B = [0 .. 1] → A
var b: B
procedure q(x: A) → (y: A)
    y := x; writeln(x[4]) // writes 0
program p
  b[1][2] := 3; b[1][3] := 5
  b[0] ← q(b[1])
  writeln(b[0][2]); writeln(b[0][3]) // writes 3, 5
""",
    'arrayvalueresult.wat',
    target='wat',
)



# ```
# (module
# (import "P0lib" "write" (func $write (param i32)))
# (import "P0lib" "writeln" (func $writeln))
# (import "P0lib" "read" (func $read (result i32)))
# (func $q (param $x i32)
# (local $y i32)
# (local $0 i32)
# (local $_fp i32)
# global.get $_memsize
# local.set $_fp
# global.get $_memsize
# i32.const 32
# i32.add
# local.tee $y
# global.set $_memsize
# local.get $y
# local.get $x
# i32.const 32
# memory.copy
# i32.const 2
# i32.const 2
# i32.sub
# i32.const 4
# i32.mul
# local.get $x
# i32.add
# i32.load
# call $write
# i32.const 3
# i32.const 2
# i32.sub
# i32.const 4
# i32.mul
# local.get $x
# i32.add
# i32.load
# call $write
# i32.const 4
# i32.const 2
# i32.sub
# i32.const 4
# i32.mul
# local.get $x
# i32.add
# i32.load
# call $write
# local.get $_fp
# global.set $_memsize
# )
# (global $_memsize (mut i32) i32.const 0)
# (func $program
# (local $b i32)
# (local $0 i32)
# (local $_fp i32)
# global.get $_memsize
# local.set $_fp
# global.get $_memsize
# i32.const 64
# i32.add
# local.tee $b
# global.set $_memsize
# i32.const 1
# i32.const 32
# i32.mul
# local.get $b
# i32.add
# i32.const 2
# i32.const 2
# i32.sub
# i32.const 4
# i32.mul
# i32.add
# i32.const 3
# i32.store
# i32.const 1
# i32.const 32
# i32.mul
# local.get $b
# i32.add
# i32.const 3
# i32.const 2
# i32.sub
# i32.const 4
# i32.mul
# i32.add
# i32.const 5
# i32.store
# i32.const 1
# i32.const 32
# i32.mul
# local.get $b
# i32.add
# call $q
# local.get $_fp
# global.set $_memsize
# )
# (memory 1)
# (start $program)
# )
# ```


compileString(
    """
type A = [2 .. 9] → integer
type B = [0 .. 1] → A
procedure q(x: A)
  var y: A
    y := x
    writeln(x[2]); writeln(x[3]); writeln(x[4]) // writes 3, 5, 0
program p
  var b: B
    b[1][2] := 3; b[1][3] := 5
    q(b[1])
""",
    'localarray.wat',
    target='wat',
)



# #### Booleans and Conditions


compileString(
    """
program p
  const five = 5
  const seven = 7
  const always = true
  const never = false
  var x, y, z: integer
  var b, t, f: boolean
    x := seven; y := 9; z := 11; t := true; f := false
    if true then writeln(7) else writeln(9)    // writes 7
    if false then writeln(7) else writeln(9)   // writes 9
    if t then writeln(7) else writeln(9)       // writes 7
    if f then writeln(7) else writeln(9)       // writes 9
    if ¬ t then writeln(7) else writeln(9)     // writes 9
    if ¬ f then writeln(7) else writeln(9)     // writes 7
    if t or t then writeln(7) else writeln(9)  // writes 7
    if t or f then writeln(7) else writeln(9)  // writes 7
    if f or t then writeln(7) else writeln(9)  // writes 7
    if f or f then writeln(7) else writeln(9)  // writes 9
    if t and t then writeln(7) else writeln(9) // writes 7
    if t and f then writeln(7) else writeln(9) // writes 9
    if f and t then writeln(7) else writeln(9) // writes 9
    if f and f then writeln(7) else writeln(9) // writes 9
    writeNewLine()
    b := true
    if b then writeln(3) else writeln(5) // writes 3
    b := false
    if b then writeln(3) else writeln(5) // writes 5
    b := x < y
    if b then writeln(x) else writeln(y) // writes 7
    b := (x > y) or t
    if b then writeln(3) else writeln(5) // writes 3
    b := (x > y) or f
    if b then writeln(3) else writeln(5) // writes 5
    b := (x = y) or (x > y)
    if b then writeln(3) else writeln(5) // writes 5
    b := (x = y) or (x < y)
    if b then writeln(3) else writeln(5) // writes 3
    b := f and (x ≥ y)
    if b then writeln(3) else writeln(5) // writes 5
    writeNewLine()
    while y > 3 do                   // writes 9, 8, 7, 6, 5, 4
      writeln(y); y := y - 1
    writeln(y); writeNewLine()              // writes 3
    if ¬(x < y) and t then
      writeln(x)                       // writes 7
""",
    'cond.wat',
    target='wat',
)




# #### Constant Folding, Local & Global Variables
#
# ```
# (module
# (import "P0lib" "write" (func $write (param i32)))
# (import "P0lib" "writeln" (func $writeln))
# (import "P0lib" "read" (func $read (result i32)))
# (global $x (mut i32) i32.const 0)
# (global $y (mut i32) i32.const 0)
# (func $q
# (local $x i32)
# i32.const 3
# local.set $x
# i32.const 1
# if
# local.get $x
# global.set $y
# else
# i32.const 7
# global.set $y
# end
# global.get $y
# call $write
# i32.const 0
# if
# local.get $x
# global.set $y
# else
# i32.const 7
# global.set $y
# end
# global.get $y
# call $write
# i32.const 1
# if
# local.get $x
# global.set $y
# else
# i32.const 7
# global.set $y
# end
# global.get $y
# call $write
# i32.const 0
# if
# local.get $x
# global.set $y
# else
# i32.const 7
# global.set $y
# end
# global.get $y
# call $write
# i32.const 0
# if
# i32.const 5
# call $write
# else
# i32.const 9
# call $write
# end
# )
# (func $program
# i32.const 7
# global.set $x
# call $q
# global.get $x
# call $write
# )
# (memory 1)
# (start $program)
# )
# ```


compileString(
    """
const seven = (9 mod 3 + 5 × 3) div 2
type int = integer
var x, y: integer
procedure q()
  const sotrue = true and true
  const sofalse = false and true
  const alsotrue = false or true
  const alsofalse = false or false
  var x: int
    x := 3
    if sotrue then y := x else y := seven
    writeln(y) // writes 3
    if sofalse then y := x else y := seven
    writeln(y) // writes 7
    if alsotrue then y := x else y := seven
    writeln(y) // writes 3
    if alsofalse then y := x else y := seven
    writeln(y) // writes 7
    if ¬(true or false) then writeln(5) else writeln(9) // writes 9
program p
  x := 7; q(); writeln(x) // writes 7
""",
    'folding.wat',
    target='wat',
)


# #### Procedures
# ```
# (module
# (import "P0lib" "write" (func $write (param i32)))
# (import "P0lib" "writeln" (func $writeln))
# (import "P0lib" "read" (func $read (result i32)))
# (global $g (mut i32) i32.const 0)
# (func $q (param $v i32)
# (local $l i32)
# i32.const 9
# local.set $l
# local.get $l
# local.get $v
# i32.gt_s
# if
# local.get $l
# call $write
# else
# global.get $g
# call $write
# end
# )
# (func $program
# i32.const 5
# global.set $g
# i32.const 7
# call $q
# )
# (memory 1)
# (start $program)
# )
# ```


compileString(
    """
var g: integer          // global variable
procedure q(v: integer) // value parameter
  var l: integer        // local variable
    l := 9
    if l > v then writeln(l) // writes 9
    else writeln(g)
program p
  g := 5; q(7)
""",
    'proc.wat',
    target='wat',
)


# #### Illustrating Lack of Optimization
# ```
# (module
# (import "P0lib" "write" (func $write (param i32)))
# (import "P0lib" "writeln" (func $writeln))
# (import "P0lib" "read" (func $read (result i32)))
# (func $program
# (local $x i32)
# i32.const 5
# local.set $x
# local.get $x
# i32.const 0
# i32.add
# local.set $x
# i32.const 0
# local.get $x
# i32.add
# local.set $x
# local.get $x
# i32.const 1
# i32.mul
# local.set $x
# i32.const 1
# local.get $x
# i32.mul
# local.set $x
# local.get $x
# i32.const 3
# i32.add
# local.set $x
# i32.const 3
# local.get $x
# i32.add
# local.set $x
# )
# (memory 1)
# (start $program)
# )
# ```


compileString(
    """
program p
  var x: integer
    x := 5
    x := x + 0
    x := 0 + x
    x := x × 1
    x := 1 × x
    x := x + 3
    x := 3 + x
""",
    'opt.wat',
    target='wat',
)




# #### Two-dimensional Array
# ```
# (module
# (import "P0lib" "write" (func $write (param i32)))
# (import "P0lib" "writeln" (func $writeln))
# (import "P0lib" "read" (func $read (result i32)))
# (global $y (mut i32) i32.const 0)
# (global $b (mut i32) i32.const 0)
# (func $program
# global.get $y
# i32.const 3
# i32.sub
# i32.const 11
# i32.mul
# i32.const 0
# i32.add
# i32.const 4
# i32.add
# i32.const 0
# i32.store
# global.get $y
# i32.const 3
# i32.sub
# i32.const 11
# i32.mul
# i32.const 0
# i32.add
# global.get $y
# i32.const 1
# i32.add
# i32.const 1
# i32.sub
# i32.const 1
# i32.mul
# i32.add
# i32.load
# global.set $b
# )
# (memory 1)
# (start $program)
# )
# ```


compileString(
    """
type R = boolean
type S = [1..11] → R
type T = [3..9] → S
var x: T
var y: integer
var b: boolean
program p
  x[y][5] := false
  b := x[y][y + 1]
""",
    'twoD.wat',
    target='wat',
)



# #### Array Parameters
# ```
# (module
# (import "P0lib" "write" (func $write (param i32)))
# (import "P0lib" "writeln" (func $writeln))
# (import "P0lib" "read" (func $read (result i32)))
# (func $r (param $a i32)
# (local $0 i32)
# i32.const 4
# i32.const 3
# i32.sub
# i32.const 4
# i32.mul
# local.get $a
# i32.add
# i32.load
# call $write
# i32.const 8
# i32.const 3
# i32.sub
# i32.const 4
# i32.mul
# local.get $a
# i32.add
# i32.const 7
# i32.store
# )
# (func $q (param $a i32)
# (local $0 i32)
# local.get $a
# call $r
# i32.const 8
# i32.const 3
# i32.sub
# i32.const 4
# i32.mul
# local.get $a
# i32.add
# i32.load
# call $write
# i32.const 6
# i32.const 3
# i32.sub
# i32.const 4
# i32.mul
# local.get $a
# i32.add
# i32.const 5
# i32.store
# )
# (func $program
# (local $0 i32)
# i32.const 4
# i32.const 3
# i32.store
# i32.const 0
# call $q
# i32.const 12
# i32.load
# call $write
# )
# (memory 1)
# (start $program)
# )
# ```


compileString(
    """
type T = [3..9] → integer
var x: T
procedure r(a: T)
  writeln(a[4]); a[8] := 7       // writes 3
procedure q(a: T)
  r(a); writeln(a[8]); a[6] := 5 // writes 7
program p
  x[4] := 3; q(x); writeln(x[6]) // writes 5
""",
    'arraypara.wat',
    target='wat',
)


# #### Sets


compileString(
    """
type S = set [1..10]
procedure elements(s: S)
  var i: integer
    writeNewLine(); i := 0
    while i < 32 do
      if i ∈ s then writeln(i)
      i := i + 1
procedure difference(s: S, t: S) → (u: S)
  u := s ∩ ∁t
program p
  var s: S
    s := {3}; elements(s) // writes 3
    s := s ∪ {1, 9}; elements(s) // writes 1, 3, 9
    s := ∁s; elements(s) // writes 2, 4, 5, 6, 7, 8, 10
    s := s ∩ {5, 7, 9}; elements(s) // writes 5, 7
    s ← difference(s, {7, 8, 9}); elements(s) // writes 5
    writeNewLine(); if s ⊆ {2, 5, 20} then writeln(#s) // writes 1
    if {2, 5} ⊆ s then writeln(-1) else writeln(-2) // writes -2
    
""",
    'sets.wat',
    target='wat',
)

