## Context Managers

When using resources like files, memory, network connections, ... it is
desirable to release the resources after they aren't in use anymore. Otherwise
it can cause several issues like not being able to create another connection or
various [memory leaks](https://en.wikipedia.org/wiki/Memory_leak).

Of course this could be avoided like in the following code:

```python
connection = create_connection()
# use the connection, for example send bytes
connection.shutdown()

file = open("foo.txt")
# do something with the file, for example read and write bytes
file.close()

lock = acquire_lock()
# run code that requires exclusive access
lock.release()
```

This approach has some drawbacks

* It requires to standardize the releasing method (for example to always to use
   `close`).
* The releasing method may be called conditionally at different places. That
  means it is not closed in all required cases.
* The releasing method might never be called because it is just forgotten, the
  documentation wasn't read, ...
* Errors may occur and exceptions will be raised.

Especially the last item would always require to write code such as:

```python
try:
    file = open("foo.txt")
    # do something with the file
finally:
    file.close()
```

where *do something with the file* can be very long, contain function calls,
conditionals, additional error handling and therefore may not always be obvious.
It gets verbose very quickly and is prone to forget some release action.

### Context Manager Protocol

As you have seen in the previous examples handling resources consists of two
phases: 1. **acquiring** (or setup) 2. **releasing** (or shutdown)

Context Managers have been introduced to handle the process of acquiring and
releasing of resources automatically even under error conditions.

Let us take a look at the Context Manager base class:

```python
class ContextManager:
    def __enter__(self):
        """
        Setup and acquire the resource and return it
        """

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Shutdown and release the resource even if an error was raised
        """
```

The `__enter__` method is intended to setup and acquire a resource. The resource
object or an object handling the resource may be returned from the method
optionally.

The `__exit__` method is intended to shutdown and release the resource and gets
the current error information passed if an error was raised.

### The With Statement

Context Managers are used in conjunction with the `with` statement.

The `with` statement is defined as:

```python
with EXPRESSION as TARGET:
    SUITE
```

where the *as TARGET* part is optional.

This is semantically equivalent to:

```python
manager = (EXPRESSION)
value = manager.__enter__(manager)
hit_except = False

try:
    TARGET = value
    SUITE
except:
    hit_except = True
    if not manager.__exit__(*sys.exc_info()):
        raise
finally:
    if not hit_except:
        manager.__exit__(None, None, None)

```

TARGET will get the return value of the Context Manager's `__enter__` method.
The `__exit__` method will be called either with the exception and traceback
information in case of an error, or when the code of SUITE has finished. In case
of an error the Context Manager can suppress the fall through of the error by
returning a truthy value from the `__exit__` method.

> With more than one item, the context managers are processed as if multiple
> with statements were nested:

```python
with A() as a, B() as b:
    SUITE
```

is semantically equivalent to:

```python
with A() as a:
    with B() as b:
        SUITE
```

[Source](https://docs.python.org/3.10/reference/compound_stmts.html#the-with-statement)

### Implementing a Context Manager using contextlib

Using [contextlib.contextmanager](https://docs.python.org/3/library/contextlib.html#contextlib.contextmanager) decorator allows for implementing a `Context Manager` easily by
using a generator/iterator function.

```python
from contextlib import contextmanager

@contextmanager
def managed_resource(*args, **kwds):
    # Code to acquire resource, e.g.:
    resource = acquire_resource(*args, **kwds)
    try:
        yield resource
    finally:
        # Code to release resource, e.g.:
        release_resource(resource)
```

This is equivalent to


```python
class managed_resource:
    def __init__(*args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.resource = None

    def __enter__(self):
        self.resource = acquire_resource(*self.args, *self.kwargs)
        return self.resource

    def __exit__(self, exc_type, exc_value, exc_traceback):
        release_resource(self.resource)
```

The implementation of the `contextmanager` decorator could be as following:

```python
class GeneratorContextManager:

    def __init__(self, generator):
        self.generator = generator

    def __enter__(self):
        return self.generator.send(None)

    def __exit__(self, exc_type, exc_value, exc_traceback):
       if exc_type is None:
           try:
               self.generator.send(None)
           except StopIteration:
               return
           else:
               raise RuntimeError("generator didn't stop")
       else:
           try:
               self.generator.throw(exc_type, exc_value, exc_traceback)
               raise RuntimeError("generator didn't stop after throw()")
           except StopIteration:
               return True
           except:
                raise

def contextmanager(func):
   def wrapper(*args, **kwargs):
       return GeneratorContextManager(func(*args, **kwargs))
   return wrapper
```

[Source](https://peps.python.org/pep-0343/#generator-decorator)

### Example Context Managers

Additional examples for using Context Manager even beyond strict resource
acquisition and release.

#### Example 1 - Redirect Stdout

A Context Manager to redirect stdout to some other IO object.

```python
import sys

class RedirectStdout:
    def __init__(self, new_target):
        self._new_stdout = new_target
        self._old_stdout = None
    def __enter__(self):
        self._old_stdout = sys.stdout
        sys.stdout = self._new_stdout
        return self._new_stdout
    def __exit__(self, exc_type, exc_value, exc_traceback):
        sys.stdout = self._old_stdout
```

```python
with open('help.txt', 'w') as f, RedirectStdout(f):
    help(print)
```

A similar Context Manager is available in the Python standard library [`contextlib.redirect_stdout`](https://docs.python.org/3/library/contextlib.html#contextlib.redirect_stdout).


#### Example 2 - Suppress Exceptions

A Context Manager to suppress all raised exceptions.

```python
from contextlib import contextmanager

@contextmanager
def catch_all():
    try:
        yield
    except:
        pass
```

```python
with catch_all():
    raise RuntimeException("foo")
```

A related Context Manager is available in the Python standard library [`contextlib.suppress`](https://docs.python.org/3/library/contextlib.html#contextlib.suppress).


#### Example 3 - Add a directory to the Python module search path

```python
import sys

@contextmanager
def add_module_path(path: str):
    sys.path.append(path)

    try:
        yield
    finally:
        try:
            sys.path.remove(path)
        except ValueError:
            # path is not in sys.path
            pass
```

#### Example 4 - Print Prefix

```python
class PrintPrefix:
    def __init__(self, prefix: str):
        self.prefix = prefix
        self.active = False
    def print(self, *args, **kwargs):
        if self.active:
            print(self.prefix, *args, **kwargs)
        else:
            print(*args, **kwargs)
    def __enter__(self):
        self.active = True
        return self
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.active = False
```

```python
with PrintPrefix("😀") as out:
    out.print("are we happy now?")

### Links

* [With Statement Context Managers](https://docs.python.org/3.10/reference/datamodel.html#with-statement-context-managers)
* [Context Manager Types](https://docs.python.org/3.10/library/stdtypes.html#typecontextmanager)
* [PEP 343 – The “with” Statement](https://peps.python.org/pep-0343/)
* [Real Python – Context Managers and Python's with Statement](https://realpython.com/python-with-statement/)
