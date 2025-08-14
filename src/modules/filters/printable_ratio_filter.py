from .base_filter import QualityFilter
from datatypes.text_candidate import TextCandidate
import string


class PrintableRatioFilter(QualityFilter):
    """
    Filtro baseado em entropia de Shannon.
    Aprova textos cuja entropia está em um intervalo típico de dados textuais.
    """

    def __init__(
        self, min_printable_ratio: float = 0.70
    ):
        self.min_printable_ratio = min_printable_ratio
        self.PRINTABLE_CHARS = set(bytes(string.printable, 'ascii'))

    def filter(self, candidate: TextCandidate) -> float:
        if not candidate:
            return True
        ratio = sum(1 for byte in candidate.raw_bytes if byte in self.PRINTABLE_CHARS) / len(
            candidate.raw_bytes
        )
        return 0.1 if ratio >= self.min_printable_ratio else 0.0
