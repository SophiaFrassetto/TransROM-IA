from core.base_processor import DataProcessor
from datatypes.chunk import Chunk
from datatypes.text_candidate import TextCandidate
from typing import List


class ContextStitcher(DataProcessor):
    """
    Processador para costura de contexto.
    Junta chunks sequenciais que parecem texto para formar candidatos maiores.
    """

    def __init__(self, printable_threshold: float = 0.5):
        self.printable_threshold = printable_threshold

    def process(self, chunks: List[Chunk], task, progress) -> List[TextCandidate]:
        """
        Costura chunks sequenciais que parecem texto para formar candidatos maiores.
        Args:
            chunks: Lista de chunks para processar
        Returns:
            Lista de candidatos costurados
        """
        progress.update(task, total=int(len(chunks)))
        progress.start_task(task)
        stitched_candidates = []
        i = 0
        while i < len(chunks):
            current_chunk = chunks[i]
            if current_chunk.text_score >= self.printable_threshold:
                candidate_start_offset = current_chunk.offset
                candidate_bytes = bytearray(current_chunk.bytes)
                j = i + 1
                while (
                    j < len(chunks) and chunks[j].text_score >= self.printable_threshold
                ):
                    candidate_bytes.extend(chunks[j].bytes)
                    j += 1
                candidate_end_offset = candidate_start_offset + len(candidate_bytes)
                stitched_candidates.append(
                    TextCandidate(
                        start_offset=candidate_start_offset,
                        end_offset=candidate_end_offset,
                        raw_bytes=bytes(candidate_bytes),
                    )
                )
                i = j
                progress.update(task, advance=1)
            else:
                i += 1
        return stitched_candidates
