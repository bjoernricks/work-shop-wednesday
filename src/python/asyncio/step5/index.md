### Step 5 - A runnable Example

Lets take a look at our current concept by using a runnable example.


```{literalinclude} loop.py
:language: python
:caption: Loop v1
```

```{literalinclude} step5.py
:language: python
```

Output:

```python
Loop step 1
main_generator 1
chaining_generator 1
generator_one 1
Loop step 2
generator_one 2
chaining_generator 2
generator_two 1
Loop step 3
generator_two 2
Loop step 4
generator_two 3
chaining_generator 3
main_generator 2
Loop finished with result None
```

As a sequence diagram:

```{mermaid}
sequenceDiagram
  participant l as loop
  participant mg as Main Generator
  participant cg as Chaining Generator
  participant g1 as Generator One
  participant g2 as Generator Two
  activate l

  activate l
  l->>mg: next
  deactivate l

  activate mg

  activate mg
  mg->>cg: yield from
  deactivate mg

  activate cg

  activate cg
  cg->>g1: yield from
  deactivate cg

  activate g1

  activate g1
  g1-->>l: yield
  deactivate g1

  activate l
  l->>g1: next
  deactivate l

  activate g1
  g1->>cg: return
  deactivate g1

  deactivate g1

  activate cg
  cg->>g2: yield from
  deactivate cg

  activate g2

  activate g2
  g2-->>l: yield
  deactivate g2

  activate l
  l->>g2: next
  deactivate l

  activate g2
  g2-->>l: yield
  deactivate g2

  activate l
  l->>g2: next
  deactivate l

  activate g2
  g2->>cg: return
  deactivate g2

  deactivate g2

  activate cg
  cg->>mg: return
  deactivate cg

  deactivate cg

  activate mg
  mg->>l: return
  deactivate mg

  deactivate mg

  deactivate l
```

```{admonition} Summary
We have learned so far:

* `yield` suspends execution of a coroutine.
* Using `yield from` suspends the execution back to the initial caller at the
  root - the loop.
* The loop resumes the execution where the last `yield` was executed.
* A loop is easiest to be implemented as a function that gets a **single**
  coroutine passed as argument. This coroutine may call other coroutines.
```

