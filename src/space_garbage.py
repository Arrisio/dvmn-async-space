import os
import random

from src import globals
from src.helpers import get_random_position, sleep
from src.settings import GARBAGE_FRAMES_DIR
from vendor.curses_tools import draw_frame, get_frame_size
from vendor.obstacles import Obstacle
from vendor.explosion import explode
from vendor.game_scenario import get_garbage_delay_tics


class Garbage:
    def __init__(self, canvas, frame, speed=0.5):
        self.canvas = canvas
        self.frame = frame
        self.speed = speed

        self.rows_number, columns_number = canvas.getmaxyx()
        _, column = get_random_position(canvas)
        column = max(column, 0)
        column = min(column, columns_number - 1)
        row = 0

        self.obstacle = Obstacle(row, column, *get_frame_size(frame))


    async def draw(self):
        while self.obstacle.row < self.rows_number - 1:
            if self.obstacle not  in globals.obstacles:
                return

            draw_frame(self.canvas, self.obstacle.row, self.obstacle.column, self.frame)

            await sleep()

            draw_frame(self.canvas, self.obstacle.row, self.obstacle.column, self.frame, negative=True)

            self.obstacle.row += self.speed

        globals.obstacles.remove(self.obstacle)

    def register(self):
        globals.obstacles.append(self.obstacle)
        globals.coroutines.append(self.draw())


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


def destroy_obstacles(canvas, collided_obstacles):
    for obstacle in collided_obstacles:
        globals.obstacles.remove(obstacle)
        globals.coroutines.append(
            explode(
                canvas,
                center_row=obstacle.row + obstacle.rows_size // 2,
                center_column=obstacle.column + obstacle.columns_size // 2,
            )
        )


async def fill_orbit_with_garbage(canvas):
    while True:
        _, col = get_random_position(canvas)

        if delay_tics := get_garbage_delay_tics(globals.year):
            random_frame_file = random.choice(os.listdir(GARBAGE_FRAMES_DIR))
            with open(os.path.join(GARBAGE_FRAMES_DIR, random_frame_file)) as fh:
                frame = fh.read()

            garbage = Garbage(frame=frame, canvas=canvas)
            garbage.register()

        await sleep(delay_tics or 1)
