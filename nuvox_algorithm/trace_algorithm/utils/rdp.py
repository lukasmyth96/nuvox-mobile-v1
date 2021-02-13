from math import sqrt
from typing import List, Tuple


def distance(point_a: Tuple[float, float],
             point_b: Tuple[float, float]) -> float:
    """Returns Euclidean distance between two (x, y) points."""
    return sqrt((point_a[0] - point_b[0]) ** 2 + (point_a[1] - point_b[1]) ** 2)


def point_line_distance(point: Tuple[float, float],
                        start_point: Tuple[float, float],
                        end_point: Tuple[float, float]) -> float:
    """Returns perpendicular distance between 'point' and a the
    straight line between 'start_point' and 'end_point'."""
    if start_point == end_point:
        return distance(point, start_point)
    else:
        n = abs(
            (end_point[0] - start_point[0]) * (start_point[1] - point[1]) -
            (start_point[0] - point[0]) * (end_point[1] - start_point[1])
        )
        d = sqrt(
            (end_point[0] - start_point[0]) ** 2 + (end_point[1] - start_point[1]) ** 2
        )
        return n / d


def rdp(points: List[Tuple[float, float]], epsilon: float) -> List[Tuple[float, float]]:
    """Ramer–Douglas–Peucker algorithm

    Reduces a series of points to a simplified version that loses detail,
    but maintains the general shape of the series.

    Notes
    ------
    - Read more about the algorithm here: https://en.wikipedia.org/wiki/Ramer%E2%80%93Douglas%E2%80%93Peucker_algorithm
    """
    dmax = 0.0
    index = 0
    # Find which point in the path is the furthest distance
    # from the line between the start and end point.
    for i in range(1, len(points) - 1):
        d = point_line_distance(points[i], points[0], points[-1])
        if d > dmax:
            index = i
            dmax = d

    if dmax >= epsilon:
        # If the furthest point is at least epsilon distance from the line then
        # it will be included in the simplified path and we recursively call
        # rdp on the sub-paths that precede and follow this point.
        results = rdp(points[:index + 1], epsilon)[:-1] + rdp(points[index:], epsilon)
    else:
        # Else the path can be simplified to just the first and last point.
        results = [points[0], points[-1]]

    return results
