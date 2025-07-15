import argparse
import os
from ..config.logging_config import setup_logging
from ..core.orchestrator import PipelineOrchestrator
from ..modules.nlp_postprocessor import NLPPostProcessor
from ..core.enums import QualityLevel
from ..core.base_config import PipelineConfig
from ..modules.output_formatter import OutputFormatter


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
    parser.add_argument(
        "--chunk-size",
        "-c",
        type=int,
        default=32,
        help="Tamanho dos chunks em bytes (padrão: 32)",
    )
    parser.add_argument(
        "--nlp",
        action="store_true",
        help="Ativa o filtro NLP de perplexidade após o pipeline principal",
    )
    parser.add_argument(
        "--nlp-threshold",
        type=float,
        default=200.0,
        help="Limiar de perplexidade para o filtro NLP (padrão: 200.0)",
    )
    parser.add_argument(
        "--nlp-min-length",
        type=int,
        default=10,
        help="Tamanho mínimo do texto para aplicar o filtro NLP (padrão: 10)",
    )
    parser.add_argument(
        "--nlp-model",
        type=str,
        default="distilgpt2",
        help="Nome do modelo HuggingFace para o filtro NLP (ex: distilgpt2, gpt2, gpt2-medium, EleutherAI/gpt-neo-125M, bigscience/bloom-560m). Padrão: distilgpt2",
    )
    parser.add_argument(
        "--nlp-window-size",
        type=int,
        default=1024,
        help="Tamanho da janela de tokens para textos longos no filtro NLP (padrão: 1024). Textos maiores que isso são divididos em partes para evitar o limite do modelo.",
    )
    parser.add_argument(
        "--nlp-stride",
        type=int,
        default=1024,
        help="Stride (avanço) da janela de tokens para textos longos no filtro NLP (padrão: 1024, ou seja, sem sobreposição). Use valor menor para sobrepor as janelas.",
    )
    parser.add_argument(
        "--nlp-agg",
        type=str,
        choices=["mean", "min", "max"],
        default="mean",
        help="Como agregar perplexidades das janelas: mean (média aritmética, padrão), min (menor valor), max (maior valor). Média é mais estável.",
    )
    args = parser.parse_args()

    # Normaliza o caminho do arquivo para evitar problemas de path
    args.filepath = os.path.abspath(os.path.normpath(args.filepath))

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
        chunk_size=args.chunk_size, quality_level=quality_map[args.quality]
    )
    orchestrator = PipelineOrchestrator(config)
    candidates = orchestrator.run(args.filepath)

    # Salva resultado SEM NLP
    base_name = args.filepath
    suffix = f"_{args.quality}_no_NLP"
    output_file = OutputFormatter.save_results(
        candidates, base_name=base_name, suffix=suffix, output_dir=output_dir
    )
    print(f"Resultado SEM NLP salvo em: {output_file}")

    if args.nlp:
        nlp_processor = NLPPostProcessor(
            perplexity_threshold=args.nlp_threshold,
            min_length=args.nlp_min_length,
            model_id=args.nlp_model,
            window_size=args.nlp_window_size,
            stride=args.nlp_stride,
            agg=args.nlp_agg,
        )
        nlp_candidates, rejected = nlp_processor.filter(
            candidates, return_rejected=True
        )
        suffix_nlp = f"_{args.quality}_{args.nlp_model.replace('/', '_')}_{args.nlp_threshold}_{args.nlp_min_length}_NLP"
        output_file_nlp = OutputFormatter.save_results(
            nlp_candidates,
            base_name=base_name,
            suffix=suffix_nlp,
            output_dir=output_dir,
        )
        print(f"Resultado COM NLP salvo em: {output_file_nlp}")
        # (Opcional) Salvar rejeitados
        if rejected:
            suffix_rej = suffix_nlp + "_rejected"
            output_file_rej = OutputFormatter.save_results(
                rejected, base_name=base_name, suffix=suffix_rej, output_dir=output_dir
            )
            print(f"Candidatos rejeitados pelo NLP salvos em: {output_file_rej}")


if __name__ == "__main__":
    main()
