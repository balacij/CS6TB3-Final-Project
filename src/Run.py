from P0 import compileString
from ST import printSymTab


def runpywasm(wasmfile):
    import pywasm

    def write(s, i):
        print(i)

    def writeln(s):
        print("\n")

    def read(s):
        return int(input())

    vm = pywasm.load(wasmfile, {"P0lib": {"write": write, "writeln": writeln, "read": read}})


def runwasmer(wasmfile):
    from wasmer import engine, Store, Module, Instance, ImportObject, Function
    from wasmer_compiler_cranelift import Compiler

    def write(i: int):
        print(i)

    def writeln():
        print('\n')

    def read() -> int:
        return int(input())

    store = Store(engine.JIT(Compiler))
    module = Module(store, open(wasmfile, 'rb').read())
    import_object = ImportObject()
    import_object.register(
        "P0lib", {"write": Function(store, write), "writeln": Function(store, writeln), "read": Function(store, read)}
    )
    instance = Instance(module, import_object)


def main(targetName=None, run=False, runtime='wasmer'):
    target = None if targetName is None else f"{targetName}.wat"

    compileString(
        """
type Tree = Branch(left: Tree, right: Tree) | Leaf(value: integer)
type Maybe = Just(v: integer) | Nothing
type List = Cons(head: integer, tail: List) | Nil

type q = (a: boolean, b: integer, c: integer)
// type f = (a: q, b: boolean, c: integer)

// var tree: Tree
var mq: q

var maybe: Maybe
var tree: Tree

procedure weird(n: q)
    var r: q
    r.a := true
    r.b := 100
    r.c := 10000
    if r.b > 1 then write(n.b) else n.b := n.b - 1; weird(r)

procedure uptoList(n: integer) → (l: List)
    var tail: List
    if n < 1 then l ← Nil() else tail ← uptoList(n-1); write(n); l ← Cons(n, tail)

// procedure uptoList2(n: integer) → (l: List)
//     if n < 1 then l ← Nil() else write(n); l ← Cons(n, uptoList2(n-1))

// TODO: "uptoList2" and this below "weird2" have the same issue! In the current
// P0 implementation, we are not able to call functions in expressions!

// procedure weird2(n: integer) → (r: integer)
//     if n < 1 then r := 0 else r ← weird2(weird2(n-2))


program potato
    var left, right: Tree
    var mylist: List
    var x: integer
    mq.a := true
    mq.b := 10
    write(mq.b)
    mq.c := 1000
    maybe ← Just(10)
    maybe ← Nothing()
    left ← Leaf(1)
    right ← Leaf(2)
    tree ← Branch(tree, tree)  // TODO: while this is weird, I will consider the impacts of allowing it, since we are playing with pointers...
    tree ← Branch(left, right)

    mylist ← uptoList(1000)

    case maybe of {
        Just: x := 100; x := 10
        Nothing: x := 0
    }

    """,
        dstfn=target,
    )
    # TODO: Right now, I'm being a little bit inconsistent
    #       with how I define the types and how I instantiate
    #       them, I should use parantheses both when defining and
    #       when creating it, because it's currently allowing you
    #       to write "Nothing" to define Nothing tag as part of
    #       "Maybe" but when you want to set some variable to
    #       "Maybe", you have to type in "x ← Nothing()"
    #                 -- hence, the inconsistency

    # TODO: Figure out where procedure calls can occur, and allow
    #       the same kind of mkADTKind generation in the same areas

    # TODO: "case"-like statements of the form:
    #
    #       case x of {
    #          Just:
    #             y := x.value
    #       }
    #

    # TODO: Figure out how we're going to handle un-initialized ADTs!!!

    if run and targetName is not None:
        import os

        ec = os.system(f"wat2wasm {target}")
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
    # main(targetName='potato', run=True, runtime='wasmer')
    main()
