### Examples using asyncio

[Waiting in asyncio](https://hynek.me/articles/waiting-in-asyncio/) has a very
good overview about which wait function to use when and explains all
differences.

#### Mastodon

Using the [Mastodon API](https://docs.joinmastodon.org/client/public/) with
asyncio and [httpx](https://www.python-httpx.org).

```{literalinclude} example_1.py
:language: python
:caption: Example 1 - Mastodon
```
