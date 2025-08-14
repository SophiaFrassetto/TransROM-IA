from core.base_filter import QualityFilter
from datatypes.text_candidate import TextCandidate
import zlib


class CompressionRatioFilter(QualityFilter):
    """
    Filtro baseado em entropia de Shannon.
    Aprova textos cuja entropia está em um intervalo típico de dados textuais.
    """

    def __init__(self, max_compression_ratio: float = 0.75):
        self.max_compression_ratio = max_compression_ratio

    def filter(self, candidate: TextCandidate) -> float:
        if not candidate:
            return True
        ratio = len(zlib.compress(candidate.raw_bytes)) / len(candidate.raw_bytes)
        return ratio < self.max_compression_ratio
