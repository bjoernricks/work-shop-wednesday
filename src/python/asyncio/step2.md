### Step 2 - Multiple Coroutines

Lets take a look at a call flow calling multiple coroutines concurrently.

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


gen1 = generator()
next(gen1)
gen2 = other_generator()
next(gen1)
next(gen2)
try:
    next(gen1)
except StopIteration as e:
    some_value = e.value
try:
    next(gen2)
except StopIteration as e:
    other_value = e.value
```

```{mermaid}
sequenceDiagram
  participant c as Caller
  participant g1 as Generator
  participant g2 as Other Generator
  activate c
  activate c
  c->>g1: send/next
  deactivate c
  activate g1
  activate g1
  g1-->>c: yield
  deactivate g1
  activate c
  c->>g2: send/next
  deactivate c
  activate g2
  activate g2
  g2->>c: yield
  deactivate g2
  activate c
  c->>g1: send/next
  deactivate c
  activate g1
  g1-->>c: yield
  deactivate g1
  activate c
  c->>g1: send/next
  deactivate c
  activate g1
  g1->>c: return/StopIteration
  deactivate g1
  deactivate g1
  activate c
  c->>g2: send/next
  deactivate c
  activate g2
  g2->>c: return/StopIteration
  deactivate g2
  deactivate g2
  deactivate c
```

```{admonition} Summary
* The caller can use several coroutines concurrently.
* The caller is in control which coroutine and when a coroutine is resumed.
* The caller needs to catch the `StopIteration` exception of each coroutine to
  get the return values.
```
