# Disjoint Union Types

Disjoint union types are types whereby a list of records are tagged with names, and instances of the disjoint union type are instances of these named records. An instance of a disjoint union type may only be one of these records at one time.

Disjoint union types are also commonly referred to as _Algebraic Data Types_ in functional programming languages.

Throughout this project, we may refer to it as well as _Algebraic Data Types_ or with the abbreviation "ADTs".

### Example of a Disjoint Union Type
```
type List = Cons(head: integer, tail: List)
          | Nil
```

## Kinds / Variants

Kinds/variants of a disjoint union type are the individual named records.

### Instantiating Kinds

Instantiation of disjoint union kinds is very similar to calling procedures in P0. If the kind being instantiated has no parameters, such as `Nil` above, you should simply treat instantiating it as if it were a procedure with no parameters. If the kind being instantiated has parameters, you should fill them in as you would with procedure parameters.

For example, using the `List` disjoint union type above, we may instantiate instances of it as follows:
```
program Main
    var l: List

    l := Cons(10, Nil())

    l <- Nil()
```
##### NOTE: We allow for procedure calls and instantiations to be performed in expressions if they have single return values.

### Self-references

Any of the tagged records may have variables that are of a self-reference type (another instance of the parent disjoint union/algebraic data type).

## Type Definitions

## Grammar

Formalized both here and in the <a href="GRAMMAR.md">GRAMMAR</a> file, the disjoint union types and kinds are defined as follows:

```
    type ::=
        ident ["(" typedIds ")"] {"|" ident ["(" typedIds ")"]} |
        "[" expression ".." expression "]" ("→" | "->") type |
        "(" typedIds ")" |
        "set" "[" expression ".." expression "]"
    typedIds ::= ident {"," ident} ":" type {"," ident {"," ident} ":" type}.
    declarations ::= 
        {"const" ident "=" expression}
        {"type" ident "=" type}
        {"var" typedIds}
        {"procedure" ident "(" [typedIds] ")" [ ("→" | "->") "(" typedIds ")" ] body}
```

##### NOTE: Disjoint union types are still built with the standard `type` definitions for type aliases but may become disjoint union types if the expected alias does not exist.
##### NOTE: when defining the disjoint union types, we ignore indents and dedents between variants to accommodate multiline and differing preferred coding styles for defining such constructions. This is purely for cosmetic purposes.

## Examples

Some examples of commonly used disjoint union types/algebraic data types in functional programming languages are as follows:

* Maybe
```
type Maybe = Just(value: integer)
           | Nothing
```

* Either
```
type Either = Left(value: integer)
            | Right(value: boolean)
```

* List
```
type List = Cons(head: integer, tail: List)
          | Nil
```

* String
```
type String = SCons(ch: integer, tail: String)
            | SNil
```

## Notes

* We allow arbitrary whitespace in between kind declarations, taking inspiration from programming languages like Haskell where many have different preferred code styling preference.


## Mutability

The disjoint union types implemented in this project have mutable values in the records, but immutable kinds. As such, you may edit the values carried by instances of the disjoint union types, but you may not change the kind of an instantiated disjoint union type.


## Warnings

When you compile a `P0` program disjoint union types that have only one kind variant, you will receive a warning saying that they are redundant.

For example, if you try to compile:
```
type Colour = R

program Main
    var s: Colour

    s <- R()
```

You will be greeted with the following warning messages:
```
WARNING: redundant: "Colour" has only been given 1 only one kind variant!
```
