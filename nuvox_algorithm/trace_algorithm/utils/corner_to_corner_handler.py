from typing import Optional

from nuvox_algorithm.utils.list_funcs import sequential_pairs

corner_corner_to_middle = {
    '13': '2',
    '31': '2',
    '17': '4',
    '71': '4',
    '39': '6',
    '93': '6',
    '79': '8',
    '97': '8'
}


def get_corner_to_corner_variants(kis, n: Optional[int] = 0):
    c = 0
    for idx, (k1, k2) in enumerate(sequential_pairs(kis)):
        middle_key = corner_corner_to_middle.get(f'{k1}{k2}')
        if middle_key is not None:
            if c == n:
                kis_with_middle_key = f'{kis[:idx + 1]}{middle_key}{kis[idx + 1:]}'
                return [*get_corner_to_corner_variants(kis, n + 1), *get_corner_to_corner_variants(kis_with_middle_key, n)]
            else:
                c += 1
    return [kis]


if __name__ == '__main__':
    a = get_corner_to_corner_variants('139')
    print(a)
