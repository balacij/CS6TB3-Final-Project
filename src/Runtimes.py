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
