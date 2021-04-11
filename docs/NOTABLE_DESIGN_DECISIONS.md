# Notable Design Decisions

* The first 4 bytes of a program are to be always initialized to 0 so that we can _always_ have uninitialized ADT pointers pointing to it, then when this uninitialized ADT is read in, we will always see that the "instance" has `kind = 0`, meaning it's uninitialized (and also not instantiated).
* When ADTs are read in, we create "helper functions" for each ADT Kind. These "helper functions" are then used whenever we want to instantiate any particular ADT Kind. ADT Kind instantiation is hence secretly just a function call (to some function that creates an ADT on the heap and returns it's memory location).
* When in scope of a case, when you're _inside_ of an actual ADT Kind's statement suite, the variable being _cased_ on is typed as if it were the ADT Kind, not just the ADT itself!
* In the `nil` and `default` cases of a `case` statement, the target variable is left untouched. However, in the other cases, they are _selectable_ records representing the ADT Kind it was pattern matched to be.
* Disjoint union type variants are mutable records!

##### NOTE: All of these points are discussed in greater length in the other documents. However, I felt it was necessary to retain a short list of these "notable design decisions" here as well for quick overview.
