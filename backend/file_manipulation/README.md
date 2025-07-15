# Backend: file_manipulation

Este diretório contém o núcleo do pipeline de extração de texto binário do projeto TransROM-IA.

## Estrutura
- `core/`: Abstrações, pipeline principal e orquestrador.
- `modules/`: Implementações concretas de processadores, filtros e pós-processadores.
- `datatypes/`: Dataclasses centrais (Chunk, TextCandidate, etc).
- `utils/`: Utilitários, decoradores, analisadores, etc.
- `config/`: Configurações (ex: logging).
- `cli/`: Interface de linha de comando para rodar o pipeline.
- `tests/`: Testes unitários e de integração.
- `scripts/`: Scripts auxiliares.
- `output/`: Todos os resultados e backups de execuções do pipeline.

## Como rodar o pipeline

```bash
cd backend/file_manipulation
python -m cli.main arquivo.bin [opções]
```

Veja as opções disponíveis com:
```bash
python -m cli.main --help
```

## Saída dos resultados
- Todos os arquivos de saída são salvos na pasta `output/`.
- **Nunca há sobrescrita de arquivos antigos**: se um arquivo já existe, ele é movido para backup com timestamp antes de salvar o novo.
- O padrão de nomes é:
  - `<nome>_<quality>_no_NLP.txt` (resultado sem NLP)
  - `<nome>_<quality>_<modelo>_<threshold>_<minlen>_NLP.txt` (resultado com NLP)
  - `<nome>_<quality>_<modelo>_<threshold>_<minlen>_NLP_rejected.txt` (rejeitados pelo NLP)
  - Backups: `.bak_<timestamp>`

## Modularidade
- Cada filtro/processador está em seu próprio arquivo.
- Fácil de estender: basta criar um novo módulo em `modules/` e registrar no pipeline.

## Referências
- Veja também o README em `backend/` para visão geral do backend. 