from ..core.base_filter import QualityFilter
from ..datatypes.text_candidate import TextCandidate
from collections import Counter


class LinearSequenceFilter(QualityFilter):
    """
    Filtro que penaliza sequências lineares (ex: ABCDE, 12345, etc).
    Detecta padrões onde a maioria das diferenças entre caracteres consecutivos é igual.
    Penaliza se mais de max_linear_ratio das diferenças forem iguais.
    """

    def __init__(self, max_linear_ratio: float = 0.7):
        self.max_linear_ratio = max_linear_ratio

    def filter(self, candidate: TextCandidate) -> float:
        text = candidate.text_content
        if len(text) < 5:
            return 0.0
        diffs = [ord(text[i + 1]) - ord(text[i]) for i in range(len(text) - 1)]
        if not diffs:
            return 0.0
        most_common, count = Counter(diffs).most_common(1)[0]
        ratio = count / len(diffs)
        return -1.0 if ratio > self.max_linear_ratio else 0.0
