### Support for `async/await` in our own Implementation

So what's necessary for supporting `async/await` in our [implementation](../implementing.md)?
Just a single line needs to be added:

````{tab} Source
```{literalinclude} future.py
:language: python
:caption: Future v5
```
````
````{tab} Diff
```{literalinclude} future.diff
:language: diff
:caption: Future v5
```
````

```{literalinclude} stepz.py
:language: python
```

Output:
```
Loop step 1 [<Handle name='Initial Task' callback='step'>]
Loop step 2 [<Handle name='Add X' callback='step'>, <Handle name='Add Y' callback='step'>]
Loop step 3 [<Handle name='Some Result' callback='_wakeup'>, <Handle name='Some Result' callback='_wakeup'>]
Loop step 4 [<Handle name='Add X' callback='step'>, <Handle name='Add Y' callback='step'>]
Loop step 5 [<Handle name='Add X' callback='_wakeup'>]
Loop step 6 [<Handle name='Initial Task' callback='step'>]
Loop step 7 [<Handle name='Add Y' callback='_wakeup'>]
Loop step 8 [<Handle name='Initial Task' callback='step'>]
Loop step 9 [<Handle name='Initial Task' callback='_done'>]
Loop finished with result 3
```

