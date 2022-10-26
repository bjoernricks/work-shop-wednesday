### Step 10 - Scheduling all the time

The [last step](step9) introduced a new `Task` class that runs a loop over a provided
coroutine. But wait isn't there an existing loop already? Yes indeed. Our
`Loop` class. Why not extend the `Loop` class to run this loop.


````{tab} Source
```{literalinclude} loop.py
:language: python
:caption: Loop v3
```
````
````{tab} Diff
```{literalinclude} loop.diff
:language: diff
:caption: Loop v3
```
````

````{tab} Source
:new-set:
```{literalinclude} task.py
:language: python
:caption: Task v2
```
````
````{tab} Diff
```{literalinclude} task.diff
:language: diff
:caption: Task v2
```
````

```{literalinclude} step10_1.py
:language: python
```

Output:

```
Loop step 1 []
Loop step 2 [<Task name='Add X' id='0x7f44a8c33b80'>]
Loop step 3 [<Task name='Add Y' id='0x7f44a8c33b80'>]
Loop finished with result 3
```

```{literalinclude} step10_2.py
:language: python
```

Output:

```
Loop step 1 []
Loop step 2 [<Task name='Add X' id='0x7fe9c7e6d240'>, <Task name='Add Y' id='0x7fe9c7e6e290'>]
Loop step 3 []
Loop finished with result 3
```

```{admonition} Summary
* The loop schedules tasks now
* The Task itself has no loop anymore to run the coroutine
* Tasks are run immediately and concurrently
```
