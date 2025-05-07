# 🟧 Compressão em ROM Hacking e Retrocomputação

> :us: [English version](compression.md)

## O que é Compressão?
Compressão é o processo de codificar dados para reduzir seu tamanho, tornando o armazenamento e a transmissão mais eficientes. Em sistemas digitais, algoritmos de compressão transformam dados em uma representação mais compacta, geralmente removendo redundâncias ou codificando padrões de forma mais eficiente.

## Importância Técnica da Compressão
- **Otimização de armazenamento:** Permite que mais dados caibam em memória ou ROM limitada.
- **Performance:** Reduz tempos de carregamento e necessidade de banda.
- **Gestão de dados:** Facilita empacotamento, arquivamento e distribuição eficiente de assets.

## Nomenclatura & Notação
- **Algoritmo de compressão:** Método usado para comprimir dados (ex: LZ77, Huffman, RLE, LZSS; LZ77 e Huffman são comuns em jogos retrô)
- **Header:** Bytes iniciais indicando tipo e parâmetros de compressão.
- **Descompressão:** Processo de restaurar os dados originais a partir do formato comprimido.

## Exemplos Ampliados
- **LZ77:** Algoritmo baseado em dicionário; blocos comprimidos geralmente começam com header específico (ex: `0x10`)
- **Huffman:** Usa códigos de tamanho variável para símbolos frequentes
- **RLE (Run-Length Encoding):** Codifica repetições como pares (valor, contagem)
- **Formatos customizados:** Muitos jogos usam esquemas proprietários ou híbridos

## Técnicas
- **Detecção de blocos:** Identificar dados comprimidos por magic numbers ou headers
- **Ferramentas de descompressão:** Usar ou criar scripts para descomprimir e analisar dados
- **Recompressão:** Necessária para repack de assets modificados em ROMs
- **Engenharia reversa:** Analisar formatos desconhecidos estudando padrões e headers

## Uso em ROM Hacking
- **Extração de gráficos:** Tilesets, sprites e backgrounds geralmente são comprimidos
- **Blocos de texto:** Scripts e diálogos podem estar em formato comprimido
- **Reempacotamento de assets:** Dados modificados precisam ser recomprimidos para caber nas restrições originais
- **Conversão de formatos:** Converter entre formatos comprimidos e descomprimidos para edição

## Exemplos de Consoles
- **SNES:** Gráficos e mapas usam variantes de RLE ou LZ77
- **GBA:** Uso amplo de LZ77 e Huffman para gráficos e texto
- **PlayStation:** Diversos algoritmos customizados e padrões
- **Mega Drive:** Compressão para músicas, gráficos e dados de fase

## Leitura adicional
- [Wikipedia: Compressão de dados](https://pt.wikipedia.org/wiki/Compress%C3%A3o_de_dados)
- [GBATEK - BIOS Compression](https://problemkaputt.de/gbatek.htm#biosdecompressionfunctions)
- [Romhacking.net - Compression Tools](https://www.romhacking.net/utilities/)

---

## Tópicos Relacionados
- [Hexadecimal](hexadecimal_PT.md)
- [Ponteiros](pointers_PT.md)
- [Magic Numbers](magic_numbers_PT.md)
- [Tabelas de Caracteres](character_tables_PT.md)
