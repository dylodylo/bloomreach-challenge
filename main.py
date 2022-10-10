import asyncio

import aiohttp
from fastapi import FastAPI, HTTPException

app = FastAPI()
URL = 'https://exponea-engineering-assignment.appspot.com/api/work'


async def request(session, sleep=None):
    if sleep:
        asyncio.sleep(sleep)
    async with session.get(URL) as response:
        if response.status == 200:
            return await response.json()
        else:
            raise ValueError('Expected 200 in status code')


async def task():
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(request(session, sleep=0.3)) for i in range(2)]
        tasks.insert(0, asyncio.create_task(request(session)))
        finished, _ = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        # TODO: handle with error in request (run again wait with pending) and close pending tasks
        session.close()
        return finished.pop().result()


@app.get('/api/smart')
async def root(timeout: int):
    timeout_in_milliseconds = timeout/1000
    try:
        result = await asyncio.wait_for(task(), timeout=timeout_in_milliseconds)
        return result
    except asyncio.TimeoutError:
        raise HTTPException(status_code=408, detail='Timeout error')
