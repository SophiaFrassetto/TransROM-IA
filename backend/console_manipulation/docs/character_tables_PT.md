# 🟩 Tabelas de Caracteres em ROM Hacking e Retrocomputação

> :us: [English version](character_tables.md)

## O que é uma Tabela de Caracteres?
Uma tabela de caracteres é um mapeamento entre valores de bytes (ou sequências de bytes) e caracteres ou strings. Em sistemas digitais, especialmente em jogos retrô e software embarcado, as tabelas de caracteres definem como o texto é codificado e decodificado, muitas vezes usando esquemas customizados ou não padronizados.

## Importância Técnica das Tabelas de Caracteres
- **Codificação/decodificação de texto:** Tabelas de caracteres são essenciais para converter entre dados brutos e texto legível.
- **ROM hacking e tradução:** Muitos jogos usam tabelas customizadas para texto, exigindo engenharia reversa para extrair ou inserir scripts.
- **Automação:** Ferramentas usam arquivos de tabela (arquivos texto simples mapeando valores hex para caracteres) para automatizar extração, inserção e tradução de texto.

## Nomenclatura & Notação
- **Arquivo de tabela (.tbl):** Arquivo texto mapeando valores hex para caracteres (ex: `80=A`)
- **Codificação single-byte:** 1 byte por caractere (ex: ASCII, codificação padrão para texto em inglês)
- **Codificação multi-byte:** 2 ou mais bytes por caractere (ex: Shift-JIS, usada para japonês)
- **Codificação customizada:** Mapeamentos específicos de jogos ou proprietários.

## Exemplos Ampliados
- **ASCII:** `41` → `A`, `61` → `a`
- **Shift-JIS:** `82 A0` → `あ`
- **Tabela customizada:** `80=A`, `81=B`, `90=É`, `8140=あ`
- **Linha de arquivo de tabela:** `80=A` (valor hex = caractere)

## Técnicas
- **Montagem de tabela:** Analisar dados da ROM para deduzir o mapeamento byte-caractere
- **Edição de tabela:** Adicionar ou corrigir mapeamentos para símbolos especiais ou diacríticos
- **Extração/inserção baseada em tabela:** Usar ferramentas (Cartographer, Atlas, WindHex) com arquivos de tabela

## Uso em ROM Hacking
- **Tradução de texto:** Decodificar e re-encodar scripts para localização
- **Font hacking:** Relacionar tabela com gráficos de fonte para alfabetos customizados
- **Ferramentas de script:** Automatizar inserção/extração usando arquivos de tabela

## Exemplos de Consoles
- **NES/SNES:** Frequentemente usam tabelas single-byte customizadas
- **Game Boy/Advance:** Mistura de ASCII, Shift-JIS e tabelas customizadas
- **PlayStation:** Codificações multi-byte, geralmente Shift-JIS ou customizadas
- **Mega Drive:** Tabelas customizadas para jogos ocidentais e japoneses

## Leitura adicional
- [Romhacking.net - Table Files](https://www.romhacking.net/utilities/)
- [Tutorial WindHex de Tabelas](http://www.loirak.com/gameboy/gbatutor.php)

---

## Tópicos Relacionados
- [Hexadecimal](hexadecimal_PT.md)
- [Ponteiros](pointers_PT.md)
- [Magic Numbers](magic_numbers_PT.md)
- [Compressão](compression_PT.md)
