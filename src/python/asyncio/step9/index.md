(step9)=

### Step 9 - A Job has to be done

Let us look at the example from the last step again with some more output.

```{literalinclude} step9_1.py
:language: python
```
Output:

```python
Loop step 1
main 1
add 1
some_result 1
Future 1
Loop step 2
Future 2
add 2
some_result 1
Future 1
Loop step 3
Future 2
add 3
main 1
Loop finished with result 3
```

As you can see there is still no real concurrency. Only a single coroutines is
run until it is finished before another one is called.

Yes we can suspend the current function but we still run all coroutines
sequentially.

To change that we need a new thing.
1. This thing should take a coroutine, because all our business logic uses
   coroutines.
2. It should run the coroutine immediately, because we want to get a job done.
3. It should run until a job is finally done.
4. And its result should be gathered in the future.

Because a result should be gathered in the future, let's derive the new thing
from `Future`. A job can be worked on in a task. So let's call this new thing
`Task`. But first let's extend our `Future` a bit.


````{tab} Source
```{literalinclude} future.py
:language: python
:caption: Future v2
```
````
````{tab} Diff
```{literalinclude} future.diff
:language: diff
:caption: Future v2
```
````

The `Future` class got a `done` method to check if the result has been set and
also a `result` method to allow accessing the result from the outside of the
class. Now it is possible to check whether the state of the `Future` is done.
Additionally it is possible to pass a name to identify the `Future` via
 `__repr__` more easily in later steps for debugging purposes.

```{literalinclude} task.py
:language: python
:caption: Task v1
```

```{literalinclude} step9_2.py
:language: python
```

Output:

```
Loop step 1
Loop step 2
Loop step 3
Loop finished with result 3
```

First of all the functionality and the result hasn't changed. We just introduced
a new class that wraps our coroutines.


```{admonition} Summary
* We have a basic `Task` class that runs a coroutine in a loop.
* The coroutine is started immediately.
* The `Task` returns the result of the coroutine in the future when it's done.
```

