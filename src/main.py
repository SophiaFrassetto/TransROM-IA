import os
from pathlib import Path
from core.orchestrator import PipelineOrchestrator
from config.pipeline_config import PipelineConfig
from utils.output_formatter import OutputFormatter
from rich.console import Console
from rich.table import Table

from config import get_args


def generate_initial_table(args, console):
    table = Table(show_header=True, header_style="bold magenta", title="TransRomIA")
    table.add_column("Rom")
    table.add_column("Directory")
    table.add_column("Extencion")
    table.add_column("Size")
    table.add_column("Output Directory")
    table.add_column("Quality")

    table.add_row(
        str(args.filepath.stem),
        str(args.filepath.parent.absolute()),
        str(args.filepath.suffix),
        f"{args.filepath.stat().st_size} B",
        str(args.output),
        str(args.quality_level.value),
    )

    console.print(table)


def main():
    """
    CLI principal para rodar o pipeline de extração de texto.
    """
    args = get_args()
    config = PipelineConfig(
        min_printable_ratio = args.min_printable_ratio,
        min_score_threshold = args.min_score_threshold,
        max_compression_ratio = args.max_compression_ratio,
        min_entropy = args.min_entropy,
        max_entropy = args.max_entropy,
        quality_level = args.quality_level
    )

    generate_initial_table(args, config.console)

    orchestrator = PipelineOrchestrator(config)
    candidates = orchestrator.run(args.filepath)

    OutputFormatter.save_results(
        candidates, base_name=args.filepath, suffix=f"_{args.quality_level.value}", output_dir=(args.output)
    )


if __name__ == "__main__":
    main()
