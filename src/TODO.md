# TODOs
1. Fill out examples
2. Clean up program entry -- get a nice `getopts` Python setup going
3. Add parsing tests (though I realistically already did them, just need to re-write them again...)
4. Create presentation
5. `grep -E "TODO" -r *` -- go through all file TODOs and handle them accordingly
6. Fix globals
7. Make sure I'm not allowing poorly formed names for ADT Kind identifiers
8. Check on memory growing issue
9.  Update grammar in separate file
10. Build and test `default` cases
11. Build and test `nil` cases
12. Create `strings` example :^)

# MAYBEs?
1. Create more standard built-in procedures for better working with Strings?
2. Make lists a built-in construction?
3. Allow ADT type parameterization?
    * In-place a fake node for generating WebAssembly (e.g., `asm.append(ADTTYPESDECLARATIONS)`)
    * Allow parameterization of form: `type X a b ... = First a | Second b | ... `
    * Whenever referring to some type `X a b ...` (it should be FULLY filled in), it should find an existing definition for this ADT or generate a new one (putting in the new type into an extra list for later in-placing into the `ADTTYPESDECLARATIONS`!)
4. Create `is<Kind>` functions automatically?
5. Improve code generation for `case`s... maybe we can cache the kind locally somehow?
6. Figure out what the goal is for the "casing reference ADT issue" (when casing and wanting to reference ADT as it is, not with selector...)?
