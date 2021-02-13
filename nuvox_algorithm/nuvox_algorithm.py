from typing import List, Dict

from .core import nuvox_keyboard, TracePoint
from .language_model import LanguageModel
from .trace_algorithm import TraceAlgorithm


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

        # Trace Algorithm
        kis_to_trace_algo_pred_prob = self.trace_algorithm.predict_intended_kis(trace=trace)
        token_to_trace_algo_pred_prob = {
            token: kis_to_trace_algo_pred_prob.get(self.token_to_kis[token], 0.0)
            for token in self.language_model.vocab
        }

        # Language Model
        token_to_lang_model_pred_prob = self.language_model.predict_next_word(prompt=prompt)

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
            token: (token_to_lang_model_prob[token] * token_to_trace_algo_prob[token])
            for token in self.language_model.vocab
        }
