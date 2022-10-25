### Step 1 - Coroutine Concept

To explain the concept in full detail let us look at standard function calls
again.

```python
def function():
    # do something
    return # some value

def other_function():
    # do something else
    return # another value

some_value = function()
another_value = other_function()
```

As a sequence diagram:

```{mermaid}
sequenceDiagram
  participant c as Caller
  participant f1 as Function
  participant f2 as Other Function
  activate c
  activate c
  c->>f1: call
  deactivate c
  activate f1
  f1->>c: return
  deactivate f1
  activate c
  c->>f2: call
  deactivate c
  activate f2
  f2->>c: return
  deactivate f2
  deactivate c
```

All function calls are run in a sequence. The caller must wait until the
function is finished to execute its next code for example another function call.

Besides let us take a look at `Generators`/`Iterators`.

```python
def generator():
    # do something
    yield # something
    # do something else
    yield # something else
    # do another thing
    return # some value

def function():
    # do something
    return # a value


gen = generator()
next(gen)
next(gen)
a_value = function()
try:
    next(gen)
except StopIteration as e:
    some_value = e.value
```

Also as a sequence diagram:

```{mermaid}
sequenceDiagram
  participant c as Caller
  participant g as Generator
  participant f as Function
  activate c
  activate c
  c->>g: next
  deactivate c
  activate g
  activate g
  g-->>c: yield
  deactivate g
  activate c
  c->>g: next
  deactivate c
  activate g
  g-->>c: yield
  deactivate g
  activate c
  c->>f: call
  deactivate c
  activate f
  f->>c: return
  deactivate f
  activate c
  c->>g: next
  deactivate c
  activate g
  g->>c: return/StopIteration
  deactivate g
  deactivate g
  deactivate c
```

A `Generator` can yield values to his called during its execution. The caller
can request the next value from the `Generator` and do other things in between
for example calling a function.

```{admonition} Summary
* Calling a function blocks the caller until the function returns.
* A `Generator` can give control back to the caller.
* The caller can do other things after getting in control again like calling
  another function.
* The caller can resume the `Generator`.
* The caller doesn't need to be interested in the **yielded** values.
* A `Generator` can return a *final* value just like a function.
* A `Generator` is a coroutine.
```

```{note}
When mentioning the term `coroutine` in the following steps of this chapter,
it references a Python `generator function` or `generator object`.
```

