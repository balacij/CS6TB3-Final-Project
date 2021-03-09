# Project Proposal

## Topic
Project 9: Disjoint Union Types

## Objective

## Division of Work
As I am enrolled in 6TB3, I, Jason Balaci, will be the only team member and will be building the entire project by myself.

## Design

### Challenges

### Language Changes/Decisions

### Pseudocode examples

#### Simple
```
data MaybeInt =
      Just Int
    | Nothing
```

```
data IntBinTree =
      Tip
    | Branch IntBinTree Integer IntBinTree
```

```
data EitherIntFloat =
      Left Int
    | Right Float
```

#### Generalized
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
|   Mar. 10 - 16  | Prototyping <br>+ Deciding between project<br>+ Learning |             |
|   Mar. 17 - 23  |                       Implementing                       |             |
|   Mar. 24 - 30  |             Debugging, rewriting, optimizing             |             |
| Mar. 21 - Apr.6 |                   Creating presentation                  |             |
| Apr. 7 - Apr.12 |             Finishing touches + Presentation             |             |

## Resources
* https://en.wikipedia.org/wiki/Algebraic_data_type

