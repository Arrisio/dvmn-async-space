import asyncio
import curses
import random
from core.helpers import _get_random_position, sleep
from core.settings import MAX_TIKS_TO_BLINK

class Star:
    blink_sequence = [curses.A_BOLD, curses.A_NORMAL, curses.A_DIM]

    def __init__(self, canvas ):
        self.canvas = canvas
        self.row, self.column =_get_random_position(canvas)
        self.blink_period = random.randint(1,MAX_TIKS_TO_BLINK)
        self.symbol = random.choice("+*.:")

    async def blink(self):
        while True:
            for blink_type in self.blink_sequence:
                self.canvas.addstr(self.row, self.column, self.symbol, blink_type)
                await sleep(self.blink_period)