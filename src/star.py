import curses
import random
from src.helpers import sleep
from src import settings


async def star_blink(canvas, row, column, blink_period):
    blink_sequence = [curses.A_BOLD, curses.A_NORMAL, curses.A_DIM]
    symbol = random.choice(settings.STAR_SYMBOLS)

    while True:
        for blink_type in blink_sequence:
            canvas.addstr(row, column, symbol, blink_type)
            await sleep(blink_period)