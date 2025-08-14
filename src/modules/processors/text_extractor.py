import string
from .base_processor import DataProcessor
from datatypes.text_candidate import TextCandidate


class TextBlockExtractor(DataProcessor):
    """
    Escaneia um stream de bytes para extrair blocos contíguos
    que se parecem com texto.
    """

    def __init__(self, min_block_size: int = 20, text_likeness_threshold: float = 0.8, window_size: int = 16):
        self.min_block_size = min_block_size
        self.text_likeness_threshold = text_likeness_threshold
        self.window_size = window_size
        self.PRINTABLE_CHARS = set(bytes(string.printable, "ascii"))

    def _get_text_likeness_score(self, data_slice: bytes) -> float:
        """Calcula uma pontuação simples baseada em caracteres imprimíveis."""
        if not data_slice:
            return 0.0
        printable_count = sum(1 for byte in data_slice if byte in self.PRINTABLE_CHARS)
        return printable_count / len(data_slice)

    def process(self, data: bytes, task, progress) -> list[TextCandidate]:
        """
        Extrai todos os blocos de texto de um conjunto de bytes.
        """
        candidates = []
        is_in_text_block = False
        start_index = 0  # Uma janela pequena para detectar transições

        progress.update(task, total=0, visible=True)
        progress.start_task(task)

        for i in range(len(data) - self.window_size):
            window = data[i : i + self.window_size]
            score = self._get_text_likeness_score(window)

            if not is_in_text_block and score >= self.text_likeness_threshold:
                # Início de um possível bloco de texto
                is_in_text_block = True
                start_index = i
            elif is_in_text_block and score < self.text_likeness_threshold:
                # Fim do bloco de texto
                is_in_text_block = False
                end_index = i

                # Adiciona o bloco se ele tiver um tamanho mínimo
                if (end_index - start_index) >= self.min_block_size:
                    candidate = TextCandidate(
                        start_offset=start_index,
                        end_offset=end_index,
                        raw_bytes=data[start_index:end_index],
                    )
                    candidate.quality_score = score
                    candidates.append(candidate)
                    progress.update(task, advance=1)

        # Caso o arquivo termine dentro de um bloco de texto
        if is_in_text_block and (len(data) - start_index) >= self.min_block_size:
            candidate = TextCandidate(
                start_offset=start_index,
                end_offset=end_index,
                raw_bytes=data[start_index:end_index],
            )
            candidate.quality_score = score
            candidates.append(candidate)
            progress.update(task, advance=1)
        return candidates
