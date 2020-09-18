import time
import curses

from vendor.obstacles import show_obstacles

from core import globals
from core.space_garbage import fill_orbit_with_garbage
from core.settings import STARS_NAMBER, TIC_TIMEOUT
from core.rocket_animation import RocketAnimation
from core.star import  Star

# from vendor.fire_animation import fire
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
        # globals.coroutines.append( fire(canvas=canvas, start_column=20, start_row=20 ))
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
