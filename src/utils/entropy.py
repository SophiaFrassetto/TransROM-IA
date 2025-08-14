from collections import Counter
import math


class EntropyCalculator:
    """
    Calculadora de entropia de Shannon para dados binários.
    """

    def shannon_entropy(data_slice: bytes) -> float:
        """
        Calcula a Entropia de Shannon para uma fatia de dados em bytes.
        Args:
            data_slice: Dados binários para análise
        Returns:
            Valor da entropia entre 0 e 8
        """
        if not data_slice:
            return 0.0
        byte_counts = Counter(data_slice)
        data_len = len(data_slice)
        entropy = 0.0
        for count in byte_counts.values():
            p_x = count / data_len
            if p_x > 0:
                entropy -= p_x * math.log2(p_x)
        return entropy
