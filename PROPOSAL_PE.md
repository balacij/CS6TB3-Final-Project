# Project Proposal

## Topic
Partial Evaluation in P0

## Objective
The goal of this project is to add enable online partial evaluation in P0.

## Division of Work
As I am enrolled in 6TB3, I, Jason Balaci, will be the only team member and will be building the entire project by myself.

## Design
A partial evaluator in P0 would be implemented using an "online" style whereby it reasons about specializations as it tries to compile P0 programs into WebAssembly (or just before compiling), relying on the already constructed Abstract Syntax Tree for P0.

When compiling, an online partial evaluator tries to specialize the constructed program as it goes along. As Abstract Syntax Trees are "trees", early reasoning about program constructions starts with "later" parts of a program (generally the "ends"). All AST components are then divided into "static" and "dynamic" components. Static components are "constants" from which we can use to pre-compute/specialize components accordingly. For example, if we had some condition `if True then a := 5 else a := 3`, we know we can specialize this into `a := 5` as the `True` is constant (static) data that we may use to specialize the `if` statement. Since P0 is an imperative language, it contains mixed "pure" and "impure" code segments for which we will need to differentiate. Pure code is code that contains no side-effects, and impure code is code that contains side-effects.

There are many ways in which we can specialize code in P0, but here are a few:
1. All constants are static.
2. "read", "write", "writeln" are the builtin functions that are impure. However, we may still specialize their inputs if they are static and contain some non-trivial AST (e.g., non-constant loading).
3. We may deem a function/procedure to be impure if it contains some component that is "impure". However, we may still specialize areas in and around it despite it containing some impure area.
4. If we have some pure binary operator, we may compute/specialize it if both of it's inputs are static.
5. If we have some pure unary operator, we may compute/specialize it if it's input is static.
6. In general, if we have some pure n-ary operator we may compute/specialize it if all of it's inputs are static.
7. Any program without any impure function usage should be computed entirely before running. For example, if we have some program meant to compute the `X`-th fibonacci number (where `X` is some constant defined in the code, specifically not read in during runtime), we will pre-compute the `X`-th fibonacci number and specialize the code such that it merely loads the `X`-th fibonacci number into memory (or just sets it to some variable).
8. We should strip unnecessary code. For example, if we have "no-op" code, we should remove it through specialization. Additionally, if we have code that is no longer used after specialization, we should try to remove it wherever possible.

There will also be a schema for writing applications that are "partial evaluator" friendly, in that they are built in such a way that static information and dynamic information is grouped together in such a way that the partial evaluator may make the most use of the information as possible (for example, if we write something as `static + dynamic + static`, we may not be able to partially evaluate this even slightly unless we do not write it as `dynamic + static + static` [up to the associativity of the operator]).

### Some examples of code specialization

Below are some examples of code specialization, however, these are not the only examples that this work would be limited to.

| Code | Effective Specialization |
|------|----------------|
| `if True then a := 5 else a := 3` | `a := 3` |
| `5 + 3` | `8` |
| `5 * 3` | `15` |
| `5 = 3` | `False` |
| `5 - 3` | `2` |
| `-(5 + 3)` | `-8` |
| `not(False)` | `True` |
| `write(5+3)` | `write(8)` |
| `if a > 0 then b := 3 else b := 0` | `b := 3` |
| `const a := 4; if a > 0 then b := 3 else b := 0` | `const a := 4; b := 3` |
| `const a := 4; b := a + 3` | `const a := 4; b := 7` |
| `q, r := quotrem(5,2)` where `quotrem` is a pure function | `q, r := 2, 1` |
| `q := fib(10)` where `fib` is a pure function (fibonacci) | `q := 55` |

## Weekly Plan

|       Week      |                           Name                           | Description |
|:---------------:|:--------------------------------------------------------:|-------------|
|   Mar. 10 - 16  | Prototyping <br>+ Deciding between project<br>+ Learning about P0 | - Study P0, watch lecture videos about P0 and WebAssembly, learning how to develop P0 programs and how to write WebAssembly S-expressions, and about how WebAssembly works in general<br> - Decide between projects<br> - Formalize proposed grammar changes to P0|
|   Mar. 17 - 23  |                       Implementing                       | - Building a prototype of partial evaluation |
|   Mar. 24 - 30  |             Debugging, rewriting, optimizing             | - Create examples, test cases, and write nice error messages<br> - Work on generalizing type parameters for the sum types<br> - Restructure if necessary (general code clean up) |
| Mar. 21 - Apr.6 |                   Creating presentation                  | - Create presentation examples and material, using JupypterHub for creating a slideshow, similar to course notes |
| Apr. 7 - Apr.12 |             Finishing touches + Presentation             | - Submission due on Apr. 12th<br> - Final tests and quality control<br> - Practicing presentation before presentation date |

## Resources
* The **existing P0 compiler from course notes** will be augmented to allow for the disjoint union types and other language features as discussed above.
* **GitLab** will be used for hosting all project artifacts, including, but not limited to, Jupyter Notebooks, notes, related research, examples, and build artifacts.
* **JupyterHub** will be used to develop the language changes. Files from JupyterHub will only exported at least once per week for uploading to GitLab so that GitLab contains a somewhat up-to-date notes.
* Language decisions will be influced by my experience with **Haskell**, **Agda**, and **Java**.
* "Tutorial on Online Partial Evaluation" - https://www.cs.utexas.edu/~wcook/tutorial/PEnotes.pdf
* "Partially-static data as Free Extension of Algebras" - https://www.cl.cam.ac.uk/~jdy22/papers/partially-static-data-as-free-extension-of-algebras.pdf
* My discussion session notes from CAS 761 (from which we discussed the above 2 papers) - https://www.cas.mcmaster.ca/~carette/CAS761/F2020/index.html
