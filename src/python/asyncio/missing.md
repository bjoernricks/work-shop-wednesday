#### What's missing?

* Timeouts
* Error Handling
* Signal Handling
* Queues
* Locks and Semaphores
* Running *operations* in [another Thread](https://docs.python.org/3/library/asyncio-dev.html#concurrency-and-multithreading) to not block the main thread
* Running [subprocesses](https://docs.python.org/3.10/library/asyncio-subprocess.htm)
* "Edge Cases"
  * Avoid cyclic references for Garbage Collection
  * Checking if passed coroutine arguments are coroutines
  * Optimized `collections.deque` instead of `list` for FIFO
* Networking and Interprocess Communication Details
  * [Streams](https://docs.python.org/3.10/library/asyncio-stream.html#asyncio-streams)
  * [Transports/Protocols](https://docs.python.org/3.10/library/asyncio-protocol.html)
* [Policies](https://docs.python.org/3.10/library/asyncio-policy.html) for providing different loop implementations
  * [uvloop](https://uvloop.readthedocs.io/user/index.html#using-uvloop) and alternative fast event loop
