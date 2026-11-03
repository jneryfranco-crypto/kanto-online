# Kanto Online — etapa de reconstrução do mapa

Esta etapa mantém a versão 0.5 original em `index.html` e prepara a engine de mundo aberto em `engine/`, como submódulo Git. A engine é o projeto **Kanto Open World**, de licença MIT; consulte `engine/LICENSE` e preserve os créditos ao redistribuir ou modificar seu código.

## O que esta base oferece

- Mundo externo de Kanto costurado em um mapa contínuo a partir das conexões de FireRed.
- Dados de mapas, layouts, warps e colisões extraídos do projeto `pret/pokefirered`.
- Renderização pixel art com tilesets, movimento em grade, câmera e transições.
- Mapas internos exportados separadamente e acessados por warps.

A engine informa um mundo externo de aproximadamente 424 × 416 tiles. Isso é a capacidade declarada pelo projeto upstream, não uma validação independente nossa de cada tile. O mapa final precisa passar pelos validadores de extração, costura, travessia e warps antes de ser considerado correto.

## Preparação (uma vez)

Clone o Kanto Online com os submódulos:

```bash
git clone --recurse-submodules https://github.com/jneryfranco-crypto/kanto-online.git
cd kanto-online
```

Se já clonou antes sem submódulos:

```bash
git submodule update --init --recursive
```

A engine espera encontrar a descompilação em `engine/decomp`. O repositório a mantém separada como submódulo na raiz; os scripts de preparação criam a ligação local automaticamente.

## Instalar, extrair e validar

Requisitos: Node.js 18+, npm, Python 3.10+ e Git.

**macOS / Linux:**
```bash
bash ./setup-map.sh
```

**Windows PowerShell:**
```powershell
.\setup-map.ps1
```

A extração é executada por `extract-map.sh`. Ela chama os 12 exportadores da engine na ordem correta: tilesets, layouts, cabeçalhos, warps, colisões, costura do mundo, mapas internos, jogador, animações de tiles, portas, sprites de surfe e NPCs. Em seguida exporta o efeito de grama, verifica os arquivos exigidos pelo runtime e executa a suíte completa de validação. Essa ordem evita um erro do agregador upstream, que tenta validar o sprite do jogador antes de gerá-lo.

O pequeno patch em `patches/engine/` evita que a ausência do efeito cosmético de poeira ao aterrissar interrompa a inicialização do jogo; os demais assets obrigatórios são verificados pelo `validate-runtime-assets.py`.

Para iniciar manualmente depois da preparação:

```bash
cd engine
npm run dev
```

Os arquivos gerados localmente não são versionados neste repositório. A extração usa a revisão de `pret/pokefirered` fixada pelo submódulo.

## Controles da engine

- WASD ou setas: andar.
- Shift: correr.
- ` (crase): menu de depuração.
- F3: alternar overlays de depuração.
- F11: tela cheia.

## Importante sobre a fidelidade

Não considerar o mapa concluído apenas porque a engine inicia. Antes de integrar como versão principal, verificar os quatro validadores, testar as conexões da sequência Pallet Town → Route 1 → Viridian City → Route 2 → Viridian Forest → Pewter City e inspecionar colisões, entradas e warps no navegador.

## Licenças e propriedade intelectual

A engine `blixxurd/kanto` é licenciada sob MIT; sua licença e avisos permanecem no submódulo `engine`. A descompilação `pret/pokefirered` é mantida em submódulo separado. Este repositório não inclui ROM, nem copia para si os assets extraídos do jogo. Verifique as licenças e permissões aplicáveis antes de publicar qualquer build com conteúdo derivado de Pokémon.
