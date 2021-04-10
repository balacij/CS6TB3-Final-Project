# TODOs
1. Add parsing tests (though I realistically already did them, just need to re-write them again...)
2. Memory management -- if memory size nears `2 ^ 16` (near being defined modulo `2 ^ 16` and within ~`X` of `2 ^ 16`, where `X` is the size of the largest construction [ADT or record!] in the program), we should grow the memory size by 1 page (at a time!)
3. Allow "nothing" sym for any case
4. Make sure that when mixing arrays with ADTs, nothing breaks
5. Make sure that we can't define new ADTs past the `type` statements

# MAYBEs?
1. Improve code generation for `case`s... maybe we can cache the kind locally somehow?
