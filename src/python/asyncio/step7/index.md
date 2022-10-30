### Step 7 - The Future

Looking at our current processing chain `loop` -> `yield from*` -> `yield` (the *
means it can be repeated n times) the `yield` part on the right side is a bit
out-of-order. It just doesn't feel right completely. Wouldn't it be better if
get a well defined API that abstracts the `yield` and `yield from` can be used
instead.

Let us try something. How does a coroutine work normally? First it runs and
starts something. Afterwards it suspends itself and gives back control to the
caller. If something is done and it is resumed, a result is returned.

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

```{note}
As a side note, the Future class implements the `Iterable` protocol.
```

Example:

```python
def future_result(future):
    # something might happen here too
    return (yield from future)

future = Future()
coroutine = future_result(future)
next(coroutine)

# the result of the future is set somewhere
# we just fake setting it here
future.set_result(123)

try:
    next(coroutine)
except StopIteration as e:
    result = e.value
    print(result)
```

````{hint}
To clarify how the `Future` works, `future_result` could be rewritten as

```python
def future_result(future):
    # __iter__ implements the Iterable protocol and
    # returns a coroutine/generator/iterator
    coroutine = future.__iter__()
    return (yield from coroutine)
```

or even more detailed without `yield from`

```python
def future_result(future):
    # __iter__ implements the Iterable protocol and
    # returns a coroutine/generator/iterator
    coroutine = future.__iter__()
    try:
        while True:
            x = next(coroutine)
            yield x
    except StopIteration as e:
        return e.value
```
````

As a result we have an object that allows to set a result (even) in a future
step.

Example Usage:

```python
def do_something(future):
    # do something, for example:
    # * start a thread
    # * wait for something being returned from the thread via a callback
    def on_result_from_thread(result):
        future.set_result(result)

    thread = thread.create()
    thread.on_exit = on_result_from_thread

def some_result():
    future = Future()
    do_something(future)
    return (yield from future)
```

Simple example without real purpose:

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

```{admonition} Summary
* We learned the basic concept of a `Future`
```
