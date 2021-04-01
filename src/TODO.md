# TODOs
1. Fill out examples
2. Clean up program entry -- get a nice `getopts` Python setup going
   1. `--clean` to get rid of leftover `.wat` and `.wasm` files (default to `false`)
   2. `--runtime` option to select between `pywasm` and `wasmer` (defaulting to `wasmer`, warning on `pywasm` usage that it's unsuitable)
   3. `--memory-size` option to set page size of the program (default to `1` page)
   4. `--run` option to automatically run the program (default to `true`)
3. Add parsing tests (though I realistically already did them, just need to re-write them again...)
4. Create presentation
5. `grep -E "TODO" -r *` -- go through all file TODOs and handle them accordingly
6. Fix globals
7. Make sure I'm not allowing poorly formed names for ADT Kind identifiers
8. Check on memory growing issue
9.  Update grammar in separate file
10. Build and test `default` cases
11. Build and test `nil` cases
12. Memory management -- if memory size nears `2 ^ 16` (near being defined modulo `2 ^ 16` and within ~`X` of `2 ^ 16`, where `X` is the size of the largest construction [ADT or record!] in the program), we should grow the memory size by 1 page (at a time!)

# MAYBEs?
1. Create more standard built-in procedures for better working with Strings? It might help to make Strings a built-in construction really if we choose to do this.
2. Allow ADT type parameterization?
    * In-place a fake node for generating WebAssembly (e.g., `asm.append(ADTTYPESDECLARATIONS)`)
    * Allow parameterization of form: `type X a b ... = First a | Second b | ... `
    * Whenever referring to some type `X a b ...` (it should be FULLY filled in), it should find an existing definition for this ADT or generate a new one (putting in the new type into an extra list for later in-placing into the `ADTTYPESDECLARATIONS`!)
3. Create `is<Kind>` functions automatically?
4. Improve code generation for `case`s... maybe we can cache the kind locally somehow?
5. Figure out what the goal is for the "casing reference ADT issue" (when casing and wanting to reference ADT as it is, not with selector...)?
