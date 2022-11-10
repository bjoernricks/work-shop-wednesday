### Issues with asyncio

#### RuntimeWarning: coroutine 'xyz' was never awaited

A very common mistake is to forget the `await` statement when calling
coroutines. You will run into it several times. I Promise!

```python
import asyncio

async def coro():
  return 42


async def other_coro():
  coro()

asyncio.run(other_coro())
```

Output:

```
<stdin>:2: RuntimeWarning: coroutine 'coro' was never awaited
RuntimeWarning: Enable tracemalloc to get the object allocation traceback
```

#### Structured Concurrency

* [Notes on structured concurrency, or: Go statement considered harmful](https://vorpus.org/blog/notes-on-structured-concurrency-or-go-statement-considered-harmful/)

> Whenever a coroutine function is run, it might or might not spawn some
> background task. The function seemed to return, but is it still running in the
> background? There's no way to know without reading all its source code,
> transitively. When will it finish? Hard to say.

> If an error occurs in a background task, and you don't handle it manually,
> then the runtime just... drops it on the floor and crosses its fingers that it
> wasn't too important. If you're lucky it might print something on the console.

[Source](https://vorpus.org/blog/notes-on-structured-concurrency-or-go-statement-considered-harmful/#go-statement-considered-harmful)

When running a coroutine function it always may create a `Task` and the code
execution is forked actually. This `Task` can be passed around, maybe cancelled,
raise exceptions and may even create additional `Task`s. All this may be hidden
to the caller. Nothing ensures that the `Task` execution is *joined* later on.


```{mermaid}
flowchart TB
   a[Start] --> b[Task]
   subgraph main
   a --> c[next statement]
   end
   subgraph forked
   b --> d[some operation]
   end
```

```{mermaid}
flowchart TB
   a[Start] --> b[forked Task]
   a --> c[next statement]
   b --> join
   c --> join
```

Different async based libraries are addressing this issue
 * [curio](https://curio.readthedocs.io/en/latest/tutorial.html#task-groups)
 * [trio](https://trio.readthedocs.io/en/latest/reference-core.html#nurseries-and-spawning)

This issue has been fixed in Python 3.11 with the introduction of
[TaskGroups](https://docs.python.org/3.11/library/asyncio-task.html#task-groups).

Before:

```python
async def main():
    task1 = asyncio.create_task(some_coro(...))
    task2 = asyncio.create_task(another_coro(...))
     # join all tasks explicitly
    await asyncio.gather(task1, task2)
    print("Both tasks have completed now.")

```

With Python 3.11:

```python
async def main():
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(some_coro(...))
        task2 = tg.create_task(another_coro(...))
    # tasks are joined automatically
    print("Both tasks have completed now.")
```

#### asyncio is not the only async library

Every async library call flow in Python must work like this

`async-lib-x` -> `coroutine` -> `...` -> `coroutine` -> `async-lib-x`

You might know already the reason for this. Every async library needs a loop and
the loop needs to track all jobs, tasks, etc. Therefore it needs to track also
all I/O to notify waiting coroutines.

So if you are an author of a networking protocol library you need to support
`async-lib-x` explicitly to work correctly with your library.

To name the major ones:

 * [asyncio](https://docs.python.org/3/library/asyncio.html)
 * [curio](https://github.com/dabeaz/curio)
 * [trio](https://github.com/python-trio/trio)
 * [anyio](https://github.com/agronholm/anyio)

Supporting all of them seems to be a big burden when you only want to get
*faster code with async/await*.

```{admonition} Personal Advice
Just stick with asyncio. It is a standard Python library and is still relatively
new. During the years it got improved with every Python release. Most async
libraries will only support asyncio and with `TaskGroups` a major downside is
already resolved.
```

#### Coloured Functions

* [What Color is Your Function?](http://journal.stuffwithstuff.com/2015/02/01/what-color-is-your-function/)
* [What Color is Your Python async Library?](https://quentin.pradet.me/blog/what-color-is-your-python-async-library.html)

In [What Color is Your Function?](http://journal.stuffwithstuff.com/2015/02/01/what-color-is-your-function/)
the author argues that every function has a color. There a no functions without
a color. He introduced blue and red colored functions. You can call a blue
function from within a red one but you can't call a red function from within a
blue one. That means red functions are getting more painful to handle then blue
ones. Best would be to just have blue functions overall but sadly some core
functions are red. Thus you can't avoid them.

Of course this is only an analogy of async and sync functions. Let's take a look
at the following table:

| If a function like this | wants to call a function like this | does it work? |
|-------------------------|------------------------------------|---------------|
| sync | sync | ✓ |
| sync | async | X |
| async | sync | ✓ |
| async | async | ✓ |

[Source](https://trio.readthedocs.io/en/latest/tutorial.html#async-functions)

Remember the [Intermediate Function Issue](../step6/index.html). It's still the
same with native coroutine functions. You still can't call async functions from
synchronous ones. The `async/await` syntax didn't change the situation.

And think [about this](./async_generators.md#async-generator-function) and
[asyncio-is-not-the-only-async-library](#asyncio-is-not-the-only-async-library)
again. Therefore as also mentioned in [What Color is Your Python async Library?](https://quentin.pradet.me/blog/what-color-is-your-python-async-library.html)
we have much more then two colors in Python.

And you just can't implement all these colors under the same namespace:

```python
class SomeClass:
    def same_name(self):       # a function (method)
        return

    def same_name(self):       # a generator function
        yield

    async def same_name(self): # a coroutine function
        await smth()

    async def same_name(self): # an asynchronous generator function
        await smth()
        yield 42

    async def same_name(self): # a coroutine function using a different async lib
        await asynclibx.smth()
```

and `async-lib-x` -> `coroutine` -> `...` -> `coroutine` -> `async-lib-y` will
not work at all too.
