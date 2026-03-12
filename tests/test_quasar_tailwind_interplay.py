from pathlib import Path

import numpy as np
from PIL import Image

from nicegui import ui
from nicegui.testing.screen import Screen


def test_rotate(screen: Screen, tmp_path: Path) -> None:
    @ui.page('/')
    def main():
        ui.icon('sym_o_wifi_1_bar').classes('rotate-90')

    screen.open('/')
    screen.find_by_tag('i').screenshot(str(tmp_path / 'icon.png'))
    img = np.array(Image.open(tmp_path / 'icon.png').convert('L'))
    left_black = (img[:, :img.shape[1] // 2] < 128).sum()
    right_black = (img[:, img.shape[1] // 2:] < 128).sum()
    assert left_black > 2 * right_black, 'the left should have significantly more black pixels than the right'
