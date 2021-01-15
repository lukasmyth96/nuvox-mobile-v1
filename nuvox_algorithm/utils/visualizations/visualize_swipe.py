from matplotlib import pyplot as plt
import matplotlib.image as mpimg
import matplotlib.cm as cm
import random


from nuvox_algorithm.core import nuvox_key_list, Keyboard
from nuvox_algorithm.trace_algorithm.swipe import Swipe
from nuvox_algorithm.trace_algorithm.create_dataset import create_dataset


def visualize_swipe(swipe: Swipe, keyboard_img_file_path: str):
    """Plots a single swipe over keyboard background image."""
    img = mpimg.imread(keyboard_img_file_path)
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


if __name__ == '__main__':
    """Example usage."""
    keyboard = Keyboard(keys=nuvox_key_list)
    data_dump_file_path = '/home/luka/PycharmProjects/nuvox-mobile/nuvox_app/trace_algorithm_dataset_09_01_2021.json'
    keyboard_img_file_path = '/home/luka/PycharmProjects/nuvox-mobile/nuvox_app/keyboard/static/keyboard/assets/nuvox_keyboard_img.png'
    swipes = create_dataset(
        data_dump_file_path=data_dump_file_path,
        keyboard=keyboard,
        remove_inaccurate_swipes=True
    )

    random.shuffle(swipes)
    for swipe in swipes[:50]:
        visualize_swipe(
            swipe=swipe,
            keyboard_img_file_path=keyboard_img_file_path
        )
