from itertools import cycle
from vendor.curses_tools import read_controls, draw_frame, get_frame_size
from vendor.physics import update_speed
from vendor.explosion import explode
from src.helpers import sleep
from src.fire_animation import fire
from src.space_garbage import has_collision_with_any_obstacle
from src import globals, settings


def get_top_positions(canvas, object_width, object_height):
    max_rows, max_columns = canvas.getmaxyx()

    top_left_position = 1
    top_right_position = max_columns - object_width - 1
    top_up_position = 1
    top_bottom_position = max_rows - object_height - 1

    return top_left_position, top_right_position, top_up_position, top_bottom_position


class RocketController:
    # двигаться по горизонтали быстрее , чтоб было комфортнее
    horizontal_movement_booster = 2

    space_pressed = False
    row_speed = 0
    column_speed = 0

    def __init__(self, canvas, frames, start_row: int = None, start_column: int = None):
        self.canvas = canvas
        self.width = max(get_frame_size(frame)[1] for frame in frames)
        self.height = max(get_frame_size(frame)[0] for frame in frames)

        (
            self.top_left_position,
            self.top_right_position,
            self.top_up_position,
            self.top_bottom_position,
        ) = get_top_positions(canvas, self.width, self.height)

        self.row = start_row or canvas.getmaxyx()[0] // 2
        self.column = start_column or canvas.getmaxyx()[1] // 2

    def update(self):
        rows_direction, columns_direction, space_pressed = read_controls(self.canvas)
        row_speed, column_speed = update_speed(
            row_speed=self.row_speed,
            column_speed=self.column_speed,
            rows_direction=rows_direction,
            columns_direction=columns_direction,
        )

        self.column, self.column_speed = self.get_new_position_and_speed(
            self.column,
            column_speed,
            self.top_left_position,
            self.top_right_position,
            self.horizontal_movement_booster,
        )

        self.row, self.row_speed = self.get_new_position_and_speed(
            self.row, row_speed, self.top_up_position, self.top_bottom_position
        )

    def get_new_position_and_speed(
        _, current_position, speed, top_min, top_max, booster=1
    ):
        position_wanted = current_position + speed * booster
        if position_wanted <= top_min:
            return top_min, 0
        elif position_wanted >= top_max:
            return top_max, 0
        else:
            return position_wanted, speed


class RocketCollidedException(Exception):
    pass


class Rocket:
    def __init__(self, canvas, start_row: int = None, start_column: int = None):
        self._canvas = canvas

        self._load_rocket_frames()
        self.controller = RocketController(canvas, self.frames, start_row, start_column)

    async def draw(self):
        for current_frame in cycle(self.frames):
            if has_collision_with_any_obstacle(
                obj_corner_column=self.controller.column,
                obj_corner_row=self.controller.row,
                obj_size_rows=self.controller.height,
            ):
                globals.coroutines.append(
                    explode(
                        canvas=self._canvas,
                        center_row=self.controller.row + self.controller.width // 2,
                        center_column=self.controller.column
                        + self.controller.height // 2,
                    )
                )
                raise RocketCollidedException

            self.controller.update()

            draw_frame(
                canvas=self._canvas,
                start_row=self.controller.row,
                start_column=self.controller.column,
                text=current_frame,
            )
            if (
                self.controller.space_pressed
                and globals.year >= settings.CANNON_AVALIABLE_YEAR
            ):
                globals.coroutines.append(
                    fire(
                        canvas=self._canvas,
                        start_column=self.column + 2,
                        start_row=self.row,
                    )
                )
            await sleep()

            draw_frame(
                canvas=self._canvas,
                start_row=self.controller.row,
                start_column=self.controller.column,
                text=current_frame,
                negative=True,
            )

    def _load_rocket_frames(self) -> None:
        self.frames = []
        frames_paths = ["content/rocket_frame_1.txt", "content/rocket_frame_2.txt"]
        for paths in frames_paths:
            with open(paths) as fh:
                self.frames.append(fh.read())

    async def draw_speed(self):

        while True:
            draw_frame(
                canvas=self._canvas,
                start_row=self.controller.top_up_position,
                start_column=self.controller.top_right_position - 8,
                text=f"row_spd {self.controller.row_speed:.2f}\ncol_spd {self.controller.column_speed:.2f}",
            )
            await sleep()
