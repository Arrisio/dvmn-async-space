import os
import random

from core import globals
from core.helpers import _get_random_position, sleep
from core.settings import GARBAGE_FRAMES_DIR
from vendor.curses_tools import draw_frame

import asyncio

from vendor.obstacles import Obstacle


async def fly_garbage(canvas, column, garbage_frame, speed=0.5):
    """Animate garbage, flying from top to bottom. Сolumn position will stay same, as specified on start."""
    rows_number, columns_number = canvas.getmaxyx()

    column = max(column, 0)
    column = min(column, columns_number - 1)

    row = 0

    while row < rows_number - 1:
        draw_frame(canvas, row, column, garbage_frame)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, garbage_frame, negative=True)
        row += speed


async def fill_orbit_with_garbage(canvas):
    global coroutines
    while True:
        _, col = _get_random_position(canvas)

        with open(
            os.path.join(
                GARBAGE_FRAMES_DIR, random.choice(os.listdir(GARBAGE_FRAMES_DIR))
            )
        ) as fh:
            frame = fh.read()

        globals.coroutines.append(
            fly_garbage(canvas=canvas, column=col, garbage_frame=frame)
        )
        globals.obstacles.append(
            Obstacle(row=)
        )
        await sleep(20)