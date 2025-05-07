# 🟪 Hexadecimal em ROM Hacking e Retrocomputação

> :us: [English version](hexadecimal.md)

## O que é Hexadecimal?
Hexadecimal (base-16) é um sistema numérico posicional que utiliza dezesseis símbolos distintos: 0-9 para os valores de zero a nove e A-F (ou a-f) para os valores de dez a quinze. Em ciência da computação e sistemas digitais, o hexadecimal fornece uma representação amigável para humanos de valores codificados em binário, já que cada dígito hex representa exatamente quatro bits binários.

## Importância Técnica do Hexadecimal
- **Mapeamento direto para o binário:** Cada dígito hexadecimal representa um nibble (4 bits), então dois dígitos hex representam um byte completo (8 bits). Isso o torna ideal para expressar endereços de memória, opcodes e dados brutos.
- **Inspeção eficiente de dados:** A notação hexadecimal é padrão em depuradores, disassemblers e editores hexadecimais para examinar e modificar arquivos binários, dumps de memória e imagens de ROM.
- **Universal em baixo nível:** O hexadecimal é a linguagem comum para assembly, análise de firmware, patching e engenharia reversa.

## Nomenclatura & Notação
- **Prefixo:** `0x` (ex: `0x1A3F`), ou `$` em alguns assemblers (ex: `$1A3F`)
- **Sufixo:** `h` (ex: `1A3Fh`)
- **Agrupamento:** Frequentemente agrupado em bytes (2 dígitos), words (4 dígitos) ou longwords (8 dígitos)
- **Case-insensitive:** `0x1a3f` é equivalente a `0x1A3F`

## Exemplos Ampliados
- **Valor de byte:** Decimal 255 = Hex `0xFF` = Binário `11111111`
- **Endereço 16 bits:** `0x8000` (usado como endereço de memória em muitos sistemas 8/16 bits)
- **Codificação de instrução:** O opcode para NOP (No Operation) em algumas CPUs é `0xEA`
- **Assinatura de arquivo (magic number):** Arquivos PNG começam com `89 50 4E 47` (`0x89504E47`)
- **Ponteiro:** Um ponteiro de 24 bits pode ser armazenado como `34 12 00` (little-endian para `0x001234`)
- **Paleta:** Uma cor em RGB565: `0x7E0` (verde puro; paleta é uma tabela de cores usada por gráficos)

## Técnicas
- **Editores hexadecimais:** Ferramentas como HxD, Hex Workshop ou MadEdit permitem inspeção e modificação direta de dados binários.
- **Busca de padrões:** Procure por magic numbers, ponteiros ou codificações de texto conhecidas em ROMs e executáveis.
- **Patch direto:** Modifique código, gráficos (tiles, paletas) ou texto editando suas representações hexadecimais.

## Fórmulas
- **Decimal para hex:** `hex(4660)` → `0x1234`
- **Hex para decimal:** `int('1A3F', 16)` → `6719`
- **Operações bit a bit:** `0xF0 & 0x0F = 0x00`
- **Extração de nibbles:** Nibble alto: `(byte & 0xF0) >> 4`, Nibble baixo: `byte & 0x0F`

## Uso em ROM Hacking
- **Ponteiros:** Armazenados como 2, 3 ou 4 bytes em hex, referenciando locais na memória ou arquivos.
- **Codificações de texto:** ASCII, Shift-JIS ou tabelas customizadas, todas representadas em hex.
- **Gráficos:** Tiles (blocos de pixels) e paletas (tabelas de cores) são manipulados em hex.
- **Compressão:** Headers e blocos de dados identificados por padrões hexadecimais.
- **Magic numbers:** Sequências hex únicas que identificam tipos de arquivo ou estruturas de dados.

## Exemplos de Consoles
- **NES:** Usa endereços hexadecimais para mapeamento de memória (ex: `0x8000` para PRG ROM).
- **SNES:** Gráficos e paletas de cor são armazenados em hex, ex: `0x7FFF` para branco em BGR555.
- **Mega Drive/Genesis:** Endereços de ROM/RAM, dados de tile e entradas de paleta são todos em hex.
- **PlayStation:** Sistema de arquivos, ponteiros e blocos de dados comprimidos são baseados em hex.

## Leitura adicional
- [Wikipedia: Hexadecimal](https://pt.wikipedia.org/wiki/Hexadecimal)
- [Hex Editors para ROM Hacking (romhacking.net)](https://www.romhacking.net/utilities/)

---

## Tópicos Relacionados
- [Magic Numbers](magic_numbers.md)
- [Ponteiros](pointers.md)
- [Compressão](compression.md)
- [Tabelas de Caracteres](character_tables.md)
