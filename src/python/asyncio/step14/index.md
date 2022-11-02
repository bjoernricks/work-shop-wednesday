### Step 14 - Let's wait

Often it is desireable to start some coroutines concurrently and wait for their
results. This can be accomplished by wrapping them in Tasks in some `wait`
function.

```{literalinclude} wait.py
:language: python
:caption: wait.py
```

Using the `wait` function our previous example from [Step 13](../step13/index.md)
can be re-written as:

```{literalinclude} step14.py
:language: python
```

Output:

```
Loop step 1 [<Handle name='Initial Task' callback='step'>]
Loop step 2 [<Handle name='Task for some_result' callback='step'>, <Handle name='Task for some_result' callback='step'>]
Loop step 3 [<Handle name='Some Result' callback='_wakeup'>, <Handle name='Some Result' callback='_wakeup'>]
Loop step 4 [<Handle name='Task for some_result' callback='step'>, <Handle name='Task for some_result' callback='step'>]
Loop step 5 [<Handle name='Task for some_result' callback='_on_completion'>, <Handle name='Task for some_result' callback='_on_completion'>]
Loop step 6 [<Handle name='Waiter for <Task name='Task for some_result' id='0x7fe9759a5e40'>, <Task name='Task for some_result' id='0x7fe9759a5f00'>' callback='_wakeup'>]
Loop step 7 [<Handle name='Initial Task' callback='step'>]
Loop step 8 [<Handle name='Initial Task' callback='_done'>]
Loop finished with result 3
```

```{admonition} Summary
* Using specific `wait` functions allow ot gather results from concurrent
  `Task`s more easily.
```
