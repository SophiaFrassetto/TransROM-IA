from abc import ABC, abstractmethod
from typing import Any


class QualityFilter(ABC):
    """
    Classe abstrata para filtros de qualidade do pipeline.
    Cada filtro deve implementar o método filter.
    """

    @abstractmethod
    def filter(self, candidate: Any) -> float:
        """
        Aplica o filtro e retorna um score de qualidade.
        """
        pass
