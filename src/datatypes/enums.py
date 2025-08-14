from enum import Enum


class QualityLevel(Enum):
    """
    Níveis de qualidade para filtragem.
    """

    LOW = 1.0
    MEDIUM = 2.0
    HIGH = 3.0
    ULTRA = 4.0
