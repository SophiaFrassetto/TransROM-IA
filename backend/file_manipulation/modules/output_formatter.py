import os
import shutil
from datetime import datetime
from datatypes.text_candidate import TextCandidate
from typing import List


class OutputFormatter:
    """
    Formatador de saída para os resultados do pipeline.
    Permite formatar e salvar resultados em arquivos, com sistema de backup automático.
    """

    @staticmethod
    def format_results(candidates: List[TextCandidate]) -> str:
        """
        Formata os resultados em uma tabela legível.
        Args:
            candidates: Lista de candidatos para formatar
        Returns:
            String formatada com os resultados
        """
        if not candidates:
            return "Nenhum candidato de texto encontrado."
        header = "{:<14} | {:<10} | {:<12} | {:<12} | {:<50} | {}".format(
            "Offset (Hex)",
            "Tamanho",
            "Idioma",
            "Perplexidade",
            "Prévia Hex (primeiros 16 bytes)",
            "Texto Decodificado (ASCII, com erros)",
        )
        separator = (
            "-" * 14
            + "-|-"
            + "-" * 10
            + "-|-"
            + "-" * 12
            + "-|-"
            + "-" * 12
            + "-|-"
            + "-" * 50
            + "-|-"
            + "-" * 50
        )
        lines = [header, separator]
        for candidate in candidates:
            offset_str = f"0x{candidate.start_offset:010X}"
            size_str = str(candidate.size)
            lang_str = getattr(candidate, "language", "?")
            perplexity_str = (
                f"{candidate.perplexity:.2f}"
                if candidate.perplexity is not None
                else "-"
            )
            hex_preview = candidate.hex_preview
            decoded_text = candidate.text_content.replace("\n", " ").replace("\r", "")
            line = "{:<14} | {:<10} | {:<12} | {:<12} | {:<50} | {}".format(
                offset_str,
                size_str,
                lang_str,
                perplexity_str,
                hex_preview,
                decoded_text,
            )
            lines.append(line)
        return "\n".join(lines)

    @staticmethod
    def _backup_if_exists(filepath: str):
        """
        Se o arquivo já existe, faz backup com timestamp antes de sobrescrever.
        Nunca sobrescreve backups antigos.
        """
        if os.path.exists(filepath):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"{filepath}.bak_{timestamp}"
            # Garante que não sobrescreve backups antigos
            while os.path.exists(backup_path):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                backup_path = f"{filepath}.bak_{timestamp}"
            shutil.move(filepath, backup_path)

    @staticmethod
    def save_results(
        candidates: List[TextCandidate],
        base_name: str,
        suffix: str = "",
        ext: str = ".txt",
        output_dir: str = ".",
    ) -> str:
        """
        Salva os resultados em um arquivo com nome legível e faz backup se necessário.
        Nunca sobrescreve arquivos antigos: sempre faz backup antes de salvar.
        Args:
            candidates: Lista de candidatos para salvar
            base_name: Nome base do arquivo (ex: nome do arquivo de entrada)
            suffix: Sufixo para diferenciar tipos de saída (ex: _no_NLP, _NLP, _rejected)
            ext: Extensão do arquivo (padrão: .txt)
            output_dir: Diretório onde salvar o arquivo e backups (padrão: atual)
        Returns:
            Caminho do arquivo salvo
        """
        safe_base = os.path.splitext(os.path.basename(base_name))[0]
        filename = f"{safe_base}{suffix}{ext}"
        full_path = os.path.join(output_dir, filename)
        OutputFormatter._backup_if_exists(full_path)
        content = OutputFormatter.format_results(candidates)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        return full_path
