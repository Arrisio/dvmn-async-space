from src import globals, settings
from vendor.curses_tools import draw_frame
from vendor.game_scenario import PHRASES
from src.helpers import sleep


async def show_fire_msg(canvas):
    text = "Press SPACE to fire"
    while True:
        if globals.year >= settings.CANNON_AVALIABLE_YEAR:
            draw_frame(canvas, 1, 1,text)
            canvas.syncup()

            # чтобы скорость мигания постепенно замедлялась
            show_text_deley =round((globals.year-settings.CANNON_AVALIABLE_YEAR)**1/2)*2

            await sleep(show_text_deley)
            draw_frame(canvas, 1, 1, text, negative=True)
            canvas.syncup()

        await sleep(2)


async def show_year(canvas):
    while True:
        draw_frame(canvas, 2, 1, f"Year: {str(globals.year)}")
        if phrase := PHRASES.get(globals.year):
            draw_frame(canvas, 3, 1, phrase)
        else:
            draw_frame(canvas, 3, 1, '-'*len(max(PHRASES.values())), negative=True)

        canvas.syncup()
        await sleep()
