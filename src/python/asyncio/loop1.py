def loop(coroutine):
    """Loop v1"""

    step = 1
    while True:
        print("Loop step", step)
        try:
            next(coroutine)
            step += 1
        except StopIteration as e:
            return e.value
