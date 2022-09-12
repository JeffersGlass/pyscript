import asyncio
from contextlib import suppress

from js import console as jsconsole


def log_loops(*args):
    for t in asyncio.all_tasks():
        jsconsole.log(str(type(t)))


async def cancel_tasks(*args):
    jsconsole.warn("Cancelling Async Tasks")
    for t in asyncio.all_tasks():
        jsconsole.log(f"Cancelling {t.get_name()}")
        with suppress(asyncio.exceptions.CancelledError):
            t.cancel()


async def countup():
    for x in range(50):
        await asyncio.sleep(1)
        print(x)


# Still error
asyncio.create_task(countup())
