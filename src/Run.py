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

    vm = pywasm.load(
        wasmfile, {"P0lib": {"write": write, "writeln": writeln, "read": read}}
    )


def main(targetName=None, run=False):
    target = None if targetName is None else f"{targetName}.wat"

    compileString(
        """
type Tree = Branch(left: Tree, right: Tree) | Leaf(value: integer)

type Maybe = Just(v: integer) | Nothing

type q = (a: boolean, b: integer, c: integer)
// type f = (a: q, b: boolean, c: integer)

// var tree: Tree
var mq: q

var maybe: Maybe

program potato
    mq.a := true
    mq.b := 10
    write(mq.b)
    mq.c := 1000
    """,
        dstfn=target,
    )

    if run and targetName is not None:
        import os

        ec = os.system(f"wat2wasm {target}")
        if ec == 0:
            runpywasm(f"{targetName}.wasm")
        else:
            print("failed to compile to wasm")
            print(ec)


if __name__ == "__main__":
    # main(targetName='potato', run=True)
    main()
