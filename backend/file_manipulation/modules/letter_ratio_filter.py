from ..core.base_filter import QualityFilter
from ..datatypes.text_candidate import TextCandidate
import string


class LetterRatioFilter(QualityFilter):
    """
    Filtro baseado na razão de letras.
    Aprova textos com alta proporção de letras em relação ao total de caracteres.
    """

    def __init__(self, min_ratio: float = 0.7):
        self.min_ratio = min_ratio
        self.letter_bytes = set(bytes(string.ascii_letters, "ascii"))

    def filter(self, candidate: TextCandidate) -> float:
        text_content = candidate.text_content.strip()
        if not text_content:
            return 0.0
        letter_count = sum(
            1 for byte in candidate.raw_bytes if byte in self.letter_bytes
        )
        letter_ratio = letter_count / len(text_content)
        return 1.0 if letter_ratio > self.min_ratio else 0.0
