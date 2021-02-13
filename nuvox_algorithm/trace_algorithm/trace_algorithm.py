from typing import Dict, List

from matplotlib import pyplot as plt
import numpy as np

from nuvox_algorithm.core import nuvox_keyboard, TracePoint
from nuvox_algorithm.utils.list_funcs import filter_adjacent_duplicates
from nuvox_algorithm.trace_algorithm.utils import rdp, angle


class TraceAlgorithm:
    def __init__(self, rdp_threshold: float, angle_threshold: float):
        # The init method can be used to load a machine learning model or simply
        # set some configurations for your trace algorithm. You do not have to
        # use it if you do not need it.
        self.rdp_threshold = rdp_threshold
        self.angle_threshold = angle_threshold

    def predict_intended_kis(self, trace: List[TracePoint]) -> Dict[str, float]:
        """This method receives a swipe trace (chronological list
        of TracePoint objects) and must return a dictionary mapping possible
        key-id-sequences (KIS) to the predicted probability that the user
        intended to swipe that sequence of keys.

        Notes
        --------
        - The values (predicted probabilities) in the returned
        dictionary must be sum to 1.0 as the dictionary must describe
        a probability distribution.

        Example
        --------
        - If a user attempts to swipe the word 'beg', their trace will
        presumably pass over keys 1 --> 2 --> 3.
        - In this case the true intended KIS would be '123' because
        the word 'beg' requires 'b' from key 1, 'e' from key 2 and 'g' from key 3.
        - For this input trace, this function may, for example, return:
          {
            '123': 0.8,
            '13': 0.2
          }
          thereby assigning a probability of 0.8 that the user intended the KIS
          1->2->3 and probability of 0.2 that the user only intended 1->3.
        """

        # All points as (x, y) tuples
        points = [(point.x, point.y) for point in trace]

        # Simplified path using Ramer–Douglas–Peucker algorithm algorithm
        rdp_points = rdp(points, self.rdp_threshold)

        # Array containing (Δx, Δy) vectors for each segment of path.
        vectors = np.diff(np.array(rdp_points), axis=0)

        # The angle between each successive segment in the path.
        # Note there is only n-2 angles for n points as you can't calculate angle for first and last.
        angles = angle(vectors)

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

        # Convert list to string i.e. [1, 2, 3] --> '123'
        kis = ''.join(key_ids)

        kis_to_predicted_probability = {
            kis: 1.0
        }

        # Uncomment this to plot the path and turning points...
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
        plt.show()

        return kis_to_predicted_probability
