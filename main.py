import aiohttp
import asyncio

from fastapi import FastAPI

app = FastAPI()
URL = 'https://exponea-engineering-assignment.appspot.com/api/work'


async def request(session):
    async with session.get(URL) as response:
        return await response.json()

async def request_after_fail(session):
    asyncio.sleep(0.3)
    async with session.get(URL) as response:
        return await response.json()


async def task():
    async with aiohttp.ClientSession() as session:
        tasks = [request_after_fail(session) for i in range(2)]
        tasks.insert(0, request(session))
        finished, _ = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        session.close()
        return finished.pop().result()


@app.get("/api/smart")
async def root():
    return await task()

