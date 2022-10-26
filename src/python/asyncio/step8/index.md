### Step 8 - Extend the Loop

As a next step we want to extend the loop so that we can get the current loop.

```{literalinclude} loop.py
:language: python
:caption: Loop v2
```

The loop has been converted into a class the uses a singleton pattern to return
the current loop. The current loop is now accessible via `Loop.get_current_loop()`.
A coroutine can be started by calling the `run` method on the loop instance.

```{literalinclude} step8.py
:language: python
```

Output:
```
Loop step 1
Loop step 2
Loop step 3
Loop finished with result 3
```

```{admonition} Summary
* The loop will not be instantiated by the application code directly anymore.
* Instead the current loop is requested at a single API point.
* The loop could decide wether it returns a new instance or not.
```
