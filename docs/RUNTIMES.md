# Runtime

While this code is built to compile  WebAssembly, we're not forcing it to be tied to usage from within a browser. As such, we allow compiling to WebAssembly for you to use whichever runtime you desire. However, for the sake of convenience, we also allow immediate code execution after compiling for quick debugging and usage.

## `wasmer`

`wasmer` is the **recommended** runtime for running programs with this compiler.

Recalling our results for the Sieve of Eratosthenes (from Lab 9):

| Run Count | P0 (Pywasm) | P0 (wasm) | P0 (wasmer) |
|-----------|-------------|-----------|-------------|
| 1,000,000 | >2hrs       | 1.67ms    | 56.8ms      |
| 10,000    | 2min 2s     | 1.62ms    | 2.64ms      |
| 1,000     | 12.3s       | 1.50ms    | 2.48ms      |

We can confidently say that `wasmer` has proven to be a fast and stable runtime (as per our Lab 9), with performance very close to `wasm` (web browser execution). However, should you want even better performance, you should considering doing manual tuning, or running with the `wasm` execution engine from your web browser.


## `pywasm`

As `pywasm` is built in Python, it has the limitations of Python imposed onto it as well. When working with disjoint union types/algebraic data types, we often write functions with high amounts of recursion. As such, the recursive call stack limit in Python can cause issues when using `pywasm` as the runtime, despite WebAssembly not actually having a call stack size limit (see [this discussion on GitHub](https://github.com/WebAssembly/design/issues/1163)).

For this reason, we _discourage_ the usage of `pywasm` for production usage. However, for small testing or careful usage, `pywasm` is fine. However, `wasmer` is considerably faster and more efficient for general programs.
