from future import Future


def wait(*tasks):
    waiter = Future(f"Waiter for {', '.join([str(t) for t in tasks])}")
    counter = len(tasks)

    def _on_completion(_future):
        nonlocal counter
        counter -= 1
        if counter <= 0:
            # all results are available let's wakeup
            waiter.set_result(None)

    for task in tasks:
        task.add_done_callback(_on_completion)

    yield from waiter

    return [t.result() for t in tasks]
