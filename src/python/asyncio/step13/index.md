### Step 13 - Deduplicate Running Coroutines

Currently the code for running a coroutine

```python
try:
    next(coroutine)
except StopIteration as e:
    result = e.value
```

can be found twice in our code. Once in the `Task` class and another time in the
`Loop` class. With the new `add_done_callback` also being available at the
`Task` class (because it derives from the `Future`) we could create an initial
root `Task` that runs the main coroutine in the `Loop`. If that root `Task` is
done our `Loop` is done too.

````{tab} Source
```{literalinclude} loop.py
:language: python
:caption: Loop v5
```
````
````{tab} Diff
```{literalinclude} loop.diff
:language: diff
:caption: Loop v5
```
````

The `Loop` doesn't know anything about the `Generator`/`Iterator` protocol
anymore. It just starts a coroutine in a `Tasks` and schedules `Handle`s.
Instead the `Task`s are resuming the coroutines via the `Generator`/`Iterator`
protocol.


```{literalinclude} step13.py
:language: python
```

Output:

```
Loop step 1 [<Handle name='Initial Task' callback='step'>]
Loop step 2 [<Handle name='Add X' callback='step'>, <Handle name='Add Y' callback='step'>]
Loop step 3 [<Handle name='Some Result' callback='_wakeup'>, <Handle name='Some Result' callback='_wakeup'>]
Loop step 4 [<Handle name='Add X' callback='step'>, <Handle name='Add Y' callback='step'>]
Loop step 5 [<Handle name='Add X' callback='_wakeup'>]
Loop step 6 [<Handle name='Initial Task' callback='step'>]
Loop step 7 [<Handle name='Add Y' callback='_wakeup'>]
Loop step 8 [<Handle name='Initial Task' callback='step'>]
Loop step 9 [<Handle name='Initial Task' callback='_done'>]
Loop finished with result 3
```

```{admonition} Summary
* It's possible have code to handle coroutines at a single place.
* `Task`s are dedicated to run coroutines.
* Starting an initial root `Task` allows the `Loop` to be completely independent
  of coroutines.
```
