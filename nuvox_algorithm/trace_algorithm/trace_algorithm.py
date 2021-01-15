from typing import Dict, List

from nuvox_algorithm.trace_algorithm.swipe import TracePoint
from nuvox_algorithm.utils.list_funcs import filter_adjacent_duplicates


class TraceAlgorithm:
    def __init__(self):
        # The init method can be used to load a machine learning model or simply
        # set some configurations for your trace algorithm. You do not have to
        # use it if you do not need it.
        pass

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
        # Below I have implemented an incredibly simple (though not very good) algorithm
        # as a demonstration. It works by simply assuming that every key that was passed
        # over during the swipe was intended as part of the word the user wanted to write.

        # Get sequence of key_ids for each point in the trace e.g. ['1', '1', '1', '2', '3', '3'...]
        sequence_of_key_ids_passed_over = [trace_point.key_id for trace_point in trace]

        # Filter out adjacent duplicates e.g. ['1', '1', '1', '2', '3', '3'...] --> ['1', '2', '3']
        sequence_of_key_ids_passed_over = filter_adjacent_duplicates(sequence_of_key_ids_passed_over)

        # Return dictionary where this key-id-sequence is assigned a probability of 1.0 of being
        # the intended KIS. Note we join the individual key ids into one string as the output expects.
        kis_to_predicted_probability = {
            ''.join(sequence_of_key_ids_passed_over): 1.0
        }

        # If you're interested... this simple algorithm predicts the intended KIS ~10% of the time - hopfully you
        # can do better...
        return kis_to_predicted_probability
