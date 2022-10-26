### Step 3 - Adding `yield from`

In the last steps we needed to catch the `StopIteration` of each coroutine to
get their values. And even further we needed to catch it at the right resume
call with next. What if we could resume the coroutines until we are just done
and get the values automatically?

That is where `yield from` comes into play. We abstract our business logic into
a single main generator function and call the coroutines via `yield from`.
Afterwards we can call the main generator function easily in a while loop until
`StopIteration` is raised.

```python
def generator():
    # do something
    yield # something
    # do something else
    yield # something else
    # do another thing
    return # some value

def other_generator():
    # do something
    yield # something
    # do something else
    return # other value

def main_generator():
    some_value = yield from generator()

    # yield from generator() is the same as
    # gen = generator()
    # try:
    #     while True:
    #         x = next(gen)
    #         yield x
    # except StopIteration as e:
    #     some_value = e.value

    other_value = yield from other_generator()

    # yield from other_generator() is the same as
    # gen = other_generator()
    # try:
    #     while True:
    #         x = next(gen)
    #         yield x
    # except StopIteration as e:
    #     some_value = e.value

    return (some_value, other_value)

gen = main_generator()

while True:
    try:
        next(gen)
    except StopIteration as e:
        return e.value
```

```{admonition} Summary
* Using `yield from` allows to write call flow sequences as they would just
  contain normal function calls.
* Using a single main generator allows for simplifying the business logic
  without having to care about the `Generator` boilerplate
  (next iteration, catching `StopIteration`).
```
