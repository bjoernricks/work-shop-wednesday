### Step 10 - Scheduling all the time

The [last step](step9) introduced a new `Task` class that runs a loop over a provided
coroutine. But wait isn't there an existing loop already? Yes indeed. Our
`Loop` class. Why not extend the `Loop` class to run this loop too.


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

The `Loop` class is extended to allow scheduling `Task`s for the next step/tick.
All scheduled `Task`s are run in the next tick/step.

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

The `Task` is refactored to not run a loop by itself. Instead it schedules its
execution via the `Loop`.

Let's take a look at our simple example:

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

Both tasks are still run sequentially. Let's change that.

````{tab} Source
:new-set:
```{literalinclude} step10_2.py
:language: python
```
````
````{tab} Diff
```{literalinclude} step10.diff
:language: diff
```
````

Output:

```
Loop step 1 []
Loop step 2 [<Task name='Add X' id='0x7fe9c7e6d240'>, <Task name='Add Y' id='0x7fe9c7e6e290'>]
Loop step 3 []
Loop finished with result 3
```

```{admonition} Summary
* The `Loop` schedules tasks now.
* The `Task` itself has no loop anymore to run the coroutine.
* `Task`s can be run immediately and concurrently.
```
