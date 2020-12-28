import os
from typing import Generator

import numpy as np
from transformers import AutoModelForCausalLM, AutoTokenizer
from torch.nn import functional as F
from tqdm import tqdm

from nuvox_algorithm.utils.io_funcs import read_text_file

if __name__ == '__main__':
    """
    This script evaluates the performance of a pre-trained language model
    on the task of predicting the next word in a sentence. It outputs the
    following metrics:
    - top-3 accuracy (% of prompts for which the model's top-3 predictions contain the true next word)
    - average true token rank (The average ranking of the true next word among the models predictions)
    - average true token prob (The average probability assigned to the true next token.)
    """

    # Configuration
    MODEL_NAME = 'gpt2'
    DATASET_DIR = '/home/luka/Downloads/openwebtext'  # directory containing .txt files.
    K = 3

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

    # List[bool], whether the top predicted word is correct for each word.
    top_1_accuracy_list = []

    # List[bool], whether the true word was in top-k for all words.
    top_k_accuracy_list = []

    # List[int]
    true_token_rank_list = []

    true_token_prob_list = []

    file_names = [f for f in os.listdir(DATASET_DIR) if f.endswith('.txt')]
    file_names_tqdm = tqdm(file_names)
    for file_name in file_names_tqdm:
        file_path = os.path.join(DATASET_DIR, file_name)
        lines = read_text_file(file_path).split('\n\n')
        for line in lines:

            if not line:
                continue  # skip empty lines.

            input_ids = tokenizer.encode(text=line, return_tensors="pt")
            model_output = model(input_ids)
            for position in range(input_ids.shape[1] - 1):
                # Predict and rank tokens
                next_token_logits = model_output.logits[:, position, :]
                probs = F.softmax(next_token_logits, dim=-1)
                ranked = probs.topk(k=tokenizer.vocab_size)
                ranked_token_ids = ranked.indices.tolist()[0]
                ranked_token_probs = ranked.values.tolist()[0]
                # top_k_tokens = [tokenizer.decode(token_id) for token_id in ranked_token_ids[:K]] # only used for debugging.

                # Track metrics
                true_next_token_id = input_ids[0, position + 1]
                top_1_accuracy_list.append(true_next_token_id == ranked_token_ids[0])
                top_k_accuracy_list.append(true_next_token_id in ranked_token_ids[:K])
                true_token_rank = ranked_token_ids.index(true_next_token_id) + 1
                true_token_prob = ranked_token_probs[true_token_rank - 1]
                true_token_rank_list.append(true_token_rank)
                true_token_prob_list.append(true_token_prob)

        top_1_acc = np.mean(top_1_accuracy_list)
        top_k_acc = np.mean(top_k_accuracy_list)
        avg_true_token_rank = np.mean(true_token_rank_list)
        avg_true_token_prob = np.mean(true_token_prob_list)
        file_names_tqdm.set_description(desc=f'| top_1_acc: {top_1_acc:.2%}'
                                             f'| top_{K}_acc: {top_k_acc:.2%}'
                                             f'| avg_true_token_rank: {avg_true_token_rank:.1f}'
                                             f'| avg_true_token_prob: {avg_true_token_prob:.1f}')
