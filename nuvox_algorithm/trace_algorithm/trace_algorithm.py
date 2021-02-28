from typing import Dict, List, Tuple, Optional

from matplotlib import pyplot as plt
import numpy as np

from nuvox_algorithm.core import nuvox_keyboard, TracePoint
from nuvox_algorithm.utils.list_funcs import filter_adjacent_duplicates
from nuvox_algorithm.trace_algorithm.utils import rdp, angle, get_corner_to_corner_variants


class TraceAlgorithm:
    def __init__(self, rdp_threshold: float, angle_threshold: float):
        self.rdp_threshold = rdp_threshold
        self.angle_threshold = angle_threshold

    def predict_intended_kis(self,
                             trace: List[TracePoint],
                             plot: Optional[bool] = False) -> Dict[str, float]:
        """This method receives a swipe trace and must return a dictionary
        mapping possible key-id-sequences (KIS) to the predicted probability
        that the user intended to swipe that sequence of keys.

        Notes
        --------
        - The values in the returned dictionary must be sum to 1.0 as
        the dictionary must describe a probability distribution.

        Returns
        --------
        kis_to_predicted_probability: Dict[str, float]
            Mapping from a possible key-id-sequence (e.g. '3246') to the predicted
            probability that the user intended to swipe that sequence of keys.
        """

        # All points as (x, y) tuples
        points = [(point.x, point.y) for point in trace]

        # Simplified path using Ramer–Douglas–Peucker algorithm
        rdp_points = rdp(points, self.rdp_threshold)

        # Array containing (Δx, Δy) vectors for each segment of path.
        path_vectors = np.diff(np.array(rdp_points), axis=0)

        # The angle between each successive segment in the path.
        # Note there is only n-2 angles for n points as you can't calculate angle for first and last.
        angles = angle(path_vectors)

        # Find the points in the rdp_points list where the angle at that point exceeds the angle threshold
        turning_point_indices = np.where(angles > self.angle_threshold)[0] + 1
        turning_points = [rdp_points[idx] for idx in turning_point_indices]

        # Use the key_at_point method to find the key_id at each turning point.
        turning_point_key_ids = [nuvox_keyboard.key_at_point(x=p[0], y=p[1]).id for p in turning_points]

        # The get the key_id at the first and last points as we know they must be in key-id-sequence
        first_key_id = nuvox_keyboard.key_at_point(x=points[0][0], y=points[0][1]).id
        last_key_id = nuvox_keyboard.key_at_point(x=points[-1][0], y=points[-1][1]).id

        # Combine to for list of key_ids
        key_ids = [first_key_id, *turning_point_key_ids, last_key_id]

        # Filter out adjacent duplicates i.e. [1, 2, 2, 3] --> [1, 2, 3]
        key_ids = filter_adjacent_duplicates(key_ids)

        # Filter out '5' as this key contains no characters so can't have been intended.
        key_ids = [key_id for key_id in key_ids if key_id != '5']

        # Convert list to string i.e. [1, 2, 3] --> '123' (lists cannot be keys of a dictionary)
        kis = ''.join(key_ids)

        if plot:
            self.plot_prediction(
                points=points,
                rdp_points=rdp_points,
                turning_point_indices=turning_point_indices,
                predicted_kis=kis
            )

        # For transitions from a corner key to an opposite corner
        # key (excluding diagonals) (e.g. 1-->3) we cannot
        # detect from turning points alone whether the
        # key in between was intended or not. For now we handle
        # this by assigning equal probability to the KIS where
        # the middle key is/isn't added. Read docstring of
        # 'get_corner_to_corner_variants' for further explanation.
        corner_to_corner_variants = get_corner_to_corner_variants(kis)
        prob = 1 / len(corner_to_corner_variants)

        kis_to_predicted_probability = {
            _kis: prob for _kis in corner_to_corner_variants
        }


        return kis_to_predicted_probability

    @staticmethod
    def plot_prediction(points: List[Tuple[float, float]],
                        rdp_points: List[Tuple[float, float]],
                        turning_point_indices: List[int],
                        predicted_kis: str) -> None:
        """Plots path, simplified (RDP) path and turning points."""

        fig = plt.figure()
        ax = fig.add_subplot(111)

        x = np.array([p[0] for p in points])
        y = np.array([p[1] for p in points])
        rdp_x = np.array([p[0] for p in rdp_points])
        rdp_y = np.array([p[1] for p in rdp_points])

        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.plot(x, y, 'b-', label='original path')
        ax.plot(rdp_x, rdp_y, 'g--', label='simplified path')
        ax.plot(rdp_x[turning_point_indices], rdp_y[turning_point_indices], 'ro', markersize=10, label='turning points')
        ax.invert_yaxis()
        plt.legend(loc='best')
        plt.title(f'Predicted KIS: {predicted_kis}')
        plt.show()
