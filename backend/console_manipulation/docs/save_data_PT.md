# 🟨 Save Data (SRAM/EEPROM/Flash) em ROM Hacking

> :us: [English version](save_data.md)

## O que é Save Data?
Save data refere-se ao armazenamento persistente usado pelos jogos para manter progresso, configurações ou desbloqueios. Em consoles retrô, isso normalmente é implementado como SRAM, EEPROM ou Flash na mídia do cartucho ou dispositivo.

## Por que é Importante?
- **Progresso:** Armazena progresso do jogador, recordes, conteúdo desbloqueado e configurações.
- **ROM hacking:** Permite tradução de menus, desbloqueio de recursos ou criação de saves customizados.
- **Debug:** Útil para testes, cheats e desenvolvimento rápido.

## Tipos de Save Data
- **SRAM:** RAM estática, geralmente com bateria, até 64 KB.
- **EEPROM:** Apagável eletricamente, pequena (512B–8KB), usada para saves.
- **Flash:** Memória maior e regravável, usada em cartuchos mais recentes.

## Exemplos
- **GBA/GB:** SRAM em 0x0E000000, EEPROM/Flash mapeados em endereços especiais.
- **SNES:** SRAM mapeada em faixa específica do ROM.
- **PlayStation:** Memory cards usam flash para saves.

## Uso em ROM Hacking
- **Edição de save:** Modificar valores (dinheiro, itens, progresso) diretamente no arquivo de save.
- **Tradução:** Alterar texto ou menus armazenados no save.
- **Desbloqueios:** Setar flags para itens, fases ou recursos.
- **Debug:** Criar saves de teste para desenvolvimento ou speedrun.

## Leitura adicional
- [Wikipedia: Save game](https://en.wikipedia.org/wiki/Save_game)
- [GBATEK - Save Types](https://problemkaputt.de/gbatek.htm#gbacartbackupflashsramandeeprom)

---

## Tópicos Relacionados
- [Hexadecimal](hexadecimal_PT.md)
- [Ponteiros](pointers_PT.md)
- [Magic Numbers](magic_numbers_PT.md)
- [Compressão](compression_PT.md)
- [Tabelas de Caracteres](character_tables_PT.md)
