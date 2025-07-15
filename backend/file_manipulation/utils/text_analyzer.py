import string
from typing import Dict


class TextAnalyzer:
    """
    Analisador de texto para detecção de qualidade e padrões.
    """

    def __init__(self):
        self.printable_bytes = set(bytes(string.printable, "ascii"))
        self.letter_bytes = set(bytes(string.ascii_letters, "ascii"))

    def analyze_structure(self, text_content: str) -> Dict[str, float]:
        """
        Analisa a estrutura do texto para determinar qualidade.
        Retorna métricas como razão de letras, contagem de palavras, tamanho médio de palavra e detecção de gagueira.
        """
        text_len = len(text_content.strip())
        if text_len < 1:
            return {}
        words = text_content.split()
        letter_count = sum(1 for char in text_content if ord(char) in self.letter_bytes)
        metrics = {
            "letter_ratio": letter_count / text_len if text_len > 0 else 0.0,
            "word_count": len(words),
            "avg_word_length": (
                sum(len(w) for w in words) / len(words) if words else 0.0
            ),
            "has_stutter": self._detect_stutter(text_content),
        }
        return metrics

    def _detect_stutter(self, text: str) -> bool:
        """
        Detecta repetições excessivas de caracteres (gagueira).
        """
        for i in range(len(text) - 2):
            if text[i] == text[i + 1] == text[i + 2] and text[i] != " ":
                return True
        return False
