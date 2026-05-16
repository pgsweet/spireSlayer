from pathlib import Path
from capture import ScreenCapture, WindowNotFoundError
import time


GAME_WINDOW_TITLE = "Slay the Spire 2"
SCREENSHOT_PATH = Path("screen.png")


def main():
    screen_capture = ScreenCapture(window_title=GAME_WINDOW_TITLE)

    try:
        time.sleep(5)
        image = screen_capture.get_image()
    except WindowNotFoundError as error:
        print(error)
        return

    image.save(SCREENSHOT_PATH)

    print(f'Saved "{GAME_WINDOW_TITLE}" screenshot to {SCREENSHOT_PATH.resolve()}')


if __name__ == "__main__":
    main()
