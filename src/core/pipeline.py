from config.pipeline_config import PipelineConfig
from modules import TextBlockExtractor
from modules import EntropyFilter
from modules import PrintableRatioFilter
from modules import CompressionRatioFilter
from datatypes.text_candidate import TextCandidate
from pathlib import Path
from typing import List, Optional


class TextExtractionPipeline:
    """
    Pipeline principal para extração de texto de arquivos binários.
    Implementa um sistema híbrido que combina análise de entropia, costura de contexto e filtragem inteligente.
    """

    def __init__(self, config: Optional[PipelineConfig] = None):
        self.config = config or PipelineConfig()
        self._setup_processors()
        self._setup_filters()

    def _setup_processors(self):
        self.text_extractor = TextBlockExtractor(
            min_block_size=20,
            text_likeness_threshold=0.8,
            window_size=16,
        )

    def _setup_filters(self):
        self.filters = [
            EntropyFilter(
                min_entropy=self.config.min_entropy,
                max_entropy=self.config.max_entropy,
            ),
            PrintableRatioFilter(
                min_printable_ratio=self.config.min_printable_ratio,
            ),
            CompressionRatioFilter(
                max_compression_ratio=self.config.max_compression_ratio
            ),
        ]

    def _apply_filters(
        self, candidates: List[TextCandidate]
    ) -> List[TextCandidate]:
        """
        Aplica todos os filtros de qualidade aos candidatos.
        Se um candidato atingir um score muito alto (ex: >= 3.5), ele é aprovado diretamente (bypass do NLP).
        """
        # self.progress.update(task, total=int(len(candidates)), visible=True)
        # self.progress.start_task(task)

        scored_candidates = []
        for candidate in candidates:
            if not candidate.raw_bytes or len(candidate.raw_bytes) == 0:
                continue

            total_score = 0.0
            for filter_obj in self.filters:
                total_score += filter_obj.filter(candidate)
            candidate.quality_score = total_score

            if total_score >= 3.5:
                scored_candidates.append(candidate)
                continue

            if total_score >= self.config.min_score_threshold:
                scored_candidates.append(candidate)

            # if candidate in scored_candidates:
            #     self.progress.update(task, advance=1)
        return scored_candidates

    def process_file(self, filepath: Path) -> List[TextCandidate]:
        """
        Processa um arquivo completo através do pipeline.
        Args:
            filepath: Caminho para o arquivo a ser processado
        Returns:
            Lista de candidatos de texto extraídos (sem NLP)
        """
        if not filepath.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {filepath}")

        with open(filepath, "rb") as f:
            file_data = f.read()

        text_blocks = self.text_extractor.process(file_data)

        final_candidates = self._apply_filters(text_blocks)

        return final_candidates
