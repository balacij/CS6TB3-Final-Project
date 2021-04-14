# Implementation Notes

We try to implement DUTs as close to the definition of DUTs as possible.

Essentially, we define the disjoint union types as an instance of one of many records, whereby each record has a uniquely identifying tag. We treat instances of these DUTs to be records in memory with the variant records prepended with a unique id. For example, if we had `type Maybe = Just(value: integer) | Nothing`, we treat it as if it were closer to `Just(id: integer, value: integer) | Nothing(id: integer)`, using `id` as a common location and identifier between each data construction. Additionally, the `id` for `Just` will always be `1` and the `id` for `Maybe` will always be `2`, which allows us to uniquely identify which DUT constructor an instance takes the form of.

When reading in the DUT type declarations, we create "instantiation helper" functions for each data constructor of each DUT type. Consider instantiating `Just`, specifically using `Just(10)`. When parsing, we rewrite the `Just` into our internal helper function (in this case, it would be `__mk_Just`) and then parse the arguments `(10)` as we would when parsing the parameters of a P0 procedure call. This instantiation helper function then allocates the construction on the heap and returns the memory address for which it was placed. This allows us to easily construct DUTs. In our helper functions, we do the "behind the scenes" work, where we store the inputs into the latest free memory area, and then grow the total memory size by the size of the DUT construction (in bytes). This memory component is discussed in depth in <a href="MEMORY.md">`MEMORY.md`</a>.

Consider the following code:
```
var m: Maybe
m := Just(10)
case m of {
    nil: ...
    Just: ...      // `m` has type changed to Just's record
    Nothing: ...   // `m` has no type change since Nothing has no record
    default: ... 
}
```
In this code above, we are `case`ing on the value of `m`. Assuming it wasn't obvious that `m` was a `Just`, the `case` statement compares the `id` of `m` (which is internally just an i32 in the first 4 bytes of the stored memory area of `m`) against each case variant's id. When comparing against `nil`, we are checking if the value of `m` is not yet instantiated (e.g., where `id = 0`). When we are comparing against `Just` and `Nothing`, we are comparing against their unique identifiers in order the cases appear. The ordering of the cases makes no difference to the results but we can do a bit of branching optimization if we know that some variant is more likely to appear than others. The `default` case is the "catch all" case where if none of the above cases were matched, it will be executed. Please note that if you create a `case` statement that is non-exhaustive of the variants, the compiler will warn you of potential error. Finally, within each `case`'s statement suite, we assume that the type of `m` is changed to be the record of the variant (if the variant has a record).


## Internal

We use the following classes in `ST.py` to represent our DUTs/ADTs:

```
class ADT:
    def __init__(self, name, kinds):
        self.name = name
        self.kinds = kinds

    def __str__(self):
        return f"ADT(name = {self.name}, kinds = [{ ', '.join(str(kind) for kind in self.kinds) }])"


class ADTKind:
    def __init__(self, index, name, record=None):
        self.index = index
        self.name = name
        self.record = record

    def __str__(self):
        return f"ADTKind(index = {self.index}, name = {self.name}, record = {str(self.record)})"


class ADTSelfRef:
    def __init__(self):
        pass

    def __str__(self):
        return f"ADTSelfRef()"
```

As we can see rather clearly, the kinds/variants are simply wrapped named and indexed records for the ADTs/DUTs. `ADTSelfRef`s are placeholder types handling recursively defined structures.

## Generated WAT

### Instantiation Helpers

The following code snippet is what the created instantiation helpers look like.

```
(func $__mk_Just (param $value i32) (result i32)
global.get $_memsize         ;; get known unused memory location
i32.const 1                  ;; get Just's kind index
i32.store                    ;; store it
global.get $_memsize         ;; get known unused memory location
i32.const 4                  ;; get offset of the next type
i32.add                      ;; impose offset onto total memory size
local.get $value             ;; get param value
i32.store                    ;; store it in it's area
global.get $_memsize         ;; get global memory size
global.get $_memsize         ;; get global memory size (again)
i32.const 8                  ;; get size of kind (Just)
i32.add                      ;; add to memory size
global.set $_memsize         ;; set memory size, leftover i32 on stack which is the returned pointer to the generated Just
)
(func $__mk_Nothing (result i32)
global.get $_memsize         ;; get known unused memory location
i32.const 2                  ;; get Nothing's kind index
i32.store                    ;; store it
global.get $_memsize         ;; get global memory size
global.get $_memsize         ;; get global memory size (again)
i32.const 4                  ;; get size of kind (Nothing)
i32.add                      ;; add to memory size
global.set $_memsize         ;; set memory size, leftover i32 on stack which is the returned pointer to the generated Nothing
)
```

### Case Statement

Consider the following type declaration and `case` statement:

```
type Colour = R | G | Unknown

procedure printCol(col: Colour)
    case col of {
        nil: writeCharLn('?')
        R: writeCharLn('R')
        G: writeCharLn('G')
        default: writeCharLn('?')
    }
```

We generate the below WebAssembly code for the above `case` statement:
```
local.get $col
i32.load
i32.const 0        ;; check if $col is nil
i32.eq
if                 ;; if it is nil
i32.const 63
call $writeCharLn  ;; print '?'
else               ;; otherwise
local.get $col
i32.load
i32.const 1        ;; check if `R`
i32.eq
if                 ;; if it is `R`
i32.const 82
call $writeCharLn  ;; print 'R'
else               ;; otherwise
local.get $col
i32.load
i32.const 2        ;; check if `G`
i32.eq
if                 ;; if it is `G`
i32.const 71
call $writeCharLn  ;; print 'G'
else
i32.const 63       ;; otherwise, default
call $writeCharLn  ;; print '?'
end
end
end
```

<a style="float:left" href="MEMORY.md">\<\< Memory</a> <a style="float:right" href="CHALLENGES.md">Challenges \>\></a>
