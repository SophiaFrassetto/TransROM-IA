from .pipeline import TextExtractionPipeline
from config.pipeline_config import PipelineConfig
from typing import Optional, Dict, Any


class PipelineOrchestrator:
    """
    Orquestrador central para pipelines de extração de texto.
    Permite compor, configurar e executar diferentes pipelines e fluxos.
    Ideal para integração com API, CLI ou outros sistemas.
    """

    def __init__(self, config: Optional[PipelineConfig] = None):
        self.config = config or PipelineConfig()
        self.pipeline = TextExtractionPipeline(self.config)
        # Futuro: permitir múltiplos pipelines, customização dinâmica, etc.

    def run(self, filepath: str, extra_args: Optional[Dict[str, Any]] = None):
        """
        Executa o pipeline principal para o arquivo informado.
        Args:
            filepath: Caminho do arquivo a ser processado
            extra_args: argumentos extras para customização futura
        Returns:
            Lista de candidatos de texto extraídos
        """
        return self.pipeline.process_file(filepath)
