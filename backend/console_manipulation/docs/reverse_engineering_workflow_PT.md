# 🟫 Fluxo de Engenharia Reversa em ROM Hacking

> :us: [English version](reverse_engineering_workflow.md)

## O que é um Fluxo de Engenharia Reversa?
Um fluxo de engenharia reversa é um processo passo a passo para analisar, entender e modificar ROMs ou arquivos binários. Ele ajuda a organizar a abordagem para extração, edição e teste de dados em jogos retrô.

## Por que é Importante?
- **Abordagem sistemática:** Garante que nada seja esquecido e aumenta a eficiência.
- **Repetibilidade:** Útil para vários jogos ou projetos.
- **Documentação:** Facilita o compartilhamento de conhecimento e onboarding de novos colaboradores.

## Etapas Típicas
1. **Aquisição da ROM:** Obtenha um dump limpo da ROM.
2. **Análise do Header:** Leia e interprete o header da ROM para metadados e entry points.
3. **Detecção de Tabelas de Ponteiros:** Encontre tabelas de endereços para blocos de dados.
4. **Identificação de Texto & Assets:** Localize e extraia textos, gráficos e outros assets.
5. **Análise de Compressão:** Identifique e descomprima blocos de dados comprimidos.
6. **Edição:** Modifique os dados extraídos (texto, gráficos, código).
7. **Reempacotamento:** Recomprima e reinsira os dados modificados na ROM.
8. **Testes:** Rode a ROM modificada em um emulador ou hardware real.

## Uso em ROM Hacking
- **Tradução:** Extrair e reinserir textos para localização.
- **Restauração:** Recuperar conteúdo oculto ou não utilizado.
- **Mods:** Adicionar novos recursos, gráficos ou fases.
- **Debug:** Testar alterações e automatizar tarefas repetitivas.

## Leitura adicional
- [Wikipedia: Reverse engineering](https://en.wikipedia.org/wiki/Reverse_engineering)
- [Romhacking.net - Documents](https://www.romhacking.net/documents/)

---

## Tópicos Relacionados
- [Hexadecimal](hexadecimal_PT.md)
- [Ponteiros](pointers_PT.md)
- [Magic Numbers](magic_numbers_PT.md)
- [Compressão](compression_PT.md)
- [Tabelas de Caracteres](character_tables_PT.md)
