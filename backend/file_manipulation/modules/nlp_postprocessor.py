import torch
from transformers import GPT2LMHeadModel, GPT2TokenizerFast
from ..datatypes.text_candidate import TextCandidate
from typing import List


class NLPPostProcessor:
    """
    Pós-processador para filtragem NLP baseada em perplexidade e outros critérios.
    Suporta textos longos dividindo-os em janelas (sliding window).
    """

    def __init__(
        self,
        perplexity_threshold: float = 200.0,
        min_length: int = 10,
        model_id: str = "distilgpt2",
        window_size: int = 1024,
        stride: int = 1024,
        agg: str = "mean",
    ):
        self.perplexity_threshold = perplexity_threshold
        self.min_length = min_length
        self.window_size = window_size
        self.stride = stride
        self.agg = agg  # 'mean', 'min', 'max'
        try:
            self.model = GPT2LMHeadModel.from_pretrained(model_id)
            self.tokenizer = GPT2TokenizerFast.from_pretrained(model_id)
            self.model.eval()
            self.model_max_length = getattr(self.model.config, "n_positions", 1024)
        except Exception as e:
            import logging

            logging.getLogger(__name__).warning(
                f"Não foi possível carregar o modelo {model_id}: {e}"
            )
            self.model = None
            self.tokenizer = None
            self.model_max_length = 1024

    def _windowed_perplexity(self, text: str) -> float:
        """
        Calcula a perplexidade de um texto, dividindo-o em janelas se for maior que o limite do modelo.
        """
        tokens = self.tokenizer.encode(text)
        if len(tokens) <= self.window_size:
            inputs = self.tokenizer(text, return_tensors="pt")
            with torch.no_grad():
                outputs = self.model(**inputs, labels=inputs["input_ids"])
            return torch.exp(outputs.loss).item()
        perplexities = []
        for i in range(0, len(tokens), self.stride):
            window = tokens[i : i + self.window_size]
            if len(window) < 10:
                continue
            window_text = self.tokenizer.decode(window)
            inputs = self.tokenizer(window_text, return_tensors="pt")
            with torch.no_grad():
                outputs = self.model(**inputs, labels=inputs["input_ids"])
            perplexities.append(torch.exp(outputs.loss).item())
        if not perplexities:
            return float("inf")
        if self.agg == "min":
            return min(perplexities)
        elif self.agg == "max":
            return max(perplexities)
        else:
            return sum(perplexities) / len(perplexities)

    def filter(self, candidates: List[TextCandidate], return_rejected: bool = False):
        """
        Filtra candidatos usando perplexidade NLP (com suporte a textos longos).
        """
        if self.model is None or self.tokenizer is None:
            import logging

            logging.getLogger(__name__).warning(
                "Filtro NLP ignorado por falha ao carregar modelo."
            )
            return (candidates, []) if return_rejected else candidates
        final_candidates = []
        rejected = []
        for cand in candidates:
            text = cand.text_content.strip()
            if len(text) < self.min_length:
                rejected.append(cand)
                continue
            try:
                cand.perplexity = self._windowed_perplexity(text)
                if cand.perplexity < self.perplexity_threshold:
                    final_candidates.append(cand)
                else:
                    rejected.append(cand)
            except Exception as e:
                rejected.append(cand)
                continue
        if return_rejected:
            return final_candidates, rejected
        return final_candidates
