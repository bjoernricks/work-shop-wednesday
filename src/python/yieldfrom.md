## Yield From

With Python 3.3 and [PEP 380](https://peps.python.org/pep-0380) a new
`yield from` statement got introduced that can be used to simplify chaining
Iterators and Generators.


### Chaining Iterators

Chaining `Iterators` without the new `yield from` statement.

```python
def get_something_generator():
    yield "foo"
    yield "bar"
    yield "baz"

def another_generator():
    for i in get_something_generator():
        yield i

for i in another_generator():
    print(i)
```

Using the `yield from` statement this can be simplified to:

```python
def get_something_generator():
    yield "foo"
    yield "bar"
    yield "baz"

def another_generator():
    yield from get_something_generator()

for i in another_generator():
    print(i)
```

Easy and straight forward. Just a simplification of the syntax.

### Chaining Generators

Chaining `Generators` with their `send`, `throw` and `close` semantics is much
more complicated and more prone for errors. A very simplified implementation
without `yield from` could be:

```python
def some_generator():
    sent = yield 0
    while sent >= 0:
        sent = yield sent
    return 'Done'

def another_generator():
    generator = some_generator()

    y = generator.send(None)

    while True:
        try:
            x = yield y
            y = generator.send(x)
        except GeneratorExit as e:
            # forward close
            generator.close()
            raise e
        except Exception as e:
            # forward throw
            generator.throw(e)
```

Using `yield from` is of course much simpler.

```python
def some_generator():
    sent = yield 0
    while sent >= 0:
        sent = yield sent
    return 'Done'

def another_generator():
    return yield from some_generator()
```

### Additional Semantics

But beside from the simplification it also got some additional semantically
change regarding the return value.

```
RESULT = yield from EXPR
```

```python
def some_generator():
    sent = yield 0
    while sent >= 0:
        sent = yield sent
    return 'Done'

def another_generator():
    generator = some_generator()
    try:
        y = generator.send(None)
    except StopIterator as e:
        result = e.value
    else:
        while True:
            try:
                x = yield y
                y = generator.send(x)
            except GeneratorExit as e:
                # forward close
                generator.close()
                raise e
            except Exception as e:
                # forward throw
                generator.throw(e)
            except StopIterator as e:
                result = e.value
                break
        return result
```

Because

```python
y = yield from g(x)
```

looks much more familiar like a normal function call

```
y = f(x)
```

but shows that y is received from a coroutine.

### Links

* [PEP 380 – Syntax for Delegating to a Subgenerator](https://peps.python.org/pep-0380/)
