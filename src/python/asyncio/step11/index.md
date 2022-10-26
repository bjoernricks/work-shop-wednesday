### Step 11 - Schedule Callbacks

```{literalinclude} handle.py
:language: python
:caption: Handle
```

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
* Using a callback abstraction makes the scheduling more generic
* Our loop can schedule and run all kind of things using a callback
```
