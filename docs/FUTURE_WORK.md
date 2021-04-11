# Future Work

In the near future, I'd like to implement all of the following:

## Type variables

I would like to implement type variables for all types so as to allow for algebraic data types to have polymorphic variables.

A possible way of implementing this is as follows:
* Change our compiler to not generate code immediately but to delay until the full file has been parsed once a large AST for the program has been built up. Though, we could do some little tricks to get it to work by in-placing fake nodes in the `asm` built that we alter just before returning it.
* Allow parameterization of form: `type X a b ... = First(v: a) | Second(v: b, r: a, q: b) | ... `
* Whenever referring to some type `X a b ...` (note: it should be fully filled in), it should find an existing definition for this filled in DUT or generate a new instance of it with name rewrites to allow for differentiation between them.

By having type variables, we would be able to create polymorphic lists, maps, general sum types, to allow for more code reuse.

## More built-in DUTs with better specialization in their code generation (e.g., Lists, Strings, Maps)

Similar to Haskell's `Prelude`, we could have stronger base functionality without having any explicit imports by implicitly importing our own `Prelude`-like module.

In particular, I would like to have Strings, Maps, Lists, and the Natural numbers as implicitly imported disjoint union types/algebraic data types. If we include Strings, then we could have `"abcd"` be an instance of a general syntactic sugar that unfolds `"abcd"` and the likes into `SCons('a', SCons('b', SCons('c', SCons('d', Nil()))))` to further assist with creating strings in P0.

## Improving Memory management

Presently, memory is allocated but never freed when no longer in use. I would like to implement better memory management to allow for more memory efficient applications, as well as potentially figuring out how to unfold more disjoint union types to conserve memory further.
