# Tests

In addition to porting over the original tests by Dr. Sekerinski, I've built this testing setup to allow for rapidly testing many tests at once.

This is constructed in such a way that testing files are sorted into parsing, running, type checking, scanner, and symbol table checks.

The majority of the scanner and symbol table checks are fairly simple and straightforward to test. As such, I've just added the majority of them into the original testing files. However, the other ones are not quite as easy to test, which is why we have this elaborate testing setup.

## `.p <-> .p.expect`

Each `.p` file in this folder can be thought of as a testing stub. The related `.p.expect` file is what we test test runs of these `.p` files against. The `.p.expect` are considered stable and what we expect.

## Testing

If you'd like to run the testing suite, please change you working directory to the `src` folder, enter the virtual environment as per the instructions for the normal compiler usage, and run `sh new_tests.sh`. After testing, if you choose not to clean your local files, there will be leftover `.wat`, `.wasm`, and `.runlog` files. If any of the tests failed, please check the related `.runlog`, `.p.expect` file, and `.p` source code file for all related information.

## Adding new tests

To create new tests, please run `sh gen_new_stub.sh` to generate a new stub using the `model.stub` file as a base. It will tell you what file it generated. Once you've made an appropriate testing stub (and tested it), please copy and paste the expected output into a new `.p.expect` file (with the same base file name). Alternatively, if you've made many tests and would like some assistance with this, please change your working directory back to `src`, run `sh new_tests.sh` (which will run all tests), and then run `sh stabilize_tests.sh` (which will create the related `.p.expect` files if they don't already exist). Finally, if you would like to rename your tests in bulk, please move back into the `tests` directory, run `python InteractiveRenameTests.py`, and follow the on-screen instructions.
