import argparse
import os
from datatypes.enums import QualityLevel
from pathlib import Path


def get_args():
    parser = argparse.ArgumentParser(
        description="Pipeline Híbrido de Extração de Texto - TransROM-IA",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "filepath",
        type=str,
        help="Caminho para o arquivo binário a ser analisado"
    )

    parser.add_argument(
        "--output",
        "-o",
        default=os.path.join(os.path.dirname(__file__), "..", "output"),
        type=str,
        help="Caminho para o output",
    )

    parser.add_argument(
        "--quality_level",
        "-q",
        choices=["low", "medium", "high", "ultra"],
        default="medium",
        type=str,
        help="Nível de qualidade para filtragem (padrão: medium)",
    )

    parser.add_argument(
        "--min_printable_ratio",
        "-ptr",
        default=0.5,
        type=float,
        help="",
    )
    parser.add_argument(
        "--min_score_threshold",
        "-mst",
        default=0.2,
        type=float,
        help="",
    )
    parser.add_argument(
        "--max_compression_ratio",
        "-mcr",
        default=0.75,
        type=float,
        help="",
    )
    parser.add_argument(
        "--min_entropy",
        "-mne",
        default=4.0,
        type=float,
        help="",
    )
    parser.add_argument(
        "--max_entropy",
        "-mxe",
        default=5.5,
        type=float,
        help="",
    )

    quality_map = {
        "low": QualityLevel.LOW,
        "medium": QualityLevel.MEDIUM,
        "high": QualityLevel.HIGH,
        "ultra": QualityLevel.ULTRA,
    }

    args = parser.parse_args()
    args.quality_level = quality_map[args.quality_level]
    filepath_normalize = os.path.abspath(os.path.normpath(args.filepath))
    filepath = Path(filepath_normalize)
    args.filepath = filepath

    output_dir = Path(os.path.abspath(args.output))
    output_dir.mkdir(parents=True, exist_ok=True)
    args.output = output_dir

    return args