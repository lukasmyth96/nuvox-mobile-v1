from typing import List, Dict

from nuvox_algorithm.core import nuvox_keyboard, TracePoint
from nuvox_algorithm.language_model import LanguageModel
from nuvox_algorithm.trace_algorithm import TraceAlgorithm


class NuvoxAlgorithm:

    def __init__(self):
        self.language_model = LanguageModel()
        self.trace_algorithm = TraceAlgorithm(rdp_threshold=0.008, angle_threshold=0.485)
        self.keyboard = nuvox_keyboard
        self.token_to_kis = {
            token: self.keyboard.text_to_kis(text=token, skip_invalid_chars=True)
            for token in self.language_model.vocab
        }

    def predict(self, prompt: str, trace: List[TracePoint]):

        # Language Model
        token_to_lang_model_pred_prob = self.language_model.predict_next_word(prompt=prompt)

        # Trace Algorithm
        kis_to_trace_algo_pred_prob = self.trace_algorithm.predict_intended_kis(trace=trace)
        token_to_trace_algo_pred_prob = {
            token: kis_to_trace_algo_pred_prob.get(self.token_to_kis[token], 0.0)
            for token in self.language_model.vocab
        }

        # Combine Predictions
        token_to_joint_prob = self.joint_prob(
            token_to_trace_algo_pred_prob,
            token_to_lang_model_pred_prob
        )

        return token_to_joint_prob

    def joint_prob(self,
                   token_to_trace_algo_prob: Dict[str, float],
                   token_to_lang_model_prob: Dict[str, float]) -> Dict[str, float]:
        """Returns dict mapping each token to the joint probability from
        the trace algorithm and laguage model"""
        return {
            token: (token_to_lang_model_prob.get(token, 0.0) * token_to_trace_algo_prob.get(token, 0.0))
            for token in self.language_model.vocab
        }


if __name__ == '__main__':
    import random
    from nuvox_algorithm.trace_algorithm.utils import load_train_set
    _swipes = load_train_set()
    _nuvox = NuvoxAlgorithm()
    random.shuffle(_swipes)
    for swipe in _swipes:
        _prompt = input(f'Type suitable prompt for: "{swipe.target_text}": ')
        token_to_joint_prob = _nuvox.predict(_prompt, swipe.trace)
        top_5 = [k for k, v in sorted(token_to_joint_prob.items(), key=lambda item: item[1], reverse=True)[:5]]
        print(f'Correct: {swipe.target_text}\n'
              f'Top-5: {" ".join(top_5)}\n')
