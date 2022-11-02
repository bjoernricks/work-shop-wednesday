### Async/Await

Similar to the `yield` statement and generators, every function with an `async` prefix is a coroutine function. Calling the coroutine function doesn't execute
the code directly instead it returns a coroutine object.

```python
 async def foo():
    pass

print(type(foo))
coro = foo()
print(type(coro))
print(dir(coro))
```

Output:

```python
>>> print(type(foo))
<class 'function'>
>>> coro = foo()
>>> print(type(coro))
<class 'coroutine'>
>>> print(dir(coro))
['__await__', ...]
```

These coroutine objects implement the `awaitable` protocol.

Besides the [`async def` function definition](https://docs.python.org/3.10/reference/compound_stmts.html#coroutine-function-definition) there are
additional new expressions and statements. [`await`](https://docs.python.org/3.10/reference/expressions.html#await)
for awaiting a coroutine result, [async for](https://docs.python.org/3.10/reference/compound_stmts.html#the-async-for-statement)
for iterating over async iterables and [async with](https://docs.python.org/3.10/reference/compound_stmts.html#the-async-with-statement)
for async context managers.

> `await` expressions, `async for` and `async with` can only be used in the body
> of a coroutine function.
>
> Functions defined with async def syntax are always coroutine functions, even
> if they do not contain await or async keywords.

[Source](https://docs.python.org/3.10/reference/compound_stmts.html#coroutine-function-definition)


