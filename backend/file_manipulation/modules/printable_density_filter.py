from ..core.base_filter import QualityFilter
from ..datatypes.text_candidate import TextCandidate


class PrintableDensityFilter(QualityFilter):
    """
    Filtro baseado na densidade de caracteres imprimíveis.
    Aprova textos com alta proporção de caracteres imprimíveis.
    """

    def __init__(self, min_density: float = 0.9):
        self.min_density = min_density

    def filter(self, candidate: TextCandidate) -> float:
        if len(candidate.raw_bytes) == 0:
            return 0.0
        printable_density = len(candidate.text_content) / len(candidate.raw_bytes)
        return 1.0 if printable_density > self.min_density else 0.0
