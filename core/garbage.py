import os
import random

from core.helpers import _get_random_position, sleep
from core.settings import GARBAGE_FRAMES_DIR
from core import globals
from vendor.space_garbage import fly_garbage

async def fill_orbit_with_garbage(canvas):
    global coroutines
    while True:
        _, col = _get_random_position(canvas)

        with open(os.path.join(
                GARBAGE_FRAMES_DIR,
                random.choice(os.listdir(GARBAGE_FRAMES_DIR)))
        ) as fh:
            frame = fh.read()

        globals.coroutines.append(fly_garbage(canvas=canvas, column=col,garbage_frame=frame))
        await sleep(20)