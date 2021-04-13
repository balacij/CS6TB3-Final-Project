# Implementation Notes

We try to implement DUTs as close to the definition of DUTs as possible.

Essentially, we define the disjoint union types as an instance of one of many records, whereby each record has a uniquely identifying tag. We treat instances of these DUTs to be records in memory with the variant records prepended with a unique id. For example, if we had `type Maybe = Just(value: integer) | Nothing`, we treat it as if it were closer to `Just(id: integer, value: integer) | Nothing(id: integer)`, using `id` as a common location and identifier between each data construction. Additionally, the `id` for `Just` will always be `1` and the `id` for `Maybe` will always be `2`, which allows us to uniquely identify which DUT constructor an instance takes the form of. 

When reading in the DUT type declarations, we create "instantiation helper" functions for each data constructor of each DUT type. Consider instantiating `Just` specifically using `Just(10)`. When parsing, we rewrite the `Just` into our internal helper function (in this case, it would be `__mk_Just`) and then parse the arguments `(10)` as we would when parsing the parameters of a P0 procedure call. This allows us to easily construct DUTs. In our helper functions, we do the "behind the scenes" work, where we store the inputs into the latest free memory area, and then grow the total memory size by the size of the DUT construction (in bytes). This memory component is discussed in depth in <a href="MEMORY.md">MEMORY.md</a>.

Consider the following code:
```
var m: Maybe
m := Just(10)
case m of {
    nil: ...
    Just: ...
    Nothing: ...
    default: ... 
}
```
In this code above, we are `case`ing on the value of `m`. Assuming it wasn't obvious that `m` was a `Just`, the `case` statement compares the `id` of `m` (which is internally just an i32 in the first 4 bytes of the stored memory area of `m`) against each case variant's id. When comparing against `nil`, we are checking if the value of `m` is not yet instantiated (e.g., where `id = 0`). When we are comparing against `Just` and `Nothing`, we are comparing against their unique identifiers in order the cases appear. The ordering of the cases makes no difference to the results but we can do a bit of branching optimization if we know that some variant is more likely to appear than others. The `default` case is the "catch all" case where if none of the above cases were matched, it will be executed. Please note that if you create a `case` statement that is non-exhaustive of the variants, the compiler will warn you of potential error.

