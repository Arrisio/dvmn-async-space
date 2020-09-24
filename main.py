import time
import curses
import asyncio

from src import globals, settings
from src.space_garbage import fill_orbit_with_garbage
from src.settings import STARS_NAMBER, TIC_TIMEOUT
from src.rocket import Rocket, RocketCollidedException
from src.star import Star
from src.messages import show_year, show_fire_msg

from vendor.curses_tools import draw_frame, get_frame_size
from src.helpers import sleep


async def update_year():
    while True:
        globals.year += 1
        await sleep(settings.UPDATE_YEAR_TICS)


async def game_over(canvas):
    with open(settings.GAME_OVER_FRAME) as fh:
        game_over_text = fh.read()

    text_height, text_width = get_frame_size(game_over_text)
    screen_height, screen_width = canvas.getmaxyx()


    while True:
        draw_frame(
            canvas=canvas,
            start_row=screen_height // 2 - text_height // 2,
            start_column=screen_width // 2 - text_width // 2,
            text=game_over_text,
        )
        # await asyncio.sleep(0)
        await sleep()


def draw(canvas):
    canvas.border()
    canvas.nodelay(True)
    curses.curs_set(False)

    globals.coroutines = [Star(canvas).blink() for _ in range(STARS_NAMBER)]
    globals.coroutines.append(Rocket(canvas).draw())
    globals.coroutines.append(fill_orbit_with_garbage(canvas))


    information_panel = canvas.derwin(5, 30, canvas.getmaxyx()[0]-7, 3 )
    globals.coroutines.append(update_year())
    globals.coroutines.append(show_year(information_panel))
    globals.coroutines.append(show_fire_msg(information_panel))
    # canvas.syncup()

    while True:
        # globals.coroutines.append( fire(canvas=canvas, start_column=20, start_row=20 ))
        for coroutine in globals.coroutines[:]:
            try:
                coroutine.send(None)
            except StopIteration:
                globals.coroutines.remove(coroutine)
            except RocketCollidedException:
                globals.coroutines.remove(coroutine)
                globals.coroutines.append(game_over(canvas))

        canvas.refresh()
        time.sleep(TIC_TIMEOUT)


def run():
    curses.update_lines_cols()
    curses.wrapper(draw)


if __name__ == "__main__":
    run()


