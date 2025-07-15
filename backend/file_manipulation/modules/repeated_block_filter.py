from ..core.base_filter import QualityFilter
from ..datatypes.text_candidate import TextCandidate
from collections import Counter


class RepeatedBlockFilter(QualityFilter):
    """
    Filtro que penaliza repetições de blocos (ex: ABABAB, 123123123).
    Divide o texto em blocos de tamanho 2 a 8 e verifica se há repetições.
    Penaliza se um bloco se repete muitas vezes.
    """

    def __init__(self, min_repeats: int = 3, max_block_ratio: float = 0.6):
        self.min_repeats = min_repeats
        self.max_block_ratio = max_block_ratio

    def filter(self, candidate: TextCandidate) -> float:
        text = candidate.text_content
        n = len(text)
        for block_size in range(2, min(9, n // 2 + 1)):
            blocks = [text[i : i + block_size] for i in range(0, n, block_size)]
            block_counts = Counter(blocks)
            most_common, count = block_counts.most_common(1)[0]
            if (
                count >= self.min_repeats
                and (count * block_size) / n > self.max_block_ratio
            ):
                return -1.0
        return 0.0
