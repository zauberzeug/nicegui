from pathlib import Path

from PIL import Image

from nicegui import ui
from nicegui.testing.screen import Screen


def test_rotate(screen: Screen, tmp_path: Path) -> None:
    @ui.page('/')
    def main():
        ui.icon('sym_o_wifi_1_bar').classes('rotate-90').props('size="64px"')

    screen.open('/')
    screen.find_by_tag('i').screenshot(str(tmp_path / 'icon.png'))

    # check that the PNG has significantly more black pixels on the left than on the right
    img = Image.open(tmp_path / 'icon.png').convert('L')
    width, height = img.size
    left_half = img.crop((0, 0, width // 2, height))
    right_half = img.crop((width // 2, 0, width, height))

    def sum_black_pixels(image: Image.Image) -> int:
        total = 0
        for pixel in image.getdata():  # type: ignore
            if pixel < 128:
                total += 1
        return total

    assert ((sum_black_pixels(left_half)+1) / (sum_black_pixels(right_half)+1) > 2)
