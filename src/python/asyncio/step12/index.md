### Step 12 - Back to the Future

Currently a `Task` is `done` in exactly two steps/ticks of the `Loop`. What if
we need to wait for more then one step/tick for some external *event* providing
a result?

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

````{tab} Source
:new-set:
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

The `Task` is extended to run a coroutine that is actually being blocked by some
external *event*. This is indicated by yielding a `Future`. If a `Future` is
yielded the `Tasks` registers a wake up callback at the `Future`. If the
`Future` is done the `Task` is scheduled again via the `Loop`. This allows for
the Task to *sleep* for one or more scheduler ticks/steps until some *event* has
occurred.

```{literalinclude} step12.py
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
* A `Task` can wait for results that are currently *blocked*.
* If a `Task` gets a `Future` from a coroutine it *blocks* until the `Future` is
  done.
* *Blocked* means the `Task` is suspended and the result is not available yet.
```
