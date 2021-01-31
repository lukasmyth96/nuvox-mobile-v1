from nuvox_algorithm.core.key import Key
from nuvox_algorithm.core.keyboard import Keyboard

__nuvox_keys = [
    Key(id='1', chars=['a', 'b', 'c'], x0=0/3, x1=1/3, y0=0/3, y1=1/3),
    Key(id='2', chars=['d', 'e', 'f'], x0=1/3, x1=2/3, y0=0/3, y1=1/3),
    Key(id='3', chars=['g', 'h', 'i'], x0=2/3, x1=3/3, y0=0/3, y1=1/3),
    Key(id='4', chars=['j', 'k', 'l'], x0=0/3, x1=1/3, y0=1/3, y1=2/3),
    Key(id='5', chars=[], x0=1/3, x1=2/3, y0=1/3, y1=2/3),
    Key(id='6', chars=['m', 'n', 'o'], x0=2/3, x1=3/3, y0=1/3, y1=2/3),
    Key(id='7', chars=['p', 'q', 'r', 's'], x0=0/3, x1=1/3, y0=2/3, y1=3/3),
    Key(id='8', chars=['t', 'u', 'v'], x0=1/3, x1=2/3, y0=2/3, y1=3/3),
    Key(id='9', chars=['w', 'x', 'y', 'z'], x0=2/3, x1=3/3, y0=2/3, y1=3/3),
]

# Keyboard instance that corresponds to the actual 3*3 nuvox keyboard.
nuvox_keyboard = Keyboard(keys=__nuvox_keys)
