import time
import curses
import random

from src import globals, settings
from src.space_garbage import fill_orbit_with_garbage
from src.rocket import Rocket, RocketCollidedException
from src.star import star_blink
from src.messages import show_year, show_fire_msg

from vendor.curses_tools import draw_frame, get_frame_size
from src.helpers import sleep, get_random_position


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
        await sleep()


def draw(canvas):
    canvas.border()
    canvas.nodelay(True)
    curses.curs_set(False)

    globals.coroutines = [
        star_blink(
            canvas,
            *get_random_position(canvas),
            blink_period=random.randint(1, settings.MAX_TIKS_TO_BLINK_STAR)
        )
        for _ in range(settings.STARS_NUMBER)
    ]
    rocket = Rocket(canvas)
    globals.coroutines.append(rocket.draw())
    globals.coroutines.append(fill_orbit_with_garbage(canvas))

    info_panel = canvas.derwin(
        settings.INFOPANEL_HEIGHT,
        settings.INFOPANEL_WIDTH,
        canvas.getmaxyx()[0]
        - settings.INFOPANEL_HEIGHT
        - settings.INFOPANEL_BOTTOM_INDENT,
        settings.INFOPANEL_LEFT_INDENT,
    )
    globals.coroutines.append(update_year())
    globals.coroutines.append(show_year(info_panel))
    globals.coroutines.append(show_fire_msg(info_panel))
    if settings.SHOW_ROCKET_SPEED:
        globals.coroutines.append(rocket.draw_speed())

    while True:
        for coroutine in globals.coroutines[:]:
            try:
                coroutine.send(None)
            except StopIteration:
                globals.coroutines.remove(coroutine)
            except RocketCollidedException:
                globals.coroutines.remove(coroutine)
                globals.coroutines.append(game_over(canvas))

        canvas.refresh()
        time.sleep(settings.TIC_TIMEOUT)


def run():
    curses.update_lines_cols()
    curses.wrapper(draw)


if __name__ == "__main__":
    run()
