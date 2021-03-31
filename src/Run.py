from P0 import compileString
from ST import printSymTab


def runpywasm(wasmFile):
    import pywasm

    def write(s, i):
        print(i, end='')

    def writeAscii(s, i):
        print(chr(i), end='')

    def writeAsciiLn(s, i):
        print(chr(i))

    def writeln(s, i):
        print(i)

    def writeNewLine(s):
        print()

    def read(s):
        return int(input())

    vm = pywasm.load(
        wasmFile,
        {
            "P0lib": {
                "write": write,
                "writeAscii": writeAscii,
                "writeln": writeln,
                "writeNewLine": writeNewLine,
                "read": read,
            }
        },
    )


def runwasmer(wasmFile):
    from wasmer import engine, Store, Module, Instance, ImportObject, Function
    from wasmer_compiler_cranelift import Compiler

    def write(i: int):
        print(i, end='')

    def writeAscii(i: int):
        print(chr(i), end='')

    def writeAsciiLn(i: int):
        print(chr(i))

    def writeln(i: int):
        print(i)

    def writeNewLine():
        print()

    def read() -> int:
        return int(input())

    store = Store(engine.JIT(Compiler))
    module = Module(store, open(wasmFile, 'rb').read())
    import_object = ImportObject()
    import_object.register(
        "P0lib",
        {
            "write": Function(store, write),
            "writeAscii": Function(store, writeAscii),
            "writeAsciiLn": Function(store, writeAsciiLn),
            "writeln": Function(store, writeln),
            "writeNewLine": Function(store, writeNewLine),
            "read": Function(store, read),
        },
    )
    instance = Instance(module, import_object)


def main(targetName=None, run=False, runtime='wasmer'):
    target = None if targetName is None else f"{targetName}.wat"

    compileString(
        """
type Tree = Branch(left: Tree, right: Tree) | Leaf(value: integer)
type Maybe = Just(value: integer) | Nothing
type Either = Left(value: integer) | Right(value: boolean)
type List = Cons(head: integer, tail: List) | Nil

type RGB = Red | Green | Blue

type Expr = Add(left: Expr, right: Expr) | Sub(left: Expr, right: Expr) | Mul(left: Expr, right: Expr) | Div(num: Expr, den: Expr) | Pow(base: Expr, exponent: Expr) | Int(value: integer)

type q = (a: boolean, b: integer, c: integer)
// type f = (a: q, b: boolean, c: integer)

// var tree: Tree
var mq: q

// var maybe: Maybe
// var tree: Tree


// procedure weird(n: q)
//     var r: q
//     r.a := true
//     r.b := 100
//     r.c := 10000
//     if r.b > 1 then write(n.b) else n.b := n.b - 1; weird(r)

procedure five() → (n: integer)
    n := 5

procedure valOr(v: Maybe, n: integer) → (r: integer)
    case v of {
        Just:
            r := v.value
        Nothing:
            r := n
    }

procedure uptoList(n: integer) → (l: List)
    var tail: List
    if n < 1 then l ← Nil() else tail ← uptoList(n-1); writeln(n); l ← Cons(n, tail)

// procedure uptoList2(n: integer) → (l: List)
//     if n < 1 then l ← Nil() else writeln(n); l ← Cons(n, uptoList2(n-1))

// TODO: "uptoList2" and this below "weird2" have the same issue! In the current
// P0 implementation, we are not able to call functions in expressions!

procedure consumeList(l: List)
    var r: List
    case l of {
        Cons:
            writeln(l.head)
            r := l.tail
            consumeList(r)
    }

procedure rgbToHex(rgb: RGB) → (n: integer)
    case rgb of {
        Red:         // apparently we lost hex codes for integer representations :(
            n := 16711680    // 0xff0000
        Green:
            n := 65280       // 0x00ff00
        Blue:
            n := 255         // 0x0000ff
    }

procedure sumList(l: List) → (n: integer)
    case l of {
        Cons:
            n ← sumList(l.tail)
            n := n + l.head
        Nil:
            n := 0
    }

program potato
    // var left, right: Tree
    var mylist: List
    var maybe: Maybe
    var x: integer
    var colour: RGB
    var w: q
    w.a := true
    w.b := 88
    writeln(w.b)
    w.c := 10000
    writeln(w.c)
    mq.a := true
    mq.b := 10
    writeln(mq.b)
    mq.c := 1000
    writeln(mq.c)
    maybe ← Nothing()
    maybe ← Just(1111)
    // left ← Leaf(1)
    // right ← Leaf(2)
    // tree ← Branch(tree, tree)
    // tree ← Branch(left, right)

    mylist ← uptoList(5)

    case maybe of {
        Just: 
            x := maybe.value
            // maybe.value := 100
            maybe.value ← five()
            writeNewLine()
            writeln(maybe.value)
            writeln(x)
            writeNewLine()
        Nothing: x := 1000
    }

    consumeList(mylist)
    x ← sumList(mylist)
    writeln(x)

    colour ← Red()
    x ← rgbToHex(colour)
    writeln(x)

    colour ← Green()
    x ← rgbToHex(colour)
    writeln(x)

    colour ← Blue()
    x ← rgbToHex(colour)
    writeln(x)

    maybe ← Just(999)
    x ← valOr(maybe, 10000)
    writeln(x)

    maybe ← Nothing()
    x ← valOr(maybe, 10000)
    writeln(x)

    writeAscii(100)
    writeAsciiLn(101)
    writeAsciiLn(102)

    writeNewLine()

    writeln(100)

    """,
        dstfn=target,
    )

    if run and targetName is not None:
        compileAndRun(targetName, runtime=runtime)


def compileAndRun(targetName, runtime='wasmer'):
    import os

    ec = os.system(f"wat2wasm {targetName}.wat")

    if ec == 0:
        if runtime == 'wasmer':
            runwasmer(f"{targetName}.wasm")
        elif runtime == 'pywasm':
            runpywasm(f"{targetName}.wasm")
        else:
            print('invalid runtime selected; only currently supporting `pywasm` and `wasmer`')
            exit(0)
    else:
        print("failed to compile to wasm")
        print(ec)


if __name__ == "__main__":
    main(targetName='potato', run=True, runtime='wasmer')
    # main()
    # compileAndRun("potato", runtime='wasmer')
