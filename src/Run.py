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


def main(targetName, run=False, runtime='wasmer'):
    if not targetName.endswith('.p'):
        print('target file must end in ".p"')
        exit(0)

    with open(targetName, "r") as f:
        src = f.read()

    dstfn = targetName[:-2] + ".wat"

    if compileString(src, dstfn) and run:
        wat2wasmAndRun(dstfn, runtime=runtime)


def wat2wasmAndRun(targetName, runtime='wasmer'):
    import os

    wasmFile = targetName[:-4] + ".wasm"
    ec = os.system(f'wat2wasm "{targetName}" --output={wasmFile}')
    if ec == 0:
        runner = None
        if runtime == 'wasmer':
            runner = runwasmer
        elif runtime == 'pywasm':
            runner = runpywasm
        else:
            print('invalid runtime selected; only currently supporting `pywasm` and `wasmer`')
            exit(0)

        runner(f"{wasmFile}")
    else:
        print("failed to compile to wasm")
        print(ec)


if __name__ == "__main__":
    # TODO: add --clean option
    # TODO: add --runtime option
    # TODO: add --run option
    import sys

    if len(sys.argv) != 2:
        print('P0 Compiler usage:')
        print('python Run.py <file>')
        exit()

    main(targetName=sys.argv[1], run=True, runtime='wasmer')
