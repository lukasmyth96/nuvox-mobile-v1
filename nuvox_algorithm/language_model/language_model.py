from typing import Dict

from transformers import AutoModelForCausalLM, AutoTokenizer
from torch.nn import functional as F


class LanguageModel:

    def __init__(self):
        self.model_name = 'gpt2'
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name)

    def predict_next_word(self, prompt: str) -> Dict[str, float]:
        token_ids = self.tokenizer.encode(text=prompt, return_tensors="pt")
        model_output = self.model(token_ids)
        next_token_logits = model_output.logits[:, -1, :]
        next_token_probs = F.softmax(next_token_logits, dim=-1)
        ranked = next_token_probs.topk(k=self.tokenizer.vocab_size)
        ranked_token_ids = ranked.indices.tolist()[0]
        ranked_token_probs = ranked.values.tolist()[0]

        token_to_predicted_prob = {
            self.tokenizer.decode(token_id): prob
            for token_id, prob in zip(ranked_token_ids, ranked_token_probs)
        }

        return token_to_predicted_prob


if __name__ == '__main__':
    _prompt = 'The quick brown fox'
    m = LanguageModel()
    p = m.predict_next_word(_prompt)
