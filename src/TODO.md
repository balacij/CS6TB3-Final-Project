# TODOs
1. Fill out examples
2. Clean up program entry -- get a nice `getopts` Python setup going
3. Allow procedures to be called and returned as values in expressions (no LARROW) if they have a single return value
4. Create `is<Kind>` functions automatically?
5. Add parsing tests (though I realistically already did them, just need to re-write them again...)
6. Create presentation
7. `grep -E "TODO" -r *` -- go through all file TODOs and handle them accordingly
8. Allow multi-line ADTKind definitions for an ADT
9. Fix globals
10. Figure out what the goal is for issue when casing and wanting to reference ADT as it is, not with selector...
11. Improve code generation for `case`s... maybe we can cache the kind locally somehow?
12. Allow `<-` and `->` as well in addition to the existing inaccessible LARROW and RARROW

# MAYBEs?
1. Create more standard built-in procedures for better working with Strings?
2. Make lists a built-in construction?
3. Allow ADT type parameterization?
