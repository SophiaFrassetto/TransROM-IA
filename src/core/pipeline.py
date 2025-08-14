from core.base_config import PipelineConfig
from modules import TextBlockExtractor
from modules import EntropyFilter
from modules import PrintableRatioFilter
from modules import CompressionRatioFilter
from datatypes.text_candidate import TextCandidate
from pathlib import Path
from typing import List, Optional, Union

from rich.progress import (
    BarColumn,
    Progress,
    TextColumn,
    TimeRemainingColumn,
    MofNCompleteColumn,
    TimeElapsedColumn,
)

from rich.panel import Panel


class TextExtractionPipeline:
    """
    Pipeline principal para extração de texto de arquivos binários.
    Implementa um sistema híbrido que combina análise de entropia, costura de contexto e filtragem inteligente.
    """

    def __init__(self, config: Optional[PipelineConfig] = None, console=None):
        self.config = config or PipelineConfig()
        self._setup_processors()
        self._setup_filters()

        self.console = console

        self.progress = PipelineProgress(
            TextColumn("[bold blue]{task.description}: {task.fields[filename]}", justify="right"),
            BarColumn(),
            "[progress.percentage]{task.percentage:>3.1f}%",
            "•",
            TimeRemainingColumn(),
            "•",
            TimeElapsedColumn(),
            "•",
            MofNCompleteColumn(),
            console=console
        )

    def _setup_processors(self):
        self.text_extractor = TextBlockExtractor()

    def _setup_filters(self):
        self.filters = [
            EntropyFilter(),
            PrintableRatioFilter(),
            CompressionRatioFilter(),
        ]

    def _apply_filters(self, candidates: List[TextCandidate], task) -> List[TextCandidate]:
        """
        Aplica todos os filtros de qualidade aos candidatos.
        Se um candidato atingir um score muito alto (ex: >= 3.5), ele é aprovado diretamente (bypass do NLP).
        """
        self.progress.update(task, total=int(len(candidates)), visible=True)
        self.progress.start_task(task)
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
            if candidate in scored_candidates:
                self.progress.update(task, advance=1)
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
        with open(filepath, "rb") as f:
            file_data = f.read()
        with self.progress:

            task_text_extractor = self.progress.add_task("Text Extractor", filename=filepath.stem, start=False, visible=False)
            task_apply_filters = self.progress.add_task("apply_filters", filename=filepath.stem, start=False, visible=False)

            text_blocks = self.text_extractor.process(file_data, task_text_extractor, self.progress)

            final_candidates = self._apply_filters(text_blocks, task_apply_filters)

            return final_candidates


class PipelineProgress(Progress):
    def get_renderables(self):
        yield Panel(self.make_tasks_table(self.tasks), title="[red]Pipeline")
