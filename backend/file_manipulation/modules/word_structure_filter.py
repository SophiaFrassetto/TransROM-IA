from ..core.base_filter import QualityFilter
from ..datatypes.text_candidate import TextCandidate


class WordStructureFilter(QualityFilter):
    """
    Filtro baseado na estrutura de palavras.
    Bonifica textos que possuem múltiplas palavras e palavras de tamanho razoável.
    """

    def filter(self, candidate: TextCandidate) -> float:
        words = candidate.text_content.split()
        if len(words) <= 1:
            return 0.0
        score = 0.5  # Bônus por ter múltiplas palavras
        if words:
            avg_word_len = sum(len(w) for w in words) / len(words)
            if 2 < avg_word_len < 12:
                score += 0.5
        return score
