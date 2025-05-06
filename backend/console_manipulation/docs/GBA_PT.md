# 📚 Game Boy Advance (GBA) - Guia Técnico de Referência

> **Este documento compila informações essenciais sobre o hardware do Game Boy Advance (GBA), memória, estrutura da ROM, ponteiros, tabelas de caracteres, compressão e mais, com foco em engenharia reversa, tradução e desenvolvimento de ferramentas próprias.**

---

## Índice

1. [Visão Geral](#visão-geral)
2. [Hardware](#hardware)
   - [CPU](#cpu)
   - [Memória](#memória)
   - [Mapa de Memória](#mapa-de-memória)
   - [Gráficos & Vídeo](#gráficos--vídeo)
   - [Áudio](#áudio)
   - [Entradas & Periféricos](#entradas--periféricos)
3. [ROMs & Espaço de Memória](#roms--espaço-de-memória)
   - [Tamanho Máximo da ROM](#tamanho-máximo-da-rom)
   - [Estrutura da ROM](#estrutura-da-rom)
4. [Ponteiros & Endereçamento](#ponteiros--endereçamento)
5. [Tabelas de Caracteres](#tabelas-de-caracteres)
   - [ASCII, Shift-JIS e Tabelas Customizadas](#ascii-shift-jis-e-tabelas-customizadas)
   - [Como Encontrar e Montar Tabelas](#como-encontrar-e-montar-tabelas)
6. [Compressão & Descompressão](#compressão--descompressão)
   - [Formatos Comuns (LZ77, Huffman, etc.)](#formatos-comuns-lz77-huffman-etc)
   - [Ferramentas & Dicas](#ferramentas--dicas)
7. [Tecnologias & Ferramentas de Desenvolvimento](#tecnologias--ferramentas-de-desenvolvimento)
8. [Links & Referências](#links--referências)

---

## Visão Geral

O Game Boy Advance (GBA) é um console portátil lançado pela Nintendo em 2001, com CPU ARM7TDMI de 32 bits. É conhecido por sua flexibilidade gráfica, som estéreo e vasta biblioteca de jogos. O GBA é popular nas comunidades de ROM hacking e homebrew devido à sua arquitetura acessível e documentação extensa.

---

## Hardware

### CPU
- **Processador:** ARM7TDMI (RISC 32 bits)
- **Frequência:** 16,78 MHz
- **Conjuntos de Instruções:** ARM (32 bits), Thumb (16 bits)
- [Referência ARM7TDMI](https://developer.arm.com/documentation/ddi0210/c/)

### Memória
- **WRAM (RAM de trabalho):** 256 KB (externa) + 32 KB (interna)
- **VRAM (RAM de vídeo):** 96 KB
- **OAM (Object Attribute Memory):** 1 KB (para sprites)
- **Palette RAM:** 1 KB (512 bytes BG + 512 bytes OBJ)
- **ROM:** Até 32 MB (256 Mbit)
- **SRAM/Flash/EEPROM:** Até 64 KB (para saves, varia por cartucho)

### Mapa de Memória

| Endereço Inicial | Tamanho   | Descrição                |
|------------------|-----------|--------------------------|
| 0x00000000       | 32 KB     | BIOS                     |
| 0x02000000       | 256 KB    | WRAM externa             |
| 0x03000000       | 32 KB     | WRAM interna             |
| 0x04000000       | 1 KB      | Registradores de I/O     |
| 0x05000000       | 1 KB      | Palette RAM              |
| 0x06000000       | 96 KB     | VRAM                     |
| 0x07000000       | 1 KB      | OAM                      |
| 0x08000000       | até 32 MB | ROM/FlashROM do cartucho |
| 0x0E000000       | 64 KB     | SRAM do cartucho         |

- [GBATEK - Mapa de Memória](https://problemkaputt.de/gbatek.htm#gbamemorymap)

### Gráficos & Vídeo
- **Resolução:** 240x160 pixels
- **Profundidade de cor:** 15 bits (BGR555), 32.768 cores possíveis, 512 na tela
- **Modos gráficos:** 6 modos (0-5), combinando BGs tileados e bitmaps
- **Sprites:** Até 128, tamanhos variados
- [Tonc - Hardware Gráfico do GBA](https://www.coranac.com/tonc/text/hardware.htm)

### Áudio
- **Canais:** 6 (2 PSG, 2 Direct Sound, 2 Wave)
- **Som estéreo**
- **Mixagem via hardware**

### Entradas & Periféricos
- **Botões:** A, B, L, R, Start, Select, D-Pad
- **Cabo Link:** Comunicação serial entre GBAs
- **Cartuchos especiais:** RTC, sensores, rumble, etc.

---

## ROMs & Espaço de Memória

### Tamanho Máximo da ROM
- **Limite teórico:** 32 MB (256 Mbit)
- **Tamanhos comuns:** 4 MB, 8 MB, 16 MB

### Estrutura da ROM
- **Header:** Informações do jogo, logo da Nintendo, checksum, etc.
- **Dados do jogo:** Código, gráficos, textos, tabelas, scripts, etc.
- [GBATEK - Game Pak ROM](https://problemkaputt.de/gbatek.htm#gbacartridges)

---

## Ponteiros & Endereçamento
- **Ponteiros** são valores (geralmente 3 ou 4 bytes) que indicam endereços na ROM ou RAM.
- **Endereçamento absoluto:** Ponteiros que apontam para endereços fixos (ex: 0x08000000 + offset)
- **Endereçamento relativo:** Ponteiros que usam um offset a partir de uma base conhecida.
- **Endianess:** GBA usa little-endian (ex: ponteiro 0x12 0x34 0x56 0x08 → endereço 0x08563412)

---

## Tabelas de Caracteres

### ASCII, Shift-JIS e Tabelas Customizadas
- **ASCII:** Usado em jogos ocidentais, 1 byte por caractere.
- **Shift-JIS:** Usado em jogos japoneses, 1-2 bytes por caractere.
- **Tabelas customizadas:** Jogos podem usar mapeamentos próprios (ex: 0x80 = 'A', 0x81 = 'B', etc.)

### Como Encontrar e Montar Tabelas
- **Ferramentas:** WindHex, MadEdit, Cartographer, Atlas, Hex Workshop
- **Processo:** Localize textos na ROM, identifique padrões, crie um arquivo .tbl mapeando bytes para caracteres.
- [Tutorial de Tabelas](http://www.loirak.com/gameboy/gbatutor.php)

---

## Compressão & Descompressão

### Formatos Comuns (LZ77, Huffman, etc.)
- **LZ77:** Muito usado no GBA (ex: gráficos, textos comprimidos)
- **Huffman:** Usado em alguns jogos para textos
- **RLE, LZSS, LZ78:** Outros formatos possíveis

### Ferramentas & Dicas
- **Ferramentas:** GBA Graphics Editor, NLZ-GBA Advance, GBA Tool Advance, unLZ-GBA
- **Dica:** Blocos LZ77 geralmente começam com 0x10

---

## Tecnologias & Ferramentas de Desenvolvimento
- **Compiladores:** [devkitARM](https://devkitpro.org/), [gba-toolchain](https://github.com/devkitPro/gba-toolchain)
- **Emuladores:** [mGBA](https://mgba.io/), [No$GBA](https://problemkaputt.de/gba.htm), [NanoBoyAdvance](https://github.com/nba-emu/NanoBoyAdvance)
- **Toolkits:** [Butano](https://github.com/GValiente/Butano), [libtonc](https://www.coranac.com/tonc/)
- **Documentação:** [GBATEK](https://problemkaputt.de/gbatek.htm), [Tonc](https://www.coranac.com/tonc/)
- **Comunidade:** [GBAdev Discord](https://discord.gg/gbadev), [GBAdev Forum](https://forum.gbadev.net/)
- **Listas de recursos:** [awesome-gbadev](https://github.com/gbadev-org/awesome-gbadev)

---

## Links & Referências
- [awesome-gbadev (curadoria de recursos)](https://github.com/gbadev-org/awesome-gbadev)
- [Blog do Chrono - Introdução à programação de GBA (PT-BR)](https://blogdochrono.blogspot.com/2017/11/introducao-programacao-de-game-boy.html)
- [Loirak - Tutoriais de ROM Hacking GBA (PT-BR)](http://www.loirak.com/gameboy/gbatutor.php)
- [Tonc - Tutoriais e documentação GBA](https://www.coranac.com/tonc/text/asm.htm)
- [GBATEK - Referência técnica completa](https://problemkaputt.de/gbatek.htm)
- [ARM7TDMI Technical Reference](https://developer.arm.com/documentation/ddi0210/c/)
- [Tonc - Hardware do GBA](https://www.coranac.com/tonc/text/hardware.htm)
- [GBAdev.net](https://www.gbadev.net/)

---

## 🛠️ Fluxo de Engenharia Reversa

1. **Aquisição da ROM:** Obtenha um dump limpo da ROM do GBA.
2. **Leitura do Header:** Leia e interprete o header da ROM para obter metadados e entry points.
3. **Detecção de Tabelas de Ponteiros:** Procure por tabelas de ponteiros (normalmente valores de 32 bits little-endian na faixa 0x08xxxxxx).
4. **Identificação de Blocos de Texto:** Localize blocos de texto (puros, codificados ou comprimidos).
5. **Detecção de Compressão:** Identifique e descomprima blocos de dados (ex: LZ77, Huffman).
6. **Extração de Assets:** Extraia gráficos, paletas e outros assets.
7. **Edição & Reempacotamento:** Modifique os dados extraídos e reempacote na ROM.
8. **Testes:** Rode a ROM modificada em um emulador ou hardware real.

---

## 🧩 Header da ROM em Detalhe

- **Offset do Header:** 0x00000000 - 0x000000BC
- **Campos:**
  - Entry Point (0x00-0x03)
  - Logo Nintendo (0x04-0x9F)
  - Título do Jogo (0xA0-0xAB)
  - Código do Jogo (0xAC-0xAF)
  - Maker Code (0xB0-0xB1)
  - Valor Fixo (0xB2)
  - Main Unit Code (0xB3)
  - Device Type (0xB4)
  - Reservado (0xB5-0xB9)
  - Versão do Software (0xBC)
  - Complement Check (0xBD)

**Exemplo em Python:**
```python
with open('jogo.gba', 'rb') as f:
    header = f.read(0xC0)
    titulo = header[0xA0:0xAC].decode('ascii')
    codigo = header[0xAC:0xB0].decode('ascii')
    print(f"Título: {titulo}, Código: {codigo}")
```
- [GBATEK - Header da ROM](https://problemkaputt.de/gbatek.htm#gbacartridgeheader)

---

## 🧩 Detecção e Extração de Tabelas de Ponteiros

**Resumo:**
Jogos de GBA usam ponteiros de 32 bits little-endian, normalmente apontando para endereços na faixa 0x08xxxxxx (ROM). Tabelas de ponteiros são blocos contíguos desses valores.

**Algoritmo (Python):**
```python
import struct

def encontrar_ponteiros(rom_bytes, base=0x08000000):
    ponteiros = []
    for i in range(0, len(rom_bytes) - 4, 4):
        val = struct.unpack('<I', rom_bytes[i:i+4])[0]
        if base <= val < base + len(rom_bytes):
            ponteiros.append((i, val))
    return ponteiros
```
- **Heurística:** Procure sequências de valores de 4 bytes onde a maioria aponta para endereços válidos da ROM.

---

## 📝 Extração e Codificação de Texto

- **Armazenamento de texto:**
  - ASCII/Shift-JIS puro
  - Codificação customizada (baseada em tabela)
  - Comprimido (geralmente LZ77)
- **Detecção:**
  - Procure blocos legíveis em ASCII/Shift-JIS
  - Use arquivos de tabela para codificações customizadas

**Exemplo: Extraindo texto ASCII**
```python
import re
with open('jogo.gba', 'rb') as f:
    data = f.read()
    for match in re.finditer(rb'[\x20-\x7E]{4,}', data):
        print(f"Offset {match.start():08X}: {match.group().decode('ascii')}")
```

**Decodificação baseada em tabela:**
- Monte um arquivo `.tbl` mapeando bytes para caracteres
- Use para decodificar blocos de texto

---

## 🗂️ Manipulação de Tabelas de Caracteres (TBL)

- **Exemplo de formato:**
  - `80=A`
  - `81=B`
  - `82=C`
- **Exemplo em Python:**
```python
def carregar_tbl(path):
    tbl = {}
    with open(path) as f:
        for line in f:
            if '=' in line:
                k, v = line.strip().split('=')
                tbl[int(k, 16)] = v
    return tbl
```

---

## 🗜️ Compressão & Descompressão

### LZ77 (GBA)
- **Header:** 0x10 (1 byte), seguido de 3 bytes para o tamanho descomprimido
- **Bloco:** [0x10][tamanho][dados comprimidos]
- **Detecção:** Procure por 0x10 no início do bloco

**Exemplo em Python (descompressão LZ77):**
- Veja [GBATEK LZ77](https://problemkaputt.de/gbatek.htm#biosdecompressionfunctions)
- [Exemplo Python LZ77 (externo)](https://github.com/pleonex/tinke/blob/master/tinke/formats/lz77.py)

**Exemplo em C:**
- [Tonc LZ77 C Implementation](https://www.coranac.com/tonc/text/asm.htm#sec-lz77)

---

## 🎨 Extração de Gráficos e Assets

- **Tiles:** 8x8 pixels, 4bpp ou 8bpp
- **Paletas:** 15 bits BGR555
- **Mapas:** Tilemaps para backgrounds
- **Extração:**
  - Leia estruturas tipo VRAM da ROM
  - Converta para PNG usando Python (ex: Pillow) ou C/C++ para velocidade

---

## 💾 Save Data (SRAM/EEPROM/Flash)
- **SRAM:** 0x0E000000, até 64 KB
- **EEPROM/Flash:** Tratamento especial, veja [GBATEK Save Types](https://problemkaputt.de/gbatek.htm#gbacartbackupflashsramandeeprom)
- **Leitura/Escrita:**
  - Para patching, localize e modifique blocos de save

---

## 🚀 Plano de Ação para Ferramenta Customizada

1. **Core em Python:**
   - Parsing da ROM, busca de ponteiros, extração de texto, patching
2. **Módulos de performance em C/C++/C#:**
   - Compressão/descompressão, conversão de gráficos
3. **Design modular:**
   - Módulos separados para cada console/formato
   - Fácil adicionar novos extratores/patchers
4. **Exemplo de estrutura de projeto:**
   - `/core` (Python): parsing, extração, patching
   - `/native` (C/C++/C#): código de alta performance
   - `/tables`: tabelas de caracteres
   - `/docs`: documentação técnica

---

## 📑 Apêndice: Padrões, Magic Numbers e Pegadinhas

- **Bloco LZ77:** Começa com 0x10
- **Base de ponteiros:** 0x08000000
- **Texto ASCII:** 0x20-0x7E
- **Shift-JIS:** 0x81-0x9F, 0xE0-0xFC (bytes iniciais)
- **Header magic:** Logo Nintendo em 0x04
- **Pegadinhas:**
  - Tabelas de ponteiros sobrepostas/comprimidas
  - Codificações mistas
  - Bank switching em alguns jogos

---

## 🔗 Referências (veja lista principal acima)
- [GBATEK](https://problemkaputt.de/gbatek.htm)
- [Tonc](https://www.coranac.com/tonc/)
- [awesome-gbadev](https://github.com/gbadev-org/awesome-gbadev)
