# Project Proposal

## Topic
Partial Evaluation in P0

## Objective
The goal of this project is to add enable online partial evaluation in P0.

## Division of Work
As I am enrolled in 6TB3, I, Jason Balaci, will be the only team member and will be building the entire project by myself.

## Design
A partial evaluator in P0 would be implemented using an "online" style whereby it reasons about specializations as it tries to compile P0 programs into WebAssembly (or just before compiling), relying on the already constructed Abstract Syntax Tree for P0.

When compiling, a partial evaluator tries to specialize

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
