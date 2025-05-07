# 🟧 Números Mágicos em Computação e ROM Hacking

> :us: [English version](magic_numbers.md)

## O que é um Número Mágico?
Um número mágico é uma constante ou sequência única de bytes embutida em um arquivo, estrutura de dados ou região de memória para identificar seu tipo, formato ou significado especial. Números mágicos são amplamente usados como assinaturas de arquivo (valores únicos no início de um arquivo), marcadores de formato e códigos de validação em sistemas digitais.

## Importância Técnica dos Números Mágicos
- **Identificação de arquivos:** Muitos formatos de arquivo começam com um número mágico para distingui-los de outros.
- **Validação de dados:** Números mágicos ajudam a detectar corrupção, tipos de arquivo incorretos ou estruturas de dados inválidas.
- **Engenharia reversa:** Reconhecer números mágicos é essencial para analisar, extrair ou modificar arquivos binários e ROMs.

## Nomenclatura & Notação
- **Assinatura de arquivo:** O número mágico no início de um arquivo, usado para identificar rapidamente o tipo de arquivo.
- **Header:** Bloco inicial de dados contendo o número mágico e metadados.
- **Endianness:** Números mágicos podem aparecer diferentes dependendo da ordem dos bytes (little-endian ou big-endian).

## Exemplos Ampliados
- **Imagem PNG:** Começa com `89 50 4E 47 0D 0A 1A 0A` (`0x89504E470D0A1A0A`)
- **Arquivo ZIP:** Começa com `50 4B 03 04` (`0x504B0304`)
- **Executável ELF:** Começa com `7F 45 4C 46` (`0x7F454C46`)
- **Formato de ROM:** Muitas ROMs têm números mágicos ou headers únicos (ex: NES: `4E 45 53 1A` para iNES)
- **Blocos customizados:** Headers de compressão, marcadores de tabela, etc.

## Técnicas
- **Inspeção em hexadecimal:** Use editores hexadecimais para localizar e reconhecer números mágicos em arquivos.
- **Busca de padrões:** Procure por números mágicos conhecidos para identificar tipos de arquivo ou blocos de dados.
- **Bancos de assinaturas:** Use ou construa listas de números mágicos para detecção automatizada.

## Uso em ROM Hacking
- **Validação de arquivos:** Garantir o tipo correto de ROM ou asset antes de processar.
- **Extração de dados:** Localizar e extrair blocos por seus números mágicos.
- **Conversão de formatos:** Identificar e converter entre formatos usando assinaturas.

## Exemplos de Consoles
- **NES:** Header iNES: `4E 45 53 1A`
- **SNES:** Header SMC: `AA BB 04 00` (nem sempre presente)
- **PlayStation:** CD-ROMs começam com `CD001` no descritor ISO9660
- **Game Boy:** Logo da Nintendo no header atua como número mágico

## Leitura adicional
- [Wikipedia: Magic number (programação)](https://pt.wikipedia.org/wiki/N%C3%BAmero_m%C3%A1gico_(programa%C3%A7%C3%A3o))
- [Tabela de Assinaturas de Arquivo](https://www.garykessler.net/library/file_sigs.html)

---

## Tópicos Relacionados
- [Hexadecimal](hexadecimal_PT.md)
- [Ponteiros](pointers_PT.md)
- [Compressão](compression_PT.md)
- [Tabelas de Caracteres](character_tables_PT.md)
