from loop import loop


def generator_one():
    print(generator_one.__name__, 1)
    yield
    print(generator_one.__name__, 2)


def generator_two():
    print(generator_two.__name__, 1)
    yield
    print(generator_two.__name__, 2)
    yield
    print(generator_two.__name__, 3)


def intermediate_function():
    print(intermediate_function.__name__, 1)
    generator_two()
    print(intermediate_function.__name__, 2)


def chaining_generator():
    print(chaining_generator.__name__, 1)
    yield from generator_one()
    print(chaining_generator.__name__, 2)
    intermediate_function()
    print(chaining_generator.__name__, 3)


def main_generator():
    print(main_generator.__name__, 1)
    yield from chaining_generator()
    print(main_generator.__name__, 2)


result = loop(main_generator())
print("Loop finished with result", result)
