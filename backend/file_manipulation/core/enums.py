from enum import Enum


class ProcessingStage(Enum):
    """
    Estágios do pipeline de processamento.
    """

    CHUNKIFICATION = "chunkification"
    STITCHING = "stitching"
    FILTERING = "filtering"
    OUTPUT = "output"


class QualityLevel(Enum):
    """
    Níveis de qualidade para filtragem.
    """

    LOW = 1.0
    MEDIUM = 2.0
    HIGH = 3.0
    ULTRA = 4.0
