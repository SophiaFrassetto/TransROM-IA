# 🟫 Estrutura de Arquivo & Header em ROM Hacking

> :us: [English version](file_structure_headers.md)

## O que é Estrutura de Arquivo & Header?
Estrutura de arquivo é a organização dos dados dentro de um arquivo, normalmente dividida em seções como header, blocos de dados e footer. O header é uma região fixa no início do arquivo ou ROM que contém metadados, magic numbers e ponteiros para dados importantes.

## Por que é Importante?
- **Navegação:** Entender a estrutura permite localizar e modificar dados específicos (texto, gráficos, código).
- **Validação:** O header geralmente contém checksums, tamanho do arquivo e outros controles de integridade.
- **Engenharia reversa:** Headers revelam entry points, informações de versão e localização de blocos de dados.

## Campos Comuns em Headers
- **Magic number:** Identifica o tipo de arquivo
- **Versão:** Indica a versão do arquivo ou formato
- **Tamanho:** Tamanho total do arquivo ou bloco de dados
- **Ponteiros/Offsets:** Endereços para seções de dados (texto, gráficos, etc.)
- **Checksums:** Para integridade dos dados
- **Info do jogo/ROM:** Título, código, região, etc.

## Exemplos
- **ROM NES:** Header contém magic number (`4E 45 53 1A`), tamanhos PRG/CHR, flags
- **ROM SNES:** Pode ter header de 512 bytes com info do jogo
- **ROM GBA:** Header inclui logo Nintendo, título do jogo, código, checksums
- **Binário geral:** Formatos customizados podem ter header curto com magic, tamanho e ponteiros

## Uso em ROM Hacking
- **Criação de patch:** Modificar header para mudar título, região ou checksums
- **Extração de dados:** Usar ponteiros/offsets para localizar e extrair assets
- **Conversão de formato:** Identificar e adaptar headers para emuladores ou ferramentas

## Leitura adicional
- [Wikipedia: File format](https://en.wikipedia.org/wiki/File_format)
- [GBATEK - GBA Cartridge Header](https://problemkaputt.de/gbatek.htm#gbacartridgeheader)

---

## Tópicos Relacionados
- [Hexadecimal](hexadecimal_PT.md)
- [Magic Numbers](magic_numbers_PT.md)
- [Ponteiros](pointers_PT.md)
- [Compressão](compression_PT.md)
- [Tabelas de Caracteres](character_tables_PT.md)
