# Testing

While implementing the disjoint union types, we've create many tests along the way to ensure that changes were implemented correctly. We store many testing stubs (which can all be run at once against "stable expectations"/correct results) in the `../src/tests/` folder. To learn how to run all the tests at once, please visit the <a href="../src/tests/README.md">`../src/tests/README.md`</a> file.

These tests are all new and specifically geared towards testing P0 and disjoint union types. In particular, we also test compatibility with existing data structures in P0 (e.g., records, sets, and arrays). We have also ported over the stable tests originally created by Dr. Sekerinski as well and updated them to accommodate the changes we made to the compiler and the standard procedures.

