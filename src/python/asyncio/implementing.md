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

#### Step Z - The coroutine/generator Issue

* We have (mis-)used the generators
* Generators/Iterators are intended for yielding something that is consumed by
  the caller.
* Coroutines use `yield` and `yield from` to just suspend the current function
  and give control back to the loop.
* Implementation wise we have the same thing, but semantically they are very
  different.
* Users could still pass generators and generators could still run coroutines.
* From looking at the code or the object users still could mix up coroutines and
  generators because it relies just on a technical detail.
* Nothing forbids to use coroutines as generators and the other way round.

A `generator function` could be marked as a `coroutine function`.

```python
import inspect

def mark_as_coroutine(func):
    if not inspect.isgeneratorfunction(func):
        raise TypeError(f"{func.__name__} is not a generator function")
    func._is_coroutine = True
    return func

def is_coroutine_function(func):
    return getattr(func, "_is_coroutine", False)

@mark_as_coroutine
def some_result():
    future = Future()
    future.set_result(result)
    return (yield from future)


is_coroutine_function(some_result)
```

Async/Await to the rescue
