from typing import List, Tuple

from transformers import PreTrainedTokenizer

from nuvox_algorithm.core import Keyboard


def filter_predictions_by_key_id_sequence(ranked_token_ids: List[int],
                                          ranked_token_probs: List[float],
                                          tokenizer: PreTrainedTokenizer,
                                          keyboard: Keyboard,
                                          target_key_id_sequence: str
                                          ) -> Tuple[List[int], List[float]]:
    """Filter ranked list(s) of predicted token ids and their assigned probabilities
    to only include tokens for which the key-id-sequence (KIS) matched the given
    key_id_sequence.
    """
    filtered_ranked_token_ids = []
    filtered_ranked_token_probs = []
    for token_id, token_prob in zip(ranked_token_ids, ranked_token_probs):
        token = tokenizer._convert_id_to_token(token_id)
        token_kis = keyboard.text_to_kis(
            text=token,
            skip_invalid_chars=True
        )
        if token_kis == target_key_id_sequence:
            filtered_ranked_token_ids.append(token_id)
            filtered_ranked_token_probs.append(token_prob)

    return filtered_ranked_token_ids, filtered_ranked_token_probs
