---
name: prompt-chain
description: Use this skill whenever the user wants to break a complex multi-step task into a sequence of prompts, each executed in a fresh chat session with full context carried forward. Trigger phrases in PT-BR and EN — "executar por etapas em chats separados", "cada etapa em um novo chat", "prompt autocontido autopropagante", "prompt que gera o próximo", "quero passar esse trabalho para vários chats", "cold start entre chats", "monte um prompt que eu colo em outro chat", "chain of prompts", "self-propagating prompt", "split this across sessions". Also trigger when the user has a long multi-phase task (P0 → P1 → P2), when they mention context limits or fresh sessions, or when they want to isolate execution between phases. Don't wait for exact wording — if the user is trying to distribute sequential work across multiple chat sessions with context preservation, invoke this skill.
---

# Prompt Chain

Transforma uma tarefa multi-etapas em uma cadeia de prompts autocontidos, onde cada prompt executa um stage em um chat novo e emite, junto ao output, o prompt do próximo stage já com o contexto acumulado. O usuário só precisa copiar-colar entre chats — a chain se propaga sozinha até `CHAIN COMPLETE`.

## Quando usar

- Tarefa grande com fases distintas (P0 → P1 → P2), cada uma com entregáveis próprios
- Usuário quer isolar contexto entre etapas (novo chat = memória limpa, cache frio, execução isolada)
- Usuário pede explicitamente "um prompt que gera o próximo" ou equivalente
- Trabalho que se beneficia de pausar entre stages para revisar output antes de continuar
- Ambientes onde o mesmo agente não pode rodar a cadeia toda (limite de sessão, política de auditoria, troca de modelo)

## Quando NÃO usar

- Tarefa de um passo só → resolva direto, sem overhead
- Tarefa onde o estado intermediário cabe numa sessão e não há risco de estouro → TodoWrite + execução direta é melhor
- Tarefa exploratória sem entregáveis discretos → chain pressupõe stages com Definition of Done claro
- Paralelismo (chains são sequenciais por natureza) → use subagents em paralelo

## Mental model

Uma chain é uma sequência de stages. Cada stage:
1. Recebe um prompt autocontido (pasteável cold em chat novo)
2. Executa uma fatia do trabalho
3. Emite o prompt do próximo stage com contexto atualizado

O pulo do gato: **contexto estável vs contexto dinâmico**.

- **Estável** — workspace path, design system, voz da marca, restrições globais, objetivo final. Copiado verbatim em todos os stages.
- **Dinâmico** — estado atual dos arquivos, decisões tomadas, bloqueios encontrados. Atualizado stage a stage.

Se a chain perder contexto estável, o próximo chat refaz decisões. Se perder contexto dinâmico, refaz trabalho. Ambas as falhas destroem o valor.

## Como montar uma chain

### Passo 1 — Delimite a tarefa e extraia contexto estável

Antes de decompor, separe:

- **Objetivo final** — o que significa "chain completa"? Enunciado único e verificável.
- **Workspace** — caminho absoluto + convenções (pasta de escrita, naming, idioma).
- **Restrições que não mudam** — design system, compliance, voz da marca, formato de output.
- **Decisões já tomadas** — o que o usuário já definiu e não será reaberto.
- **Ambiente alvo** — Claude Code / Cowork / Claude.ai Chat. Cada um tem tools diferentes.

Esse conjunto vai na seção CONTEXTO HERDADO de todos os stages, inalterado.

### Passo 2 — Decomponha em 2 a 6 stages

**Heurísticas de corte:**
- Cada stage tem um deliverable concreto e verificável (arquivo criado, decisão tomada, output validado)
- Um stage não depende do estado interno do anterior (variáveis, buffers) — só de arquivos e decisões registradas
- Priorize por dependência e risco: P0 (bloqueadores) → P1 (alto impacto) → P2 (polish)

**Número ideal:**
- **2 stages** — divisão natural em "construir" → "validar/polish"
- **3–4 stages** — sweet spot para a maioria dos casos
- **5–6 stages** — só quando cada fase tem > 10 min de trabalho próprio
- **> 6** — re-agrupe. A chain está fatiada demais e o overhead supera o ganho.

**Teste dos 10 minutos:** se um stage leva < 5 min de trabalho real, combine com o vizinho. Se leva > 30 min, quebre. Alvo: 10–20 min por stage.

### Passo 3 — Redija o Stage 1 (prompt-semente)

Use o template canônico da próxima seção. Este é o único prompt que o usuário cola manualmente; os demais a chain gera sozinha.

### Passo 4 — Entregue ao usuário

Entregue o Stage 1 em bloco de código copiável, com uma instrução curta de uso acima:

> 1. Abra chat novo no ambiente [X]
> 2. Cole o bloco STAGE 1
> 3. Ao final da resposta, copie o bloco `### PRÓXIMO PROMPT — STAGE 2` e cole em novo chat
> 4. Repita até `CHAIN COMPLETE`

## Template canônico de STAGE

Copie-colando verbatim, ajustando conteúdo. Todo stage da chain usa essa estrutura.

````markdown
# STAGE N/TOTAL — [NOME_CURTO]
# Chain: "[NOME DA CHAIN]"

## CHAIN META
- Total stages: TOTAL
- Current stage: N/TOTAL
- Stage 1 objetivo: [...]
- Stage 2 objetivo: [...]
- (todos os stages resumidos em uma linha cada)

## WORKSPACE
Absolute path: `[caminho absoluto]`
Ambiente alvo: [Claude Code / Cowork / Chat]
[Convenções relevantes: pasta de escrita, naming, idioma]

## CONTEXTO HERDADO — LEITURA OBRIGATÓRIA

### Objetivo da chain
[Enunciado único do que significa chain completa]

### Decisões já tomadas
- [decisão 1 — não reabrir]
- [decisão 2 — não reabrir]

### Estado atual auditado ([YYYY-MM-DD])
- ✅ EXISTE: [arquivos criados por stages anteriores]
- ❌ NÃO EXISTE: [arquivos faltantes]
- ⚠️ [nuances, warnings, gotchas]

### [Contexto estável: design system / voz / compliance / etc.]
[Blocos literais, copiados verbatim em todos os stages]

## TAREFA DESTE STAGE
1. [ação concreta com critério de "feito"]
2. [ação concreta com critério de "feito"]
...

## RESTRIÇÕES
- [o que NÃO fazer neste stage — arquivos intocáveis, decisões congeladas]

## DELIVERABLES
1. [arquivo/output 1]
2. [arquivo/output 2]
...
N. **OBRIGATÓRIO**: bloco `### PRÓXIMO PROMPT — STAGE N+1` ao final (ou `### CHAIN COMPLETE` se N = TOTAL)

## PROPAGATION PROTOCOL — CRÍTICO
Ao final da sua resposta, emita um bloco de código markdown contendo o prompt completo e autocontido para Stage N+1. O próximo chat terá ZERO memória deste. O prompt de Stage N+1 deve:

- Abrir com `# STAGE N+1/TOTAL — [NOME]`
- Copiar verbatim CHAIN META, WORKSPACE, e todo CONTEXTO HERDADO estável (design system / voz / compliance) deste prompt
- Atualizar "Decisões já tomadas" e "Estado atual auditado" com o que você acabou de fazer
- Substituir TAREFA pela lista de ações do Stage N+1 (ver CHAIN META acima)
- Incluir o mesmo PROPAGATION PROTOCOL para Stage N+2 (ou substituir por FINAL TERMINATION se Stage N+1 for o último)

Se este stage não puder ser completado (bloqueio, ambiguidade, input faltante), emita no lugar do próximo prompt um bloco `### CHAIN PAUSED` (ver protocolos).
````

## Protocolos de transição

### PROPAGATION PROTOCOL (stage → próximo stage)

Toda resposta de stage não-final termina com o header:

```
### PRÓXIMO PROMPT — STAGE N+1
```

Seguido por um bloco de código markdown fechado. **Atenção ao escape de fences**: como o conteúdo do próximo prompt contém crases triplas, use fence com **4 crases** no bloco externo (ou `~~~~` como alternativa). Isso evita que o parser feche o bloco cedo.

Princípios:
- **Nunca abrevie com "igual ao anterior"** — o próximo chat não tem o anterior
- **Copiar contexto estável verbatim é o comportamento correto**, não redundância
- **Atualize apenas campos dinâmicos**: Decisões já tomadas, Estado atual auditado, TAREFA DESTE STAGE
- **Mantenha o PROPAGATION PROTOCOL intacto** dentro do próximo stage, apontando para o stage seguinte
- **Ajuste o "Current stage"** e atualize o DoD de Stage N+1 com base no que foi feito agora

### CHAIN PAUSED (bloqueio)

Quando um stage não pode ser completado sem input humano, substitua o bloco de próximo prompt por:

```markdown
### CHAIN PAUSED

**O que foi feito:**
- [...]

**Bloqueio:**
[descrição do que impede progressão]

**Pergunta para o usuário:**
[pergunta direta, única, com opções quando possível]

**Como retomar:**
Responda à pergunta acima. Em seguida, copie este mesmo prompt de STAGE N em chat novo, acrescentando no início uma seção "## DECISÃO DO USUÁRIO" com a resposta. A chain continua a partir daqui.
```

**Regra-mestra:** pausar é sempre preferível a adivinhar. Adivinhar no stage N contamina todos os stages seguintes e o usuário só descobre o erro no final.

### CHAIN COMPLETE (último stage)

O último stage substitui o bloco de próximo prompt por:

```markdown
### CHAIN COMPLETE

**Objetivo da chain:**
[enunciado original da CHAIN META]

**Entregáveis finais:**
- [arquivo 1 — caminho]
- [arquivo 2 — caminho]
...

**Decisões registradas durante a chain:**
- Stage 1: [...]
- Stage 2: [...]
...

**Próximos passos fora da chain:**
[se houver — deploy, revisão humana, publicação]
```

Esse bloco funciona como acta da chain — o usuário arquiva junto com os entregáveis e tem rastro do que foi decidido.

## Heurísticas de decomposição

**Separe por tipo de risco:**
- Decisões irreversíveis primeiro (criar estrutura, escolher formato, empacotar)
- Edições reversíveis depois (ajustes, refinamentos, polish)
- Validação por último (QA, contagem, contraste, cross-browser)

**Um stage = um contexto de execução:**
Se dois passos usam o mesmo conjunto de arquivos e o mesmo mindset, coloque no mesmo stage. Se precisam de modos mentais diferentes (construir vs. auditar, escrever vs. testar), separe.

**DoD antes de redigir:**
Antes de escrever o stage N, enuncie em voz alta: *"Stage N está pronto quando [X] existe e [Y] é verdadeiro."* Se não consegue enunciar, o stage está mal definido — redesenhe antes de continuar.

**Regra da amnésia:**
Para cada stage, pergunte: *"Se um agente completamente diferente abrisse este prompt sem contexto algum, ele teria tudo que precisa?"* Se não, o CONTEXTO HERDADO está frouxo.

## Contexto estável forte — checklist

O usuário paga o preço da chain se o contexto estável estiver incompleto. Inclua sempre que aplicável:

- [ ] Caminho absoluto do workspace (não relativo)
- [ ] Ambiente alvo (Claude Code / Cowork / Chat) — muda as tools disponíveis
- [ ] Design system / tokens inline no prompt (não "ver arquivo X")
- [ ] Voz e tom da marca (se relevante)
- [ ] Compliance / regras invioláveis (se houver)
- [ ] Convenções (naming, formato de data, idioma)
- [ ] Objetivo final da chain (não só deste stage)

## Exemplo mínimo — chain de 2 stages

Cenário: refatorar `styles.css` + validar responsivo.

**Stage 1 — o que o usuário cola:**

````markdown
# STAGE 1/2 — REFATORAR CSS
# Chain: "CSS Cleanup + Responsivo"

## CHAIN META
- Total stages: 2
- Current stage: 1/2
- Stage 1: extrair tokens + consolidar duplicações
- Stage 2: testar viewports + ajustes finais

## WORKSPACE
Absolute path: `/Users/nome/projeto/`
Ambiente alvo: Claude Code

## CONTEXTO HERDADO

### Objetivo da chain
Reduzir styles.css de 1200 → < 600 linhas mantendo output visual idêntico em 320px, 768px e 1440px.

### Decisões já tomadas
- Usar CSS custom properties (não Sass)
- Manter convenção BEM
- Sem pré-processadores

### Estado atual auditado (2026-04-23)
- ✅ EXISTE: styles.css (1247 linhas, muitas duplicações)
- ❌ NÃO EXISTE: arquivo de tokens

## TAREFA DESTE STAGE
1. Mapear seletores duplicados em styles.css
2. Extrair valores repetidos para custom properties em :root
3. Consolidar regras equivalentes
4. Salvar resultado — deve estar < 700 linhas

## RESTRIÇÕES
- Não alterar output visual (mesma hierarquia, mesmas cores finais)
- Não remover seletores usados no HTML

## DELIVERABLES
1. styles.css refatorado
2. Bloco `### PRÓXIMO PROMPT — STAGE 2`

## PROPAGATION PROTOCOL
[...instrução completa como no template...]
````

**Stage 2 — emitido pelo agente que rodou o Stage 1**, já com:
- Estado atual atualizado (styles.css agora tem X linhas, Y tokens extraídos)
- TAREFA trocada para validação responsiva
- PROPAGATION PROTOCOL substituído por FINAL TERMINATION (próxima emissão será `### CHAIN COMPLETE`)

## Sinal de skill bem aplicada

A chain está bem montada quando:

- Cada prompt emitido é colável cold em chat novo sem edição manual
- O último stage emite `### CHAIN COMPLETE` com todos os deliverables listados
- O usuário não precisou explicar nada de novo entre stages
- Se um stage falhou, emitiu `### CHAIN PAUSED` com pergunta direta — não adivinhou

O valor da skill: o usuário passa de *"preciso explicar de novo cada vez que abro um chat"* para *"colou, chain rodou"*.
