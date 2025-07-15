from dataclasses import dataclass, field


@dataclass
class TextCandidate:
    """
    Representa um candidato a texto extraído.
    Inclui offsets, bytes, score de qualidade, idioma e perplexidade.
    """

    start_offset: int
    end_offset: int
    raw_bytes: bytes
    quality_score: float = field(default=0.0, init=False)
    language: str = field(default="", init=False)
    perplexity: float = field(default=None, init=False)

    @property
    def size(self) -> int:
        """Retorna o tamanho do candidato em bytes."""
        return self.end_offset - self.start_offset

    @property
    def text_content(self) -> str:
        """Retorna o conteúdo decodificado como texto."""
        return self.raw_bytes.decode("ascii", errors="ignore")

    @property
    def hex_preview(self) -> str:
        """Retorna uma prévia hexadecimal dos primeiros 16 bytes."""
        return " ".join(f"{b:02X}" for b in self.raw_bytes[:16])
