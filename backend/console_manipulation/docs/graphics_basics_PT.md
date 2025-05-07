# 🟦 Fundamentos de Gráficos (Tiles & Paletas) em ROM Hacking

> :us: [English version](graphics_basics.md)

## O que são Tiles & Paletas?
- **Tiles:** Blocos pequenos e de tamanho fixo de dados de pixels (ex: 8x8 ou 16x16 pixels) usados para construir fundos, sprites e mapas em jogos retrô. Tiles são reutilizados para economizar espaço e criar imagens complexas de forma eficiente.
- **Paletas:** Tabelas de cores. Cada pixel em um tile se refere a um índice na paleta, permitindo representação compacta de cores e trocas fáceis de esquema de cores.

## Por que são importantes?
- **Eficiência de espaço:** Tiles e paletas permitem gráficos grandes e coloridos com uso mínimo de memória.
- **Edição:** Entender os formatos de tile e paleta é essencial para hacks de sprites, fontes e fundos.
- **ROM hacking:** Possibilita tradução de gráficos de texto, arte customizada e mods visuais.

## Formatos Típicos
- **Tamanho do tile:** 8x8 ou 16x16 pixels, 2bpp, 4bpp ou 8bpp (bits por pixel)
- **Tamanho da paleta:** 16 ou 256 cores, geralmente em formato RGB555 ou RGB565
- **Tilemaps:** Estruturas de dados que definem como os tiles são organizados na tela

## Exemplos
- **NES:** Tiles 8x8, 2bpp, paletas de 4 cores
- **SNES:** Tiles 8x8 ou 16x16, 4bpp, paletas de 16 cores
- **GBA:** Tiles 8x8, 4bpp ou 8bpp, paletas de 16 ou 256 cores
- **Mega Drive:** Tiles 8x8, 4bpp, paletas de 16 cores

## Uso em ROM Hacking
- **Edição de sprites:** Alterar gráficos ou animações de personagens
- **Hack de fontes:** Editar fontes do jogo para tradução
- **Fundos:** Redesenhar ou modificar fundos e interface
- **Troca de paletas:** Alterar esquemas de cores para novos efeitos

## Leitura adicional
- [Wikipedia: Tile-based video game](https://en.wikipedia.org/wiki/Tile-based_video_game)
- [Romhacking.net - Ferramentas de Gráficos](https://www.romhacking.net/utilities/)

---

## Tópicos Relacionados
- [Hexadecimal](hexadecimal_PT.md)
- [Ponteiros](pointers_PT.md)
- [Magic Numbers](magic_numbers_PT.md)
- [Compressão](compression_PT.md)
- [Tabelas de Caracteres](character_tables_PT.md)
