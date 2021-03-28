# Project Proposal

## Table of Contents
- [Project Proposal](#project-proposal)
  - [Table of Contents](#table-of-contents)
  - [Topic](#topic)
  - [Objective](#objective)
  - [Division of Work](#division-of-work)
  - [Design](#design)
    - [Language Changes](#language-changes)
    - [Pseudocode examples](#pseudocode-examples)
      - [Simple](#simple)
      - [Generalized](#generalized)
  - [Weekly Plan](#weekly-plan)
  - [Resources](#resources)

## Topic
Project 9: Disjoint Union Types

## Objective
The goal of this project is to add disjoint union types to P0, with adding some "functional" aspects onto them such as pattern matching.

## Division of Work
As I am enrolled in 6TB3, I, Jason Balaci, will be the only team member and will be building the entire project by myself.

## Design

### Language Changes
An approximate language proposal:
```
type ::= identifier << dynamic list of possible types, thereby allowing embedding types within types >>

constructor ::= identifier{" " type}
sumTypeDefinition ::= "data" identifier = constructor {" | " constructor} 

case ::= constructor ":\n" statementBlock "\n"
caseExpr ::= "case " expression " of {\n" case {"\n" case} "}"
```
Note: whitespace will be allowed but is not important to be added to the above proposal.

We specifically want to note the following:
1. Language changes will be influenced by Haskell and Agda.
2. `data <Type Name> = <Constructor Name> {<Type> }| <Constructor Name> {<Type> }| ...` will be the general structure of a type definition of a sum type.
3. `case x of { a: ... b: ... c: ... ... }` will be the general structure of pattern matching on variables, with new lines between each case (examples below).
4. Deep pattern matching will not be allowed when "case"-ing. When using a "case" on some sum type, each case should be a single constructor (along with new variable names when applicable) from the parent type. You will not be allowed to further pattern match on any of the individual variables.
5. A single "default" case will allowed as the last case, matching any non-explicitly matched types. It will be similar to how Java's switch-statements' "default".

### Pseudocode examples
The following are some examples of the proposed language changes.

#### Simple
The following are some _simple_ examples that do not include any generalized types.
```
data MaybeInt =
      Just integer
    | Nothing

procedure defaultOr(x: MaybeInt, d: integer) → (y: integer)
    case x of {
        Just b:
            y := b
        Nothing:
            y := d
    }

procedure add(x, y: MaybeInt) → (r: integer)
    r := defaultOr(x, 0) + defaultOr(y, 0)

program arithmetic
    var x, y, z: integer
    var mX, mY : MaybeInt
      x ← read(); y ← read()
      if x ≥ 10
        then mX := Just x
        else mX := Nothing
      if y ≥ 10
        then mY := Nothing
        else mY := Just y
      z ← add(mX, mY)
      write(z)

```

```
data IntBinTree =
      Tip
    | Branch IntBinTree integer IntBinTree

procedure total(b: IntBinTree) → (r: integer)
    var lt, lr: integer
    case b of {
        Tip:
            r := 0
        Branch l v r:
            lt ← total(l)
            rt ← total(r)
            r := lt + v + rt
    }
```

Using `quotrem` from course notes, `EitherIntInt` is a more common example of using `Either` (influenced by Haskell), `EvenOddIntInt` is a variant of `Either` in that it has the same construction with different names. 
```
data EitherIntInt =
      Left integer
    | Right integer

data EvenOddIntInt =
      Even integer
    | Odd integer

procedure evenOrOdd(i: integer) → (eo: EitherIntInt)
    var q, r: integer
    q, r = quotrem(i, 2)
    if r ≠ 0
        then eo := Odd i
        else eo := Even i

procedure printIfEven(eo: EvenOddIntInt)
    case eo of {
        Even i:
            write(i)
    }

procedure printIfOdd(eo: EvenOddIntInt)
    case eo of {
        Odd i:
            write(i)
    }
```

#### Generalized
The following are the same examples but using parameters to generalize the same constructions.

```
data Maybe a =
      Just a
    | Nothing
```

```
data BinTree a =
      Tip
    | Branch BinTree a BinTree
```

```
data Either a b =
      Left a
    | Right b
```

## Weekly Plan

|       Week      |                           Name                           | Description |
|:---------------:|:--------------------------------------------------------:|-------------|
|   Mar. 10 - 16  | Prototyping <br>+ Deciding between project<br>+ Learning about P0 | - Study P0, watch lecture videos about P0 and WebAssembly, learning how to develop P0 programs and how to write WebAssembly S-expressions, and about how WebAssembly works in general<br> - Decide between projects<br> - Formalize proposed grammar changes to P0|
|   Mar. 17 - 23  |                       Implementing                       | - Building a prototype of disjoint union types |
|   Mar. 24 - 30  |             Debugging, rewriting, optimizing             | - Create examples, test cases, and write nice error messages<br> - Work on generalizing type parameters for the sum types<br> - Restructure if necessary (general code clean up) |
| Mar. 21 - Apr.6 |                   Creating presentation                  | - Create presentation examples and material, using JupypterHub for creating a slideshow, similar to course notes |
| Apr. 7 - Apr.12 |             Finishing touches + Presentation             | - Submission due on Apr. 12th<br> - Final tests and quality control<br> - Practicing presentation before presentation date |

## Resources
* The **existing P0 compiler from course notes** will be augmented to allow for the disjoint union types and other language features as discussed above.
* **GitLab** will be used for hosting all project artifacts, including, but not limited to, Jupyter Notebooks, notes, related research, examples, and build artifacts.
* **JupyterHub** will be used to develop the language changes. Files from JupyterHub will only exported at least once per week for uploading to GitLab so that GitLab contains a somewhat up-to-date notes.
* Language decisions will be influced by my experience with **Haskell**, **Agda**, and **Java**.
* https://en.wikipedia.org/wiki/Algebraic_data_type

