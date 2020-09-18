import random
import asyncio

def _get_random_position(canvas):
    screen_height, screen_width = canvas.getmaxyx()
    return (
        random.randint(1, screen_height - 2),
        random.randint(1, screen_width - 2),
    )

async def sleep(tics=1):
    for i in range(tics):
        await asyncio.sleep(0)