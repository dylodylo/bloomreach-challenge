import asyncio

import aiohttp
from fastapi import FastAPI, HTTPException

app = FastAPI()
URL = 'https://exponea-engineering-assignment.appspot.com/api/work'


async def request(session, sleep=None):
    if sleep:
        await asyncio.sleep(sleep)
    async with session.get(URL) as response:
        if response.status == 200:
            return await response.json()
        else:
            raise ValueError('Expected 200 in status code')


async def close_pending(pending):
    for task in pending:
        task.cancel()


async def exponea_session():
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(request(session, sleep=0.3)) for _ in range(2)]
        tasks.insert(0, asyncio.create_task(request(session)))
        done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        while done:
            task = done.pop()
            try:
                result = task.result()
                break
            except AttributeError:
                pass
            except ValueError:
                if not pending:
                    result = HTTPException(status_code=503)
                    break
            if pending:
                done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)

        await close_pending(pending)
        await session.close()
        return result


@app.get('/api/smart')
async def api_smart(timeout: int):
    timeout_in_milliseconds = timeout/1000
    try:
        result = await asyncio.wait_for(exponea_session(), timeout=timeout_in_milliseconds)
        return result
    except asyncio.TimeoutError:
        return HTTPException(status_code=408, detail='Timeout error')
