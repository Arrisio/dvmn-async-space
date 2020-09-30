import os
import random

from src import globals
from src import settings
from src.helpers import _get_random_position, sleep
from src.settings import GARBAGE_FRAMES_DIR
from vendor.curses_tools import draw_frame, get_frame_size
from vendor.obstacles import Obstacle
from vendor.explosion import explode
from vendor.game_scenario import get_garbage_delay_tics


class Garbage(Obstacle):
    _destroyed = False

    def __init__(self, canvas, frame, speed=0.5):
        self.canvas = canvas
        self.frame = frame
        self.speed = speed

        self.rows_number, columns_number = canvas.getmaxyx()
        _, column = _get_random_position(canvas)
        column = max(column, 0)
        column = min(column, columns_number - 1)
        row = 0

        super(Garbage, self).__init__(row, column, *get_frame_size(frame))

    async def draw(self):
        while self.row < self.rows_number - 1:
            if self._destroyed:
                return

            draw_frame(self.canvas, self.row, self.column, self.frame)
            if settings.SHOW_OBSTACLE_BORDERS:
                draw_frame(
                    self.canvas, self.row, self.column, self.get_bounding_box_frame()
                )

            await sleep()

            draw_frame(self.canvas, self.row, self.column, self.frame, negative=True)
            if settings.SHOW_OBSTACLE_BORDERS:
                draw_frame(
                    self.canvas,
                    self.row,
                    self.column,
                    self.get_bounding_box_frame(),
                    negative=True,
                )

            self.row += self.speed

    def register(self):
        globals.obstacles.append(self)
        globals.coroutines.append(self.draw())

    def destroy(self):
        self._destroyed = True
        globals.obstacles.remove(self)
        globals.coroutines.append(
            explode(
                self.canvas,
                center_row=self.row + self.rows_size // 2,
                center_column=self.column + self.columns_size // 2,
            )
        )


def get_collided_obstacles(
    obj_corner_row, obj_corner_column, obj_size_rows=1, obj_size_columns=1
):
    return [
        obst
        for obst in globals.obstacles
        if obst.has_collision(
            obj_corner_row, obj_corner_column, obj_size_rows, obj_size_columns
        )
    ]


def has_collision_with_any_obstacle(
    obj_corner_row, obj_corner_column, obj_size_rows=1, obj_size_columns=1
):
    collided_obstacles = get_collided_obstacles(
        obj_corner_row, obj_corner_column, obj_size_rows, obj_size_columns
    )
    return len(collided_obstacles) > 0


def destroy_collided_obstacles(
    obj_corner_row, obj_corner_column, obj_size_rows=1, obj_size_columns=1
):
    for obstacle in get_collided_obstacles(
        obj_corner_row, obj_corner_column, obj_size_rows, obj_size_columns
    ):
        obstacle.destroy()


async def fill_orbit_with_garbage(canvas):
    while True:
        _, col = _get_random_position(canvas)

        if delay_tics := get_garbage_delay_tics(globals.year):
            random_frame_file = random.choice(os.listdir(GARBAGE_FRAMES_DIR))
            with open(os.path.join(GARBAGE_FRAMES_DIR, random_frame_file)) as fh:
                frame = fh.read()

            garbage = Garbage(frame=frame, canvas=canvas)
            garbage.register()

        await sleep(delay_tics or 1)
