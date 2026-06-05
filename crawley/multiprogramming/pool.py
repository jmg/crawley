"""Concurrency primitives built on top of :mod:`asyncio`.

The legacy framework relied on ``eventlet`` green pools. The modern core is
fully asynchronous, so concurrency is expressed with asyncio tasks bounded by
a semaphore.
"""

import asyncio


class AsyncPool:
    """A bounded pool of asyncio tasks.

    ``spawn`` schedules a coroutine to run as soon as a slot is available
    (limited by *size*). Coroutines may themselves call ``spawn`` to enqueue
    more work; ``join`` waits until every scheduled task -- including the ones
    spawned recursively -- has finished.
    """

    def __init__(self, size):
        if size < 1:
            raise ValueError("AsyncPool must allow at least 1 concurrent task")
        self.size = size
        self._semaphore = asyncio.Semaphore(size)
        self._tasks = set()

    def spawn(self, coro):
        """Schedule *coro* for execution and return the created task."""
        task = asyncio.ensure_future(self._run(coro))
        self._tasks.add(task)
        task.add_done_callback(self._tasks.discard)
        return task

    # Backwards compatible alias with the old eventlet based API.
    def spawn_n(self, func, *args, **kwargs):
        """Schedule ``func(*args, **kwargs)`` where *func* returns a coroutine."""
        return self.spawn(func(*args, **kwargs))

    async def _run(self, coro):
        async with self._semaphore:
            return await coro

    async def join(self):
        """Wait until all scheduled tasks (and their children) complete."""
        while self._tasks:
            await asyncio.gather(*list(self._tasks), return_exceptions=True)

    # Backwards compatible alias.
    async def waitall(self):
        await self.join()
