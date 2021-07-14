# P0 Compiler

## Documentation

Please see the <a href="../docs/README.md">`../docs`</a> folder for all information related to this project.

## Usage
### Prerequisites
You will need to have a working installation of:
* Python 3.7+
* `pip`
* `virtualenv`
* `wat2wasm`

### Setup environment
Please carefully read and follow these instructions:
1. Open up a terminal window and move into the `src` directory<br>`cd src`
2. Open up a new Python virtual environment if you haven't already created one for the project.<br>`virtualenv -v .venv/`
3. Open up the virtual environment.<br>`source .venv/bin/activate`
4. If you haven't previously installed the project required libraries, please do so using:<br>`pip install -r requirements.txt`

### Run
Before running, please ensure that your environment is in working order and that you have a `.p` suffixed P0 program nearby and ready for compilation.

To view compiler usage information, please run `python Compiler.py --help`.

Using one of my pre-made examples, you may run the following commands:
1. Open up a terminal window and move into the `src` directory (if not already)<br>`cd src`
2. Open up the Python virtual environment (if not already)<br>`source .venv/bin/activate`
3. Compile and run the file<br>`python Compiler.py examples/lists.py --run` (or, you may designate another example or another file for it to compile)

**Alternatively**, if you would like to run all of the examples at once, please follow steps 1 & 2, and then run `sh run_examples.sh` (note: this script is written in bash, and, as such, you will need some sort of bash shell as a prerequisite if you would like to use it).

## Testing

### Original Tests

Each component of compiler has it's own testing suite built originally by Dr. Sekerinski. I've ported these tests, tweaked them to accommodate my changes to core P0, added new tests to them, and now they are all applicable.

Please run the related testing stub(s) for each component you would like to test using `python <testing_stub>`.

For example, if you would like to test parsing of the P0 language, please run `python P0ParsingTest.py` (assuming you're already using the virtualenv, otherwise, please follow the steps above).

### Additional tests

All of my tests are strictly related to P0 and it's interactions with my implementation of disjoint union types in it.

As such, I've differentiated my own from the original ones.

To test the project using my testing stubs, please run `sh run_new_tests.sh`.

Additionally, please visit <a href="tests/README.md">`tests/README.md`</a> for more information about the testing stubs.
