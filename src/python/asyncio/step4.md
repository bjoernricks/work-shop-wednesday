### Step 4 - A Loop is running

Running the coroutines is very generic now. It calls a `Generator` in a while
loop, which runs until a `StopIteration` exception is raised. Thus it can be
abstracted into a function accepting a `Generator`. Internally it's a loop so
lets call the function loop too.

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
    other_value = yield from other_generator()
    # do something with some_value and other_value

def loop(gen):
    while True:
        try:
            next(gen)
        except StopIteration as e:
            return e.value

loop(main_generator())
```

```{admonition} Summary
* Running the coroutines is done in loop
* Looping over and therefore running the coroutines is generic
```
