### The Coroutine/Generator Issue

Let's take a look at our [Coroutine/Generator Issue](../coroutine_generator_issue.md)
again now we have the new `async/await` syntax.

* ~~We have (mis-)used the generators~~

  Fixed: Generators and Coroutines are separated concepts and objects now.

* ~~Generators/Iterators are intended for yielding something that is consumed by
  the caller.~~
* ~~Implementation wise we have the same thing, but semantically they are very
  different.~~

  Fixed: Generators/Iterators are a different concept now and we have async
  versions of both too.

* ~~Coroutines in contrast use `yield` and `yield from` to just suspend the
  current function and give control back to the loop.~~

  We have `await` instead of `yield from` and suspending is carefully hidden in
  `Awaitables` like `Futures` and `Tasks`.

* ~~From looking at the code or the object users still could mix up coroutines and
  generators because it relies just on a technical detail.~~
* ~~Using `yield`/`yield from` somewhere in a function declaration to make the
  function asynchronous is not very obvious.~~

  Fixed: By using `async def` for coroutines they are much easier to identify
  and prone against mixing them up.

* ~~Users could still pass generators and generators could still run coroutines
  because nothing forbids to use coroutines as generators and the other way
  round.~~

  Fixed: It's not possible to use generators as coroutines with Python 3.11
  anymore.

* ~~Users could refactor a generator function that it becomes a normal function
  (accidentally) just because `yield`/`yield from` is removed.~~

  Fixed: Can't happen with `async def`. The identity of a coroutine doesn't
  depend on a statement within the function. It is already settled during the
  function definition.
