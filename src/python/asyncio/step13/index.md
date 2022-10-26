### Step 13 - Let's wait

```{literalinclude} wait.py
:language: python
:caption: wait.py
```

```{literalinclude} step13.py
:language: python
```

Output:

```
Loop step 1 [<Handle name='Initial Task' callback='step'>]
Loop step 2 [<Handle name='Add X' callback='step'>, <Handle name='Add Y' callback='step'>]
Loop step 3 [<Handle name='Some Result' callback='_wakeup'>, <Handle name='Some Result' callback='_wakeup'>]
Loop step 4 [<Handle name='Add X' callback='step'>, <Handle name='Add Y' callback='step'>]
Loop step 5 [<Handle name='Add X' callback='_on_completion'>, <Handle name='Add Y' callback='_on_completion'>]
Loop step 6 [<Handle name='Waiter for <Task name='Add X' id='0x7fb53804d6c0'>, <Task name='Add Y' id='0x7fb53804d780'>' callback='_wakeup'>]
Loop step 7 [<Handle name='Initial Task' callback='step'>]
Loop step 8 [<Handle name='Initial Task' callback='_done'>]
Loop finished with result 3
```

```{admonition} Summary
```
