from collections import defaultdict
from typing import List, Dict

from nuvox_algorithm.utils.dict_funcs import ranked_keys
from nuvox_algorithm.utils.list_funcs import filter_duplicates
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
        self.kis_to_tokens = defaultdict(list)
        for token, kis in self.token_to_kis.items():
            self.kis_to_tokens[kis].append(token)

    def predict(self, prompt: str, trace: List[TracePoint]) -> List[str]:

        # Trace Algorithm
        kis_to_trace_algo_pred_prob = self.trace_algorithm.predict_intended_kis(trace=trace)
        token_to_trace_algo_pred_prob = {
            token: prob
            for kis, prob in kis_to_trace_algo_pred_prob.items()
            for token in self.kis_to_tokens[kis]
        }

        # Language Model
        possible_tokens = list(token_to_trace_algo_pred_prob)
        token_to_lang_model_pred_prob = self.language_model.predict_next_token(
            prompt=prompt,
            possible_tokens=possible_tokens
        )

        # Calculate Joint Probability
        token_to_joint_prob = self.joint_prob(
            token_to_trace_algo_pred_prob,
            token_to_lang_model_pred_prob
        )

        ranked_words = ranked_keys(token_to_joint_prob)
        ranked_words = [self.language_model.tokenizer.convert_tokens_to_string(w) for w in ranked_words]
        if prompt == '':
            ranked_words = [w.lstrip().capitalize() for w in ranked_words]
        ranked_words = filter_duplicates(ranked_words)
        print('Ranked words: ', ranked_words)

        return ranked_words

    def joint_prob(self,
                   token_to_trace_algo_prob: Dict[str, float],
                   token_to_lang_model_prob: Dict[str, float]) -> Dict[str, float]:
        """Returns dict mapping each token to the joint probability from
        the trace algorithm and laguage model"""
        possible_tokens = set(token_to_trace_algo_prob)
        assert possible_tokens == set(token_to_lang_model_prob)
        return {
            token: (token_to_lang_model_prob[token] * token_to_trace_algo_prob[token])
            for token in possible_tokens
        }
