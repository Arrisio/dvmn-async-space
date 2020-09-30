import os

TIC_TIMEOUT = 0.1

STARS_NUMBER = 50
MAX_TIKS_TO_BLINK_STAR = 10  # in ticks

GARBAGE_FRAMES_DIR = os.path.join("content", "trash_frames")
GAME_OVER_FRAME = os.path.join("content", "game_over.txt")

SHOW_OBSTACLE_BORDERS = False
SHOW_ROCKET_SPEED = False


# year
START_GAME_YEAR: int = 1957
UPDATE_YEAR_TICS = 20

# fire
# CANNON_AVALIABLE_YEAR = 2001
CANNON_AVALIABLE_YEAR = 1959

#info panel
INFOPANEL_WIDTH=44
INFOPANEL_HEIGHT=5
INFOPANEL_LEFT_INDENT=5
INFOPANEL_BOTTOM_INDENT=3