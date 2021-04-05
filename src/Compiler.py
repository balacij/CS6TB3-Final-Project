from P0 import compileString
from ST import printSymTab


def runpywasm(wasmFile):
    import pywasm

    def write(s, i):
        print(i, end='')

    def writeChar(s, i):
        print(chr(i), end='')

    def writeCharLn(s, i):
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
                "writeChar": writeChar,
                "writeCharLn": writeCharLn,
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

    def writeChar(i: int):
        print(chr(i), end='')

    def writeCharLn(i: int):
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
            "writeChar": Function(store, writeChar),
            "writeCharLn": Function(store, writeCharLn),
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


def printHelp():
    print('P0 Compiler usage:')
    print('python Compile.py <file> [--run] [--runtime=<pywasm/wasmer>; defaults to `wasmer`]')


if __name__ == "__main__":
    import sys
    args = sys.argv

    if len(args) < 2 or len(args) > 4:
        printHelp()
        exit()
    
    targetName = args[1]
    if targetName == '--help':
        printHelp()
        exit(0)
    
    args = args[2:]
    run = False
    runtime = 'wasmer'

    for arg in args:
        if arg == '--run':
            run = True
        elif arg.startswith('--runtime'):
            if '=' in arg:
                runtime = arg[arg.index('=')+1:]
                if runtime not in {'pywasm', 'wasmer'}:
                    print(f'invalid runtime: {runtime}')
                    printHelp()
                    exit(0)
                elif runtime == 'pywasm':
                    print('*** WARNING *** Running with `pywasm` is discouraged! See NOTES.md for more information.')
            else:
                print(f'malformed runtime designation, please designate runtime using `--runtime=<pywasm/wasmer>`  (without the <>!)')
                exit(0)
        else:
            print(f'invalid argument: {arg}')
            printHelp()
            exit()

    main(targetName=targetName, run=run, runtime=runtime)
