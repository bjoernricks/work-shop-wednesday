## AsyncIO - Implementing AsyncIO

To understand how the `asyncio` Python standard library works and provides
asynchronous I/O via `async/await` syntax. We are going to reimplement it from
scratch.

### Rewind: Coroutines

> `coroutine` Coroutines are a more generalized form of subroutines. Subroutines
> are entered at one point and exited at another point. Coroutines can be
> entered, exited, and resumed at many different points.

[Source](https://docs.python.org/3.10/glossary.html#term-coroutine)

`AsyncIO` in Python is based on coroutines. We already know
`Generators`/`Iterators` are coroutines. `Generators` allow suspend the current
function and to return to the caller of the function.

### Overview

We are going to re-implement the `asyncio` Python standard library step-by-step
as it was provided with Python 3.4 initially. This allows for understanding
it's internals and general concept. Of course we are using simplifications and
skipping some parts like cancellation. These parts are mentioned in the
[What's missing](missing.md) chapter.

```{toctree}
step1
step2
step3
step4
step5/index
step6/index
step7/index
step8/index
step9/index
step10/index
step11/index
step12/index
step13/index
step14/index
missing
stepz
```
