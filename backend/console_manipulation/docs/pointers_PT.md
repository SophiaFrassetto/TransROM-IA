# 🟦 Ponteiros em ROM Hacking e Retrocomputação

> :us: [English version](pointers.md)

## O que é um Ponteiro?
Um ponteiro é um valor de dado que representa um endereço de memória ou um offset dentro de um arquivo ou espaço de memória. Em sistemas digitais, ponteiros são usados para referenciar a localização de dados, código ou recursos, permitindo acesso dinâmico e estruturas de dados flexíveis.

## Importância Técnica dos Ponteiros
- **Referência de dados:** Ponteiros permitem que programas e estruturas de dados referenciem outros locais, viabilizando tabelas, listas encadeadas e conteúdo dinâmico.
- **Estrutura de ROMs e arquivos:** Muitos formatos binários usam ponteiros para organizar blocos de dados, textos, gráficos e scripts.
- **Engenharia reversa:** Entender ponteiros é essencial para extrair, realocar ou modificar dados em ROMs e executáveis.

## Nomenclatura & Notação
- **Ponteiro absoluto:** Armazena um endereço completo (ex: `0x00123456`)
- **Ponteiro relativo:** Armazena um offset a partir de uma base conhecida (ex: `0x00002000` a partir do início do arquivo)
- **Endianness:** Ordem dos bytes em ponteiros multi-byte (little-endian = byte menos significativo primeiro; big-endian = mais significativo primeiro)
- **Tabela de ponteiros:** Bloco contíguo de ponteiros, geralmente usado para listas de dados ou blocos de texto.

## Exemplos Ampliados
- **Ponteiro de 4 bytes (little-endian):** `56 34 12 00` → `0x00123456`
- **Ponteiro de 3 bytes:** `34 12 00` → `0x001234`
- **Ponteiro relativo:** Offset `0x200` a partir da base `0x8000` aponta para `0x8200`
- **Tabela de ponteiros:** Sequência de endereços: `00 10 00 08`, `20 20 00 08`, ...

## Técnicas
- **Busca de ponteiros:** Procurar valores que correspondam a padrões conhecidos de endereços ou offsets
- **Identificação de tabelas de ponteiros:** Detectar blocos de ponteiros consecutivos
- **Patch de ponteiros:** Atualizar ponteiros ao mover ou expandir dados
- **Conversão de endianness:** Converter entre little-endian e big-endian conforme necessário.

## Fórmulas
- **Little-endian para endereço:** `endereco = b0 + (b1 << 8) + (b2 << 16) + (b3 << 24)`
- **Cálculo de ponteiro relativo:** `alvo = base + offset`
- **Stride de tabela de ponteiros:** Distância em bytes entre ponteiros consecutivos (geralmente 2, 3 ou 4)

## Uso em ROM Hacking
- **Extração de texto:** Localizar e seguir ponteiros para blocos de texto
- **Gráficos e assets:** Sprites, tiles e paletas geralmente são referenciados por ponteiros
- **Sistemas de script/eventos:** Lógica ramificada e data-driven usa ponteiros para controle de fluxo
- **Expansão de ROM:** Atualizar ponteiros ao adicionar ou mover dados

## Exemplos de Consoles
- **NES:** Usa ponteiros de 2 bytes para tabelas de salto e texto
- **SNES:** Ponteiros de 3 bytes para endereçamento de ROMs grandes
- **PlayStation:** Ponteiros de 4 bytes para sistemas de arquivos e blocos de dados
- **Mega Drive:** Ponteiros para gráficos, músicas e código

## Leitura adicional
- [Wikipedia: Ponteiro (computação)](https://pt.wikipedia.org/wiki/Ponteiro_(computa%C3%A7%C3%A3o))
- [Romhacking.net - Tutoriais de Ponteiros](https://www.romhacking.net/documents/)

---

## Tópicos Relacionados
- [Hexadecimal](hexadecimal_PT.md)
- [Magic Numbers](magic_numbers_PT.md)
- [Compressão](compression_PT.md)
- [Tabelas de Caracteres](character_tables_PT.md)
