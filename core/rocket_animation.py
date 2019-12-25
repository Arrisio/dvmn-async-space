import asyncio
import time
from core.curses_tools import read_controls, draw_frame, get_frame_size

TIC_TIMEOUT = 0.01


class RocketAnimation:
    def __init__(self, canvas, start_row: int = None, start_column: int = None):
        self._canvas = canvas
        self.row = start_row or canvas.getmaxyx()[0] // 2
        self.column = start_column or canvas.getmaxyx()[1] // 2

        self._load_rocket_frames()
        self._init_top_positions()
        self._frame_swither = self._init_frame_switcher()
        # self._frame_swither.send(None)

    async def draw(self):
        while True:
            self._frame_swither.send(None)
            self._set_new_rocket_position()
            draw_frame(
                canvas=self._canvas,
                start_row=self.row,
                start_column=self.column,
                text=self.current_frame,
            )

            time.sleep(TIC_TIMEOUT)

            await asyncio.sleep(1)
            draw_frame(
                canvas=self._canvas,
                start_row=self.row,
                start_column=self.column,
                text=self.current_frame,
                negative=True,
            )

            await asyncio.sleep(0)

    async def clear(self):
        while True:
            draw_frame(
                canvas=self._canvas,
                start_row=self.row,
                start_column=self.column,
                text=self.current_frame,
                negative=True,
            )
            await asyncio.sleep(0)

    def _load_rocket_frames(self) -> None:
        self.frames = []
        frames_paths = ["content/rocket_frame_1.txt", "content/rocket_frame_2.txt"]
        for paths in frames_paths:
            with open(paths) as fh:
                self.frames.append(fh.read())

    def _init_top_positions(self):
        max_rows, max_columns = self._canvas.getmaxyx()

        max_frame_width = max(get_frame_size(frame)[1] for frame in self.frames)
        max_frame_height = max(get_frame_size(frame)[0] for frame in self.frames)

        self.top_left_position = 1
        self.top_right_position = max_columns - max_frame_width - 1
        self.top_up_position = 1
        self.top_bottom_position = max_rows - max_frame_height - 1

    def _set_new_rocket_position(self):
        rows_direction, columns_direction, _ = read_controls(self._canvas)

        new_row_wanted = self.row + rows_direction
        if new_row_wanted <= self.top_up_position:
            self.row = self.top_up_position
        elif new_row_wanted >= self.top_bottom_position:
            self.row = self.top_bottom_position
        else:
            self.row = new_row_wanted

        new_column_wanted = self.column + columns_direction
        if new_column_wanted <= self.top_left_position:
            self.column = self.top_left_position
        elif new_column_wanted >= self.top_right_position:
            self.column = self.top_right_position
        else:
            self.column = new_column_wanted

    async def _init_frame_switcher(self):
        while True:
            for frame in self.frames:
                self.current_frame = frame
                await asyncio.sleep(0)
