from typing import Final, NamedTuple

import cv2
import numpy as np

from my_module.K24132.lecture05_camera_image_capture import MyVideoCapture


class Shape(NamedTuple):
    height: int
    width: int
    channels: int


class BGR(NamedTuple):
    blue: int
    green: int
    red: int


def lecture05_01() -> None:
    app = MyVideoCapture()
    app.run()

    frame: np.ndarray | None = app.get_img()

    if frame is None:
        raise ValueError("カメラから画像を取得できませんでした。")

    google_img = cv2.imread("images/google.png")
    if google_img is None:
        raise ValueError("Googleロゴ画像を読み込めませんでした。パスを確認してください。")

    g = Shape(*google_img.shape)
    c = Shape(*frame.shape)

    # NOTE: ローテーションする等差数列を作成
    # [0, 1, 2, ..., c_height-1, 0, 1, 2, ...]
    y_indices = np.arange(g.height) % c.height
    x_indices = np.arange(g.width) % c.width

    white: Final = BGR(255, 255, 255)

    for x in range(g.width):
        for y in range(g.height):
            color = BGR(*google_img[y, x])
            if color == white:
                google_img[y, x] = frame[y_indices[y], x_indices[x]]

    cv2.imwrite("output_images/lecture05_01_output.png", google_img)
