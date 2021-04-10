# Future Work

* Memory management
* More built-in ADTs with better specialization in their code generation (e.g., Lists, Strings, Maps)
    * Built-in String ADT --> then we can have "abcdef..." syntactic sugar for generating Strings at compile time!
* Type variables!
* Allow ADT type parameterization?
    * In-place a fake node for generating WebAssembly (e.g., `asm.append(ADTTYPESDECLARATIONS)`)
    * Allow parameterization of form: `type X a b ... = First a | Second b | ... `
    * Whenever referring to some type `X a b ...` (it should be FULLY filled in), it should find an existing definition for this ADT or generate a new one (putting in the new type into an extra list for later in-placing into the `ADTTYPESDECLARATIONS`!)
