from dataclasses import dataclass
from datatypes.enums import QualityLevel
from rich.console import Console


@dataclass
class PipelineConfig:
    """
    Configuração do pipeline de processamento.
    Permite ajustar chunk_size, thresholds e nível de qualidade.
    """

    min_printable_ratio: float = 0.5
    min_score_threshold: float = 2.0
    max_compression_ratio: float = 0.75
    min_entropy: float = 4.0,
    max_entropy: float = 5.5
    quality_level: QualityLevel = QualityLevel.MEDIUM

    console: Console = Console()

    def __post_init__(self):
        """
        Ajusta o threshold baseado no nível de qualidade.
        """
        self.min_score_threshold = self.quality_level.value
