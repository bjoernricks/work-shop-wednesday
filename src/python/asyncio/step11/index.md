### Step 11 - Schedule Callbacks

The `Loop` is currently stuck to schedule `Task`s and run coroutines.
We could introduce a new `Protocol` to abstract the scheduling of `Tasks` but
at the end we just need to scheduling some callbacks (which are actually
`Callable`s) and together with their arguments. Therefore we introduce an
internal class `Handler`.

```{literalinclude} handle.py
:language: python
:caption: Handle
```

Let's arrange our `Loop` to schedule `Handle` instances.

````{tab} Source
```{literalinclude} loop.py
:language: python
:caption: Loop v4
```
````
````{tab} Diff
```{literalinclude} loop.diff
:language: diff
:caption: Loop v4
```
````

The scheduler method (`run_step`) now loops over `Handle` instances instead of
`Task`s. The `schedule` method got adjusted to accept a `Callable` as callback
and some arguments. These are put into a `Handle` which gets scheduled for the
next step/tick.

````{tab} Source
:new-set:
```{literalinclude} task.py
:language: python
:caption: Task v3
```
````
````{tab} Diff
```{literalinclude} task.diff
:language: diff
:caption: Task v3
```
````

The `Task` requires only a small change. Instead of passing itself to the loop,
it passed its `step` method for being scheduled and its name for debugging
purposes.

```{literalinclude} step11.py
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
* Using a callback abstraction makes the scheduling more generic.
* Our loop can schedule and run all kind of things using a callback.
```
