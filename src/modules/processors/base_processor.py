from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    """
    Classe abstrata para processadores de dados do pipeline.
    Cada processador deve implementar o método process.
    """

    @abstractmethod
    def process(self, data: Any) -> Any:
        """
        Processa os dados e retorna o resultado.
        """
        pass
