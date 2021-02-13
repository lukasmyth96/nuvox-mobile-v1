import math
from typing import Optional

import matplotlib; matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.animation
import matplotlib.image as mpimg
import numpy as np

from definition import KEYBOARD_IMAGE_PATH
from nuvox_algorithm.core import Swipe


def plot_swipe(swipe: Swipe):
    """Plots a single swipe over keyboard background image."""
    img = mpimg.imread(KEYBOARD_IMAGE_PATH)
    width = img.shape[0]
    height = img.shape[1]

    x = []
    y = []
    t = []
    for trace_point in swipe.trace:
        x.append(trace_point.x * width)
        y.append(trace_point.y * height)
        t.append(trace_point.t)

    plt.imshow(img[:, :, 0], cmap='hot')
    plt.scatter(x=x, y=y, c=t, cmap='Blues', s=10)
    plt.scatter(x=x[:1], y=y[:1], c='r', s=10)
    plt.title(f'"{swipe.target_text}" - device: {swipe.device_type}')
    plt.show()


def animate_swipe(swipe: Swipe, repeat: Optional[bool] = True):
    """Animates a single swipe over keyboard background image.

    Notes
    -------
    - You may need to run sudo apt-get install python3-tk for this to work!
    - In Pycharm this function does not seem to work via Python console.
    """

    interval_ms = 100  # time (ms) between each frame.
    required_frames = math.ceil((swipe.trace[-1].t * 1000) / interval_ms)

    img = mpimg.imread(KEYBOARD_IMAGE_PATH)
    width = img.shape[0]
    height = img.shape[1]

    fig, ax = plt.subplots()
    x, y = [], []
    ax.imshow(img[:, :, 0], cmap='hot')
    ax.set_title(f'Swipe for word: "{swipe.target_text}" on device: {swipe.device_type}')
    sc = ax.scatter(x, y, s=5)

    def animate(frame):
        current_time_secs = (frame * interval_ms) / 1000
        x = []
        y = []
        for trace_point in swipe.trace:
            if trace_point.t <= current_time_secs:
                x.append(trace_point.x * width)
                y.append(trace_point.y * height)
        sc.set_offsets(np.c_[x, y])

    ani = matplotlib.animation.FuncAnimation(fig=fig,
                                             func=animate,
                                             frames=required_frames,
                                             interval=interval_ms,
                                             repeat=repeat)
    plt.show()


if __name__ == '__main__':
    """Example usage."""
    from nuvox_algorithm.trace_algorithm.utils import load_train_set

    swipes = load_train_set()
    animate_swipe(swipes[0])
