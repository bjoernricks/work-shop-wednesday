### Step 10 - Scheduling all the time

The last step introduced a new `Task` class that runs a loop over a provided
coroutine. But wait isn't there an existing loop already? Yes indeed. Our
`Loop` class. Why not extend the `Loop` class to run this loop.


```{literalinclude} loop.py
:language: python
:caption: Loop v3
```

```{literalinclude} task.py
:language: python
:caption: Task v2
```

```{literalinclude} step10.py
:language: python
```

```{admonition} Summary
```
