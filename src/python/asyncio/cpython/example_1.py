import asyncio
import json
import sys

import httpx

SERVERS = [
    "https://mastodon.social",
    "https://norden.social",
    "https://fosstodon.org",
    "https://floss.social",
    "https://osna.social",
]


async def get_public_feed(
    client: httpx.AsyncClient, server: str
) -> tuple[str, dict]:
    response = await client.get(f"{server}/api/v1/timelines/public")
    response.raise_for_status()
    return server, response.json()


async def get_trends(
    client: httpx.AsyncClient, server: str
) -> tuple[str, dict]:
    response = await client.get(f"{server}/api/v1/timelines/public")
    response.raise_for_status()
    return server, response.json()


async def main():
    servers = sys.argv[1:] if len(sys.argv) > 1 else SERVERS

    async with httpx.AsyncClient(
        http2=True, timeout=httpx.Timeout(20.0, connect=30.0)
    ) as client:

        trends_coros = [get_trends(client, server) for server in servers]
        for coro in asyncio.as_completed(trends_coros):
            server, data = await coro
            print(server, json.dumps(data, indent=2))

        # asyncio.wait expects tasks
        # passing coroutines prints a deprecation warning
        public_feed_tasks = [
            asyncio.create_task(get_public_feed(client, server))
            for server in servers
        ]
        done, pending = await asyncio.wait(public_feed_tasks, timeout=0.5)
        print(f"{len(done)} requests done, {len(pending)} request pending")
        for task in done:
            server, data = await task
            print(server, json.dumps(data, indent=2))

        if pending:
            done, pending = await asyncio.wait(pending)


asyncio.run(main())
