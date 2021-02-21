from typing import Dict

from transformers import AutoModelForCausalLM, AutoTokenizer
from torch.nn import functional as F


class LanguageModel:

    def __init__(self):
        self.model_name = 'gpt2'
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name)

    @property
    def vocab(self):
        token_to_id = self.tokenizer.get_vocab()
        vocab = list(token_to_id)
        return vocab

    def predict_next_word(self, prompt: str) -> Dict[str, float]:
        if prompt == '':
            prompt = '.'  # requires token to start sentence
        token_ids = self.tokenizer.encode(text=prompt, return_tensors="pt")
        model_output = self.model(token_ids)
        next_token_logits = model_output.logits[:, -1, :]
        next_token_probs = F.softmax(next_token_logits, dim=-1)

        token_to_predicted_prob = {
            self.tokenizer.decode(idx): next_token_probs[0, idx].item()
            for idx in range(next_token_probs.shape[1])
        }

        return token_to_predicted_prob


if __name__ == '__main__':
    _prompt = 'The quick brown fox'
    m = LanguageModel()
    p = m.predict_next_word(_prompt)
