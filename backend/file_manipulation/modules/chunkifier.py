from ..core.base_processor import DataProcessor
from ..core.enums import ProcessingStage
from ..utils.decorators import stage_logger, performance_monitor
from ..datatypes.chunk import Chunk
from typing import List


class Chunkifier(DataProcessor):
    """
    Processador para chunkificação de dados binários.
    Divide os dados em chunks sequenciais de tamanho fixo.
    """

    def __init__(self, chunk_size: int = 32):
        self.chunk_size = chunk_size

    @stage_logger(ProcessingStage.CHUNKIFICATION)
    @performance_monitor
    def process(self, data: bytes) -> List[Chunk]:
        """
        Corta os dados em chunks sequenciais de tamanho fixo.
        Args:
            data: Dados binários para processar
        Returns:
            Lista de chunks processados
        """
        chunks = []
        for i in range(0, len(data), self.chunk_size):
            chunk_bytes = data[i : i + self.chunk_size]
            if chunk_bytes:
                chunks.append(Chunk(offset=i, bytes=chunk_bytes))
        return chunks
