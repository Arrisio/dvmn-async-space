import time
import asyncio
import curses
import random

from core.fire_animation import fire
from core.rocket_animation import RocketAnimation

STARS_NAMBER = 50
MAX_TIKS_TO_BLINK = 10  # in ticks
TIC_TIMEOUT = .1

async def blink(canvas, row, column, symbol="*", tiks_to_blink=10):
    blink_sequence = [curses.A_BOLD, curses.A_NORMAL, curses.A_DIM]
    while True:
        for blink_type in blink_sequence:
            canvas.addstr(row, column, symbol, blink_type)
            for _ in range(tiks_to_blink):
                await asyncio.sleep(0)


def draw(canvas):
    canvas.border()
    canvas.nodelay(True)
    curses.curs_set(False)

    def _get_random_position(canvas=canvas):
        screen_height, screen_width = canvas.getmaxyx()
        return (
            random.randint(1, screen_height - 2),
            random.randint(1, screen_width - 2),
        )

    def _init_star(blink_period, canvas=canvas):
        row, column = _get_random_position()
        return blink(
            canvas,
            row,
            column,
            symbol=random.choice("+*.:"),
            tiks_to_blink=blink_period,
        )

    stars = [
        _init_star(blink_period=random.randint(1, MAX_TIKS_TO_BLINK))
        for _ in range(STARS_NAMBER)
    ]

    shots = [
        fire(canvas, *_get_random_position()),
        fire(canvas, *_get_random_position()),
    ]

    rocket_animation = RocketAnimation(canvas)

    coroutines = stars + shots + [rocket_animation.draw()]

    while True:
        for coroutine in coroutines[:]:
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)

        canvas.refresh()
        time.sleep(TIC_TIMEOUT)


def run():
    curses.update_lines_cols()
    curses.wrapper(draw)


if __name__ == "__main__":
    run()
