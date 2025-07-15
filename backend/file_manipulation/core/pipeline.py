from ..core.base_config import PipelineConfig
from ..core.enums import ProcessingStage
from ..modules.chunkifier import Chunkifier
from ..modules.context_stitcher import ContextStitcher
from ..modules.entropy_filter import EntropyFilter
from ..modules.printable_density_filter import PrintableDensityFilter
from ..modules.letter_ratio_filter import LetterRatioFilter
from ..modules.word_structure_filter import WordStructureFilter
from ..modules.stutter_penalty_filter import StutterPenaltyFilter
from ..modules.linear_sequence_filter import LinearSequenceFilter
from ..modules.repeated_block_filter import RepeatedBlockFilter
from ..modules.low_char_diversity_filter import LowCharDiversityFilter
from ..modules.dictionary_word_filter import DictionaryWordFilter
from ..datatypes.text_candidate import TextCandidate
from pathlib import Path
from typing import List, Optional, Union
import logging

logger = logging.getLogger(__name__)


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
        self.chunkifier = Chunkifier(self.config.chunk_size)
        self.stitcher = ContextStitcher(self.config.printable_threshold)

    def _setup_filters(self):
        self.filters = [
            EntropyFilter(),
            PrintableDensityFilter(),
            LetterRatioFilter(),
            WordStructureFilter(),
            StutterPenaltyFilter(),
            LinearSequenceFilter(),
            RepeatedBlockFilter(),
            LowCharDiversityFilter(),
            DictionaryWordFilter(),
        ]

    def _apply_filters(self, candidates: List[TextCandidate]) -> List[TextCandidate]:
        """
        Aplica todos os filtros de qualidade aos candidatos.
        Se um candidato atingir um score muito alto (ex: >= 3.5), ele é aprovado diretamente (bypass do NLP).
        """
        logger.info("Aplicando filtros de qualidade...")
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
        logger.info(
            f"Resultado: {len(scored_candidates)} candidatos sobreviveram à filtragem."
        )
        return scored_candidates

    def process_file(self, filepath: Union[str, Path]) -> List[TextCandidate]:
        """
        Processa um arquivo completo através do pipeline.
        Args:
            filepath: Caminho para o arquivo a ser processado
        Returns:
            Lista de candidatos de texto extraídos (sem NLP)
        """
        filepath = Path(filepath)
        if not filepath.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {filepath}")
        logger.info(f"Iniciando processamento do arquivo: {filepath}")
        with open(filepath, "rb") as f:
            file_data = f.read()
        chunks = self.chunkifier.process(file_data)
        stitched_candidates = self.stitcher.process(chunks)
        final_candidates = self._apply_filters(stitched_candidates)
        return final_candidates
