from typing import Dict, List

from matplotlib import pyplot as plt
import numpy as np

from nuvox_algorithm.core import nuvox_keyboard
from nuvox_algorithm.trace_algorithm.swipe import TracePoint
from nuvox_algorithm.utils.list_funcs import filter_adjacent_duplicates
from nuvox_algorithm.trace_algorithm.rdp import rdp
from nuvox_algorithm.trace_algorithm.angle import angle


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

        points = [(point.x, point.y) for point in trace]

        rdp_points = rdp(points, self.rdp_threshold)

        vectors = np.diff(np.array(rdp_points), axis=0)

        angles = angle(vectors)

        turning_point_indices = np.where(angles > self.angle_threshold)[0] + 1
        turning_points = [rdp_points[idx] for idx in turning_point_indices]
        turning_point_key_ids = [nuvox_keyboard.key_at_point(x=p[0], y=p[1]).id for p in turning_points]
        first_key_id = nuvox_keyboard.key_at_point(x=points[0][0], y=points[0][1]).id
        last_key_id = nuvox_keyboard.key_at_point(x=points[-1][0], y=points[-1][1]).id
        key_ids = [first_key_id, *turning_point_key_ids, last_key_id]
        key_ids = filter_adjacent_duplicates(key_ids)
        kis = ''.join(key_ids)

        kis_to_predicted_probability = {
            kis: 1.0
        }

        # PLOTTING
        # fig = plt.figure()
        # ax = fig.add_subplot(111)
        #
        # x = np.array([p[0] for p in points])
        # y = np.array([p[1] for p in points])
        # rdp_x = np.array([p[0] for p in rdp_points])
        # rdp_y = np.array([p[1] for p in rdp_points])
        #
        # ax.plot(x, y, 'b-', label='original path')
        # ax.plot(rdp_x, rdp_y, 'g--', label='simplified path')
        # ax.plot(rdp_x[turning_point_indices], rdp_y[turning_point_indices], 'ro', markersize=10, label='turning points')
        # ax.invert_yaxis()
        # plt.legend(loc='best')
        # plt.show()

        return kis_to_predicted_probability


if __name__ == '__main__':
    from nuvox_algorithm.trace_algorithm.utils import load_train_set
    trace_algorithm = TraceAlgorithm(rdp_threshold=0.01, angle_threshold=np.pi * 0.22)
    swipes = load_train_set()
    for swipe in swipes[:10]:
        prediction = trace_algorithm.predict_intended_kis(swipe.trace)
        print(f'Prediction for word: {swipe.target_text} with KIS {swipe.target_kis} is : {prediction.keys()}')

