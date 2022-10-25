### Step 6 - The Intermediate Function Issue

Our current concept uses generator functions to call generator functions. But
what about "normal" functions calling generators in between?

```{literalinclude} loop.py
:language: python
:caption: Loop v1
```

```{literalinclude} step6.py
:language: python
```

Output:

```python
Loop step 1
main_generator 1
chaining_generator 1
generator_one 1
Loop step 2
generator_one 2
chaining_generator 2
intermediate_function 1
intermediate_function 2
chaining_generator 3
main_generator 2
Loop finished
```

As we can see the `intermediate_function` has run but `generator_two` is never
executed. The `intermediate_function` is blocking our generator based code from
being executed as expected. The only way to fix this is to run another loop in
the `intermediate_function` or to use the `yield from` statement again. But
using `yield from` would also convert the "normal" function into a generator
function.

```{admonition} Summary
* Calling coroutines from normal functions breaks the concept
* Therefore normal functions must not call coroutines
* Coroutines are allowed to call normal functions
```

