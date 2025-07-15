from dataclasses import dataclass
from .enums import QualityLevel


@dataclass
class PipelineConfig:
    """
    Configuração do pipeline de processamento.
    Permite ajustar chunk_size, thresholds e nível de qualidade.
    """

    chunk_size: int = 32
    printable_threshold: float = 0.5
    min_score_threshold: float = 2.0
    quality_level: QualityLevel = QualityLevel.MEDIUM

    def __post_init__(self):
        """
        Ajusta o threshold baseado no nível de qualidade.
        """
        self.min_score_threshold = self.quality_level.value
