## AsyncIO - Introduction

### What is AsyncIO

* `async IO` (Asynchronous IO): a language-agnostic paradigm (model) that has
  implementations across a host of programming languages

* `async/await`: two new Python keywords that are used to define coroutines

* `asyncio`: the Python package that provides a foundation and API for running
  and managing coroutines

[Source](https://realpython.com/async-io-python/)

### Background

#### C10K

[The C10K problem](http://www.kegel.com/c10k.html):

> It's time for web servers to handle ten thousand clients simultaneously

How can servers handle more then ten thousand requests simultaneously? In the
past two solutions where prominent:

* Multiprocessing - Requires a lot of memory, IPC required.
* Threading - Still requires some memory, Synchronization is difficult.

Clearly there must be another solution: “Asynchronous I/O”

> The term “Asynchronous I/O” is used to refer to [...] an execution model for
> network programming, where the scalability of an I/O bound application is
> governed by the number of open socket connections that can be handled in a
> single OS process rather than by the number of concurrent OS level threads.
> This approach can significantly improve the scalability of an application, as
> most POSIX based operating systems can effectively manage thousands or tens of
> thousands of open socket connections without any significant tuning of process
> options, but only hundreds of threads (with the default size of the C stack
> being a key culprit - consuming the resources of an entire thread to wait for
> an I/O operation can waste a whole lot of memory).

[Source](http://python-notes.curiousefficiency.org/en/latest/pep_ideas/async_programming.html#a-bit-of-background-info)

#### Parallelism vs. Concurrency

You can find this section in nearly all articles about `asyncio` and really it
is necessary to understand its foundations. This chapter will give you just a
short overview.

To get a deeper understanding the following links can be recommended:

*  [https://www.tedinski.com/2018/10/16/concurrency-vs-parallelism.html](https://www.tedinski.com/2018/10/16/concurrency-vs-parallelism.html)
*  [https://realpython.com/python-concurrency/](https://realpython.com/python-concurrency/)
*  [https://go.dev/blog/waza-talk](https://go.dev/blog/waza-talk)

What's concurrency? Some tasks are run concurrently. What's parallelism? Some
tasks are run in parallel. But isn't this the same? Not really. Parallelism is a
subset ob concurrency. A task can be suspended and another can be started. Both
tasks are still concurrent because they are not finished yet. In contrast two
parallel tasks are run at the same time. Speaking of CPUs a concurrent task runs
on a single CPU, is interrupted, paused and resumed. Parallel tasks are running
on different CPU cores.

So what are both best for. Parallel tasks are best for computing something and
the CPU is busy with calculations. For example with rendering a video.
Interrupting tasks or better task switching is good for situations where the CPU
has to wait for something. When the CPU has to wait for some event to happen a
different work task can be executed. And when does this happen often? During
I/O. I/O devices like memory, disk, networks are a few times slower then the
CPU. While waiting for some data to be written or read it can execute some other
task.

| Name | Python Standard Library | Concurrency Type | Memory Consumption | CPUs | Best For |
|------|-------------------------|------------------|--------------------|------|----------|
| Processes | `multiprocessing` | Multiprocessing | High | many | CPU bound |
| Threads | `threading` | preemptive multitasking | Medium | 1 (because of the GIL) | I/O bound |
| AsyncIO | `asyncio` | cooperative multitasking | Low | 1 | I/O bound |

