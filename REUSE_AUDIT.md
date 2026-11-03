# Auditoria de reutilização de código — Kanto Online

Data da auditoria: 2026-11-02

## Objetivo

Acelerar o Kanto Online reaproveitando código legalmente reutilizável, sem perder:
- a geografia e os mapas derivados da estrutura de Pokémon FireRed;
- a engine atual e o trabalho de extração/validação já feito;
- suporte obrigatório a navegador móvel e desktop;
- a direção de experiência inspirada no InfinityMMO.

## 1. InfinityMMO

Site analisado: https://infinitymmo.net/

A página pública apresenta fluxo de conta/treinador, seleção de nome, servidor, equipe, dinheiro, insígnias, Pokédex, shinies, comunidade/chat e controles na tela. A inspeção pública não revelou um repositório de código-fonte ou uma licença de software que autorize reutilização.

**Decisão:** não copiar HTML, CSS, JavaScript, imagens, sprites, marca ou outros arquivos do InfinityMMO. Usá-lo como referência funcional e visual observável. Reavaliar se o responsável publicar o código ou conceder autorização expressa por escrito.

## 2. RPGJS v5 — candidato para estudo e reutilização modular

- Repositório: https://github.com/RSamaium/RPG-JS
- Documentação: https://rpgjs.dev/
- Licença declarada: MIT.
- Stack: TypeScript, Vite, CanvasEngine, pacotes cliente/servidor.
- Recursos anunciados: mapas Tiled, eventos, diálogos, inventário, habilidades, combate, salvamento, HUD, menus, sincronização multiplayer, contas/chat e controles mobile/gamepad.

A licença MIT permite reutilizar e modificar o código, mantendo os avisos de copyright e licença. Antes de incorporar qualquer arquivo/pacote, conferir a licença e os avisos da versão exata utilizada e registrar a proveniência.

**Compatibilidade:** é o candidato mais próximo do formato 2D RPG/MMORPG de navegador e de mobile. Porém, o Kanto Online já depende de uma engine PixiJS própria, de mapas FireRed extraídos, colisões, warps e ferramentas de validação. RPGJS v5 usa outra arquitetura de renderização e runtime. Trocar a engine inteira agora arriscaria descartar o progresso de mapa e atrasar a beta.

**Decisão:** não substituir a engine atual neste momento. Fazer prova de conceito isolada antes de importar qualquer módulo. Priorizar estudo/reutilização de sistemas independentes (controles mobile, UI, diálogos, inventário, persistência e multiplayer) apenas se puderem ser adaptados sem quebrar o pipeline de mapas.

## 3. RealmForge — referência secundária

- Repositório: https://github.com/mattiaa95/realmforge
- Licença declarada: MIT.
- Stack: Phaser 3 + TypeScript/Preact no cliente; Rust/WebSocket no servidor.
- Recursos anunciados: inventário, equipamento, banco, crafting, quests, guildas, chat, grupos, diálogos e multiplayer autoritativo.

**Limitação:** é um MMORPG isométrico com geração procedural de mundo, não um motor de mapa top-down de tiles FireRed. Seu servidor Rust e arquitetura de cliente são diferentes da base atual.

**Decisão:** usar como referência técnica para desenho de sistemas MMO (chat, grupos, servidor autoritativo, persistência e inventário), não importar o projeto inteiro nem seus mapas/arte.

## 4. Engine atual do Kanto Online

- Repositório: https://github.com/blixxurd/kanto
- Revisão fixada no submódulo: `7eba2607b5894f558c40c72d9d310f7d501c301a`
- Licença: MIT (arquivo `engine/LICENSE`).
- Stack atual: TypeScript, Vite, PixiJS 8 e @pixi/tilemap.
- Já existe pipeline de extração de layouts, tilesets, cabeçalhos, warps, colisões, mapas internos, sprites e costura do mundo.

**Decisão:** manter essa engine como base da beta. Reaproveitar código MIT de terceiros somente por integração incremental e com atribuição/licenças registradas. Não fazer migração ampla sem uma prova de conceito que demonstre mapas, warps, colisões, browser, mobile e testes funcionando.

## 5. Próxima ordem de implementação

1. Completar a beta jogável na engine atual.
2. Implementar controles de toque e layout responsivo para celular sem remover teclado no computador.
3. Construir a interface e os sistemas visíveis inspirados no InfinityMMO (sem copiar seus arquivos proprietários).
4. Adicionar progressivamente equipe, inventário, Pokédex, insígnias, diálogos, batalhas e salvamento.
5. Introduzir servidor, contas e sincronização multiplayer depois de a experiência local estar estável.
6. Fazer uma prova de conceito RPGJS isolada somente se um sistema concreto não puder ser implementado de forma segura na engine atual.

## Fontes consultadas

- InfinityMMO: https://infinitymmo.net/
- RPGJS v5: https://github.com/RSamaium/RPG-JS
- RPGJS site/documentação: https://rpgjs.dev/
- RealmForge: https://github.com/mattiaa95/realmforge
- Engine atual: https://github.com/blixxurd/kanto

## Observação de propriedade intelectual

A licença MIT dos motores de código não concede direitos sobre Pokémon, marcas, ROMs ou assets proprietários. O conteúdo derivado de Pokémon FireRed deve continuar separado e ser tratado conforme os direitos e permissões aplicáveis antes de qualquer distribuição pública.
