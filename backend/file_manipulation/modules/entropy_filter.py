from ..core.base_filter import QualityFilter
from ..utils.entropy import EntropyCalculator
from ..datatypes.text_candidate import TextCandidate


class EntropyFilter(QualityFilter):
    """
    Filtro baseado em entropia de Shannon.
    Aprova textos cuja entropia está em um intervalo típico de dados textuais.
    """

    def __init__(self, min_entropy: float = 4.0, max_entropy: float = 6.5):
        self.min_entropy = min_entropy
        self.max_entropy = max_entropy

    def filter(self, candidate: TextCandidate) -> float:
        entropy = EntropyCalculator.shannon_entropy(candidate.raw_bytes)
        return 1.0 if self.min_entropy < entropy < self.max_entropy else 0.0
