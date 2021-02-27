from typing import Dict, List

from transformers import AutoModelForCausalLM, AutoTokenizer
from torch.nn import functional as F

from definition import LANGUAGE_MODEL_VOCAB_PATH
from nuvox_algorithm.utils.io_funcs import read_json_file


class LanguageModel:

    def __init__(self):
        """Wrapper class for GPT-2 language model provided
        by Hugging Face "transformers" package."""

        self.model_name = 'gpt2'
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
        self.token_to_id = self.tokenizer.get_vocab()
        self.vocab = read_json_file(LANGUAGE_MODEL_VOCAB_PATH)

    def predict_next_token(self, prompt: str, possible_tokens: List[str]) -> Dict[str, float]:
        """Returns dictionary mapping each token in to the list of
        "possible_tokens"  to the language model's predicted probability
        that the token is the next token following the text prompt.

        Notes
        -------
        - Vocabulary is restricted to the tokens contained in the
        "cleaned_vocab.json" file to prevent returning nonsense
        tokens.
        """

        if prompt == '':
            prompt = self.tokenizer.bos_token  # requires token to start sentence

        token_ids = self.tokenizer.encode(text=prompt, return_tensors="pt")

        model_output = self.model(token_ids)

        next_token_logits = model_output.logits[:, -1, :]

        next_token_probs = F.softmax(next_token_logits, dim=-1)

        token_to_predicted_prob = {
            token: next_token_probs[0, self.token_to_id[token]].item()
            for token in possible_tokens
        }

        return token_to_predicted_prob
