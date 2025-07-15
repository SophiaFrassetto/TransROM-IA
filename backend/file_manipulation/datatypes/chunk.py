from dataclasses import dataclass, field
import string


@dataclass
class Chunk:
    """
    Representa um chunk de dados binários.
    Inclui offset, bytes e score de textualidade.
    """

    offset: int
    bytes: bytes
    text_score: float = field(default=0.0, init=False)

    def __post_init__(self):
        """
        Calcula automaticamente o score de textualidade baseado em caracteres imprimíveis.
        """
        self.text_score = self._calculate_text_score()

    def _calculate_text_score(self) -> float:
        if not self.bytes:
            return 0.0
        printable_bytes = set(bytes(string.printable, "ascii"))
        printable_count = sum(1 for byte in self.bytes if byte in printable_bytes)
        return printable_count / len(self.bytes)
