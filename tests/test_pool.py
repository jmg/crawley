"""Tests for the asyncio AsyncPool."""

import asyncio

import pytest

from crawley.multiprogramming.pool import AsyncPool


def test_invalid_size():
    with pytest.raises(ValueError):
        AsyncPool(0)


async def test_spawn_and_join_collects_results():
    pool = AsyncPool(10)
    seen = []

    async def work(n):
        await asyncio.sleep(0)
        seen.append(n)

    for i in range(20):
        pool.spawn(work(i))
    await pool.join()

    assert sorted(seen) == list(range(20))


async def test_recursive_spawn():
    pool = AsyncPool(5)
    counter = {"n": 0}

    async def work(depth):
        counter["n"] += 1
        if depth > 0:
            pool.spawn(work(depth - 1))
            pool.spawn(work(depth - 1))

    pool.spawn(work(3))
    await pool.join()

    # 1 + 2 + 4 + 8 = 15 nodes in a binary tree of depth 3
    assert counter["n"] == 15


async def test_concurrency_is_bounded():
    pool = AsyncPool(3)
    state = {"current": 0, "max": 0}

    async def work():
        state["current"] += 1
        state["max"] = max(state["max"], state["current"])
        await asyncio.sleep(0.01)
        state["current"] -= 1

    for _ in range(15):
        pool.spawn(work())
    await pool.join()

    assert state["max"] <= 3


async def test_spawn_n_alias():
    pool = AsyncPool(2)
    seen = []

    async def work(a, b):
        seen.append((a, b))

    pool.spawn_n(work, 1, 2)
    await pool.join()
    assert seen == [(1, 2)]
