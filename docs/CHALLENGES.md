# Challenges

While developing this project, I came across a few interesting challenges.

## Runtime -- pywasm

While testing out early programs that heavily used recursive, I was running into a frequent "stack size limit" error that seemingly occurred very quickly. I had first thought that this might have been a restriction by WebAssembly but after a bit of research, I found out that the real culprit was `pywasm`. `pywasm` is, of course, written in Python, for which has a rather small recursive call stack size limit. As such I switched my default runtime to `wasmer` and there were no more issues.

## Grammar

Implementing "natural feeling" disjoint union types in an imperative language was quite interesting. It's only a feature that I've come across in functional programming languages, with my own view of it heavily being modelled after Haskell. At first, I considered having `case` statement cases also contain a small list of names next to the targeted kind, for which it would assign the values of the `case`d variable if it were of that kind. However, I ultimately felt that this design wasn't quite appropriate for `P0` and ultimately felt that having selector access, with `.`, to access named variables from each kind was more appropriate.

In the end, I enjoy this grammar I decided on as it also forces the programmers to have uniform names for their DUT kind's variable names, as they can only access them through these selectors.
