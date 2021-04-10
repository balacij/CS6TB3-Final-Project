from P0 import compileString
from ST import printSymTab


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
        from Runtimes import runwasmer, runpywasm
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
                    print('*** WARNING *** Running with `pywasm` is discouraged! See docs/RUNTIMES.md for more information.')
            else:
                print(f'malformed runtime designation, please designate runtime using `--runtime=<pywasm/wasmer>`  (without the <>!)')
                exit(0)
        else:
            print(f'invalid argument: {arg}')
            printHelp()
            exit()

    main(targetName=targetName, run=run, runtime=runtime)
