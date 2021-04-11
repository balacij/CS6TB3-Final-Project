# The `case` Statement

The `case` statement is very important for effectively using disjoint union types as it's the only way that you can access the data held within them. The `case` statement lets you execute code based on what the `kind` of a disjoint union type is. It also lets you check if a variable is not initialized through a `nil` case.

The `case` statement is of the form `case <variable> of { ... cases ... }` where `cases` are of the form `KindIdentifier: statementSuite` with optional `nil` (uninitialized disjoint union types) and `default` cases ("catch all other" case). Default cases may also do `nothing` (no-operations). _NOTE_: The `nil` case should be the first _kind_ if you choose to check for it, and the `default` case should be the last case if you choose to use it. If you choose to use the no-operation `default` case, you should simply write `default nothing` instead of writing a statement suite.

The `case` statement is very natural feeling if you have experience programming with Haskell and/or Java. It's modelled after Java's `switch` statement with inspiration regarding typing assumptions from Haskell.


## Examples

Assuming we have some `List`-like disjoint union type:
```
type List = Cons(value: integer, tail: List) | Nil
```

We may `case` on instances of it as follows:
```
var m: List
var x: integer
m <- Cons(10, Nil())

case m of {
    Cons:                      // if `m` is a Cons-kind
        writeln(m.value)       // assuming `m` is a record (value: integer, tail: List)
    default nothing            // otherwise, we default to doing nothing (and `m` is left as a DUT)
}

case m of {
    nil:                       // if `m` is uninitialized
        writeln(0)             // print 0
    Nil:                       // if `m` is a Nil-kind
        writeln(1)             // print 1
    default:
        writeln(10)            // `m` is left as a DUT
}
```

## Grammar 

Formalized both here and in the <a href="GRAMMAR.md">GRAMMAR</a> file, statements (and `case`s in particular) are defined as follows:

```
    statement ::=
        ident selector ":=" expression |
        ident {"," ident} (":=" expression {"," expression} |
            ("←" | "<-") ident "(" [expression {"," expression}] ")") |
        "if" expression "then" statementSuite ["else" statementSuite] |
        "while" expression "do" statementSuite |
        "case" expression "of" "{" INDENT ["nil" ":" statementSuite] {ident ":" statementSuite} ["default" (":" statementSuite | "nothing")] DEDENT "}"
```

## Warnings

When you compile a `P0` program with in-exhaustive `cases` for any case, you will be greeted with warnings that your program may have unintended/unforeseen side-effects, or, more likely, incomplete.

For example, if you try to compile:
```
type Colour = R | G | B

procedure printCol(col: Colour)
    case col of {
        R: writeCharLn('R')
        G: writeCharLn('G')
    }

program Main
    var s: Colour

    s <- R()
    case s of {
        default: writeCharLn('F'); printCol(s)
    }
```

You will be greeted with the following warning messages:
```
WARNING: line 7: missing explicit `nil` case
WARNING: line 7: non-exhaustive cases
WARNING: line 15: redundant `case`ing (only has default case, `case`ing can be removed)
```

The first two lines of these messages mean that the first-most `case` statement is incomplete -- it does not cover all variant possibilities (as such, it is "non-exhaustive"), it's specifically missing variant `B` and the `nil` case. The third line is just a warning that the second `case` statement which only has `default` case and statement is redundant. 
