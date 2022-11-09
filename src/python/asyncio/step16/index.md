### Step 16 - Cancellation

````{tab} Source
```{literalinclude} future.py
:language: python
:caption: Future v4
```
````
````{tab} Diff
```{literalinclude} future.diff
:language: diff
:caption: Future v4
```
````

````{tab} Source
:new-set:
```{literalinclude} task.py
:language: python
:caption: Task v5
```
````
````{tab} Diff
```{literalinclude} task.diff
:language: diff
:caption: Task v5
```
````

```{literalinclude} step16.py
:language: python
```

Output:

```python
Loop step 1 [<Handle name='Initial Task' callback='step'>]
Loop step 2 [<Handle name='Task for some_result' callback='step'>, <Handle name='Task for cancelled_result' callback='step'>]
Loop step 3 [<Handle name='Some Result' callback='_wakeup'>, <Handle name='Some Result' callback='_wakeup'>]
Loop step 4 [<Handle name='Task for some_result' callback='step'>, <Handle name='Task for cancelled_result' callback='step'>]
Loop step 5 [<Handle name='Task for some_result' callback='_on_completion'>, <Handle name='Task for cancelled_result' callback='_on_completion'>]
Loop step 6 [<Handle name='Waiter for <Task name='Task for some_result' state=FutureState.PENDING id='0x7f3cd90b6530'>, <Task name='Task for cancelled_result' state=FutureState.PENDING id='0x7f3cd90b65c0'>' callback='_wakeup'>]
Loop step 7 [<Handle name='Initial Task' callback='step'>]
Loop step 8 [<Handle name='Initial Task' callback='_done'>]
Loop got cancelled
```
