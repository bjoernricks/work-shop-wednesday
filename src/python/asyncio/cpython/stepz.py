from future import Future
from loop import Loop
from task import Task


async def some_result(result):
    future = Future("Some Result")
    future.set_result(result)
    return await future


async def add(coroutine1, coroutine2):
    task1 = Task(coroutine1, "Add X")
    task2 = Task(coroutine2, "Add Y")
    x = await task1
    y = await task2
    return x + y


async def main():
    return await add(some_result(1), some_result(2))


loop = Loop.get_current_loop()
result = loop.run(main())
print("Loop finished with result", result)
