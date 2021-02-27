from typing import Dict, List

from transformers import AutoModelForCausalLM, AutoTokenizer
from torch.nn import functional as F


class LanguageModel:

    def __init__(self):
        self.model_name = 'gpt2'
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
        self.token_to_id = self.tokenizer.get_vocab()
        self.vocab = list(self.token_to_id)

    def predict_next_token(self, prompt: str, possible_tokens: List[str]) -> Dict[str, float]:
        """Returns dictionary mapping each token in to the list of
         "possible_tokens"  to the language model's predicted probability
        that the token is the next token following the text prompt."""

        if prompt == '':
            prompt = '.'  # requires token to start sentence

        token_ids = self.tokenizer.encode(text=prompt, return_tensors="pt")

        model_output = self.model(token_ids)

        next_token_logits = model_output.logits[:, -1, :]

        next_token_probs = F.softmax(next_token_logits, dim=-1)

        token_to_predicted_prob = {
            token: next_token_probs[0, self.token_to_id[token]].item()
            for token in possible_tokens
        }

        return token_to_predicted_prob
