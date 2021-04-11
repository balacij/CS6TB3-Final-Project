# Standard Procedures

We've changed the functionality of the standard built-in procedures as follows:

| Name           | Inputs  | Outputs | Description                                                                                                   | 
|----------------|---------|---------|---------------------------------------------------------------------------------------------------------------|
| `read`         | -       | `i32`   | Reads single input from standard input                                                                        |
| `write`        | `i32`   | -       | Writes single integer to standard output                                                                      |
| `writeln`      | `i32`   | -       | Writes single integer to standard output with a newline character afterwards                                  |
| `writeChar`    | `i32`   | -       | Writes single integer converted into a utf-8 character to standard output with a newline character afterwards |
| `writeCharLn`  | `i32`   | -       | Writes single integer converted into a utf-8 character to standard output with a newline character afterwards |
| `writeNewLine` | -       | -       | Writes single newline character to standard output                                                            |

##### Note: `i32` is represented by an `integer` in P0.
