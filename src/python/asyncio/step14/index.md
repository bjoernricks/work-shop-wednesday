### Step 14 - And what about real Async IO?

Until now why didn't handle real Asynchronous IO like reading and writing from
and to network sockets. Because this topic heavily depends on the used operating
system and loop implementation it is handled here only schematically for a Linux
based system.

```{literalinclude} step14.py
:language: python
```

The idea is to have a `Selector` API that does `select` calls on sockets
internally. If no data is available the `select` calls do block the current
thread (and therefore our loop) until data is available. Otherwise the
`Selector` API returns the corresponding `Handler` for sockets with available
data. The `Selector` API is called at every step/tick before the `Handler`s are
run to schedule the socket `Handler`s for this step.

To allow the `Loop` to track all socket communication the creation of the socket
must originate in the `Loop`. In our case it is done via the `create_connection`
method. This allows for pairing a `Future` with a socket in a `Handler`.


```{admonition} Summary
* All I/O must originate in our `Loop`.
* The `Loop` provides methods for creating network connections.
* The `Loop` tracks the network connections and notifies waiting `Future`s.
```
