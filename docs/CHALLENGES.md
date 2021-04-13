# Challenges

While developing this project, I came across a few interesting challenges.

## Self-references

Consider our list definition, `type List = Cons(value: integer, tail: List) | Nil`. In this construction, we create a "Cons" construction which contains another "List". However, when we are parsing the "Cons" construction, we are also parsing the "List" construction. As such, while parsing "List", we assume it to be a new construction that is not yet declared so that when we encounter it in the variants, we know that it is a self-reference to the "List" type. In this way, we register it as a pointer to another "List" instance.


## Runtime -- pywasm

While testing out early programs that heavily used recursive, I was running into a frequent "stack size limit" error that seemingly occurred very quickly. I had first thought that this might have been a restriction by WebAssembly but after a bit of research, I found out that the real culprit was `pywasm`. `pywasm` is, of course, written in Python, for which has a rather small recursive call stack size limit. As such I switched my default runtime to `wasmer` and there were no more issues.

## Grammar

Implementing "natural feeling" disjoint union types in an imperative language was quite interesting. It's only a feature that I've come across in functional programming languages, with my own view of it heavily being modelled after Haskell. At first, I considered having `case` statement cases also contain a small list of names next to the targeted kind, for which it would assign the values of the `case`d variable if it were of that kind. However, I ultimately felt that this design wasn't quite appropriate for `P0` and ultimately felt that having selector access, with `.`, to access named variables from each kind was more appropriate.

In the end, I enjoy this grammar I decided on as it also forces the programmers to have uniform names for their DUT kind's variable names, as they can only access them through these selectors.

## WebAssembly Code Size

In the first iteration of my implementation, generated code size was rather large. This was due to frequent code being placed everywhere whenever disjoint union types were instantiated. As such, to reduce size of generated code, we generate "instantiation helper functions" in our WebAssembly code for each variant of all disjoint union types. By doing this, we were able to reduce generated code size by a large factor. This particular amount reduced heavily depends on how many areas in the code that the variants are instantiated. As such, so as long as there are more areas that these variants are instantiated than the total number of variants in the file, there will be a notable reduction between the initial implementation generated code size and this one.

## WebAssembly Code Generation Time

The default compiler we are to build upon generates WebAssembly code while it parses the syntax tree of a P0 program. Unfortunately, some constructions and optimizations are quite difficult to get working with this kind of compiler. If we had a compiler that delayed code generation until after the full abstract and concrete syntax trees have been read in, we could place another step between them whereby we do our pre-processing. In this pre-processing step, we could have implemented many more features, such as partial evaluation (whereby we differentiate expressions further by static and dynamic components, and partially evaluate side-effect free codes), and even type variables for our disjoint union types. In many functional programming languages (in particular, Haskell), type variables allow for polymorphic type signatures, polymorphic algebraic data types (disjoint union types), and typeclass restrictions on type signatures. In particular, if we had the ability to have type variables, we would be able to make many of our examples polymorphic, allowing for increased levels of code reuse -- this would be particularly helpful for our List and Map constructions.

