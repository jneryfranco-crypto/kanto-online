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

A engine espera encontrar a descompilação em `engine/decomp`. O repositório a mantém separada como submódulo na raiz para não misturar os dois projetos. Crie uma ligação local:

**macOS / Linux:**

```bash
ln -s ../decomp engine/decomp
```

**Windows PowerShell (na pasta raiz do projeto):**

```powershell
New-Item -ItemType Junction -Path engine\decomp -Target (Resolve-Path decomp)
```

## Instalar e gerar os dados

Requisitos: Node.js 18+, npm, Python 3.10+ e Git.

```bash
cd engine
npm install
python -m pip install -r scripts/requirements.txt
npm run extract
npm test
npm run typecheck
npm run dev
```

O comando `npm run extract` gera os mapas, atlas de tiles, colisões, warps e sprites localmente. Os arquivos gerados não são versionados neste repositório; a extração usa a revisão de `pret/pokefirered` fixada pelo submódulo.

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
