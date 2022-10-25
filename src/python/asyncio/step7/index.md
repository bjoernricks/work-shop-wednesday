### Step 7 - The Future

Looking at our current processing chain `loop -> yield from* -> yield` (the *
means it can be repeated n times) the `yield` part on the right side is a bit
out-of-order. It just doesn't feel right completely. Wouldn't it be better if
get a well defined API that abstracts the `yield` and `yield from` can be used
instead.

Let us try something. How does a coroutine work normally? It runs and starts
something. Afterwards it suspends itself and gives back control to the caller.
If something is finished and it is resumed a result is returned.

```{literalinclude} future.py
:language: python
:caption: Future v1
```

We introduce a new class `Future` that can be called with `yield from future`
to first suspend and give the control back to the caller and second to return a
result. Additionally a `Future` can be in one of the following states:

1. Pending - Waiting for a result
2. Done - A result is set

It always takes (at least) two generator steps to get the into the done state.

Example:

```python
def future_result(future):
    return (yield from future)

future = Future()
coroutine = future_result(future)
next(coroutine)
future.set_result(123)
try:
    next(coroutine)
except StopIteration as e:
    result = e.value
    print(result)
```

As a result we have an object that allows to set a result (even) in a future
step.

```{literalinclude} step7.py
:language: python
```

Output:

```python
Loop step 1
Loop step 2
Loop step 3
Loop finished with result 3
```

```{note}
As a side note, the Future class implements the `Iterable` protocol.
```

```{admonition} Summary
* We learned the basic concept of a `Future`
```
