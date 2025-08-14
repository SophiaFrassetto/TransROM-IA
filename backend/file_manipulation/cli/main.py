import argparse
import os
from pathlib import Path
from config.logging_config import setup_logging
from core.orchestrator import PipelineOrchestrator
from core.enums import QualityLevel
from core.base_config import PipelineConfig
from utils.output_formatter import OutputFormatter
from rich.console import Console
from rich.table import Table


def main():
    """
    CLI principal para rodar o pipeline de extração de texto.
    """
    # Configuração global de logging
    setup_logging()

    parser = argparse.ArgumentParser(
        description="Pipeline Híbrido de Extração de Texto - TransROM-IA",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "filepath", help="Caminho para o arquivo binário a ser analisado"
    )
    parser.add_argument(
        "--quality",
        "-q",
        choices=["low", "medium", "high", "ultra"],
        default="medium",
        help="Nível de qualidade para filtragem (padrão: medium)",
    )

    console = Console()

    args = parser.parse_args()

    # Normaliza o caminho do arquivo para evitar problemas de path
    args.filepath = os.path.abspath(os.path.normpath(args.filepath))
    filepath = Path(args.filepath)

    # Cria a pasta de saída se não existir
    output_dir = os.path.join(os.path.dirname(__file__), "..", "output")
    output_dir = os.path.abspath(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    quality_map = {
        "low": QualityLevel.LOW,
        "medium": QualityLevel.MEDIUM,
        "high": QualityLevel.HIGH,
        "ultra": QualityLevel.ULTRA,
    }
    config = PipelineConfig(
        quality_level=quality_map[args.quality]
    )

    table = Table(show_header=True, header_style="bold magenta", title="TransRomIA")
    table.add_column("Rom")
    table.add_column("Directory")
    table.add_column("Extencion")
    table.add_column("Size")
    table.add_column("Output Directory")
    table.add_column("Quality")

    table.add_row(
        str(filepath.stem),
        str(filepath.parent.absolute()),
        str(filepath.suffix),
        f"{filepath.stat().st_size} B",
        str(output_dir),
        str(quality_map[args.quality].value),
    )

    console.print(table)

    orchestrator = PipelineOrchestrator(config, console)
    candidates = orchestrator.run(args.filepath)


    base_name = args.filepath
    suffix = f"_{args.quality}"
    OutputFormatter.save_results(
        candidates, base_name=base_name, suffix=suffix, output_dir=output_dir
    )

if __name__ == "__main__":
    main()
