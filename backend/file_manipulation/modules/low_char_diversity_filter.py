from ..core.base_filter import QualityFilter
from ..datatypes.text_candidate import TextCandidate


class LowCharDiversityFilter(QualityFilter):
    """
    Filtro que penaliza textos com baixa diversidade de caracteres.
    Se o número de caracteres únicos for muito pequeno em relação ao tamanho do texto, penaliza.
    """

    def __init__(self, min_unique_ratio: float = 0.15):
        self.min_unique_ratio = min_unique_ratio

    def filter(self, candidate: TextCandidate) -> float:
        text = candidate.text_content
        n = len(text)
        if n < 10:
            return 0.0
        unique_chars = set(text)
        ratio = len(unique_chars) / n
        return -1.0 if ratio < self.min_unique_ratio else 0.0
