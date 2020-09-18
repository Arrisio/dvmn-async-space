import time
import curses

from core import globals
from core.garbage import fill_orbit_with_garbage
from core.settings import STARS_NAMBER, TIC_TIMEOUT
from core.rocket_animation import RocketAnimation
from core.star import  Star


def draw(canvas):
    canvas.border()
    canvas.nodelay(True)
    curses.curs_set(False)

    globals.coroutines = ([
        Star(canvas).blink()
        for _ in range(STARS_NAMBER)
    ])
    globals.coroutines.append(RocketAnimation(canvas).draw())
    globals.coroutines.append(fill_orbit_with_garbage(canvas))

    while True:
        for coroutine in globals.coroutines[:]:
            try:
                coroutine.send(None)
            except StopIteration:
                globals.coroutines.remove(coroutine)

        canvas.refresh()
        time.sleep(TIC_TIMEOUT)


def run():
    curses.update_lines_cols()
    curses.wrapper(draw)


if __name__ == "__main__":
    run()
