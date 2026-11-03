# Histórico de validação e diagnóstico

Este arquivo registra falhas reais do CI, sua causa identificada, a correção aplicada e o resultado. Não tratar uma hipótese como defeito confirmado do jogo.

## 2026-11-03 — Teste de movimento inicial com timeout

- **Execução:** [GitHub Actions #41568952604](https://github.com/jneryfranco-crypto/kanto-online/actions/runs/41568952604)
- **Etapas aprovadas:** extração dos mapas e validadores; TypeScript; build de produção; instalação do Chromium; inicialização do jogo no navegador.
- **Estado inicial confirmado:** API de diagnóstico presente, canvas renderizado em 960×640, estado `playing`, jogador em `(80,278)`, zona Pallet Town.
- **Falha observada:** `page.waitForFunction: Timeout 3000ms exceeded`, em `engine/[eval1]:69:14`, durante a primeira confirmação de movimento real por teclado.
- **Classificação:** timeout do teste de navegador; não há evidência nesta execução de falha na extração, build ou colisões do mapa. A execução anterior havia passado pelo teste de movimento, então a hipótese mais provável é variação de tempo/frame no Chromium do CI.
- **Correção aplicada:** ampliar para 10 segundos os dois limites de espera de movimento inicial/retorno no smoke test, sem alterar regras de movimento do jogo.
- **Commit da correção:** `3e2a1477e774f9c5448b464776790069c93e37f3`.
- **Resultado:** aguardando nova execução do CI.

## 2026-11-03 — Alvo fixo em Pewter não alcançável

- **Execução:** [GitHub Actions #41568005343](https://github.com/jneryfranco-crypto/kanto-online/actions/runs/41568005343)
- **Falha:** o teste tentou caminhar até `(74,82)` a partir de `(73,121)` e não encontrou caminho sem colisão.
- **Diagnóstico:** o validador de dados já confirmava caminho da saída norte até a zona de Pewter. O teste de navegador estava impondo uma coordenada fixa, em vez de um tile caminhável dentro dos limites da zona.
- **Correção aplicada:** o smoke test agora seleciona, usando a grade real de colisão e os limites de `MAP_PEWTER_CITY`, um tile alcançável a partir da posição de retorno.
- **Commit:** `a19e3fd817ea1d91095e3a757032c9886f86a93f`.
- **Resultado:** a execução seguinte passou os validadores, mas revelou o timeout de movimento inicial documentado acima.

## Princípio de manutenção

- Corrigir primeiro o teste quando a evidência apontar para uma premissa incorreta ou timeout do teste.
- Alterar colisão, mapa ou mecânica somente quando houver evidência reproduzível de defeito no jogo.
- Preservar os testes que já passaram e reexecutar CI após cada correção.
