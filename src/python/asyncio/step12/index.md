### Step 12 - Back to the Future

Currently a `Future` is `done` in exactly two steps/ticks of the `Loop`.


```python
from future import Future

future = Future()
it = iter(future)
# step 1
next(it)
# step 2
# still no result yet
next(it)
```

A `StopIteration` exception is raised without a value set at the second step.

````{hint}
Remember `yield from future` is the same as
```python
it = iter(future)
while True:
  try:
    value = next(it)
    yield value
  except StopIteration as e:
    return e.value
```
````

What if we need to wait for more then one step/tick for example to wait for some
external *event* providing the result?

````{tab} Source
```{literalinclude} future.py
:language: python
:caption: Future v3
```
````
````{tab} Diff
```{literalinclude} future.diff
:language: diff
:caption: Future v3
```
````

The `Future` is extended to allow adding callbacks that are executed after
a result is set. This allows for getting notified when a `Future` is done. When
the `Future` is done the callbacks are scheduled for the next step/tick in our
`Loop`.

But the actual waiting for some external *event* providing the result is not
implemented directly in a `Future`. Instead the `Task` is extended.

````{tab} Source
:new-set:
```{literalinclude} task.py
:language: python
:caption: Task v4
```
````
````{tab} Diff
```{literalinclude} task.diff
:language: diff
:caption: Task v4
```
````

The `Task` is extended to run a coroutine that is actually being *blocked* by
some external *event*. The coroutine indicates this by yielding a `Future`. If
a `Future` is yielded the `Tasks` registers a wake up callback at this `Future`.
The `Task` is suspended now (it isn't scheduled in the loop anymore). If the
`Future` is done the `Task` is notified and scheduled again via the `Loop`. This
allows the Task to *sleep* for one or more scheduler ticks/steps until some
*event* has occurred.

```{literalinclude} step12.py
:language: python
```

Output:

```
Loop step 1 []
Loop step 2 [<Handle name='Add X' callback='step'>, <Handle name='Add Y' callback='step'>]
Loop step 3 []
Loop finished with result 3
```

```{admonition} Summary
* A `Task` can wait for results that are currently *blocked*.
* If a `Task` gets a `Future` from a coroutine it *blocks* until the `Future` is
  done.
* *Blocked* means the `Task` is suspended, it is not scheduled in the `Loop`
  anymore and the result is not available yet.
* If the result is available finally the `Task` gets notified and schedules
  itself for the next step/tick in the `Loop`.
```
