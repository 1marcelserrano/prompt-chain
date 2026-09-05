---
name: prompt-chain
description: >-
  Monta prompts autocontidos para trabalhos que precisam atravessar chats
  isolados sem perder contexto nem autoridade. Use CHAIN quando cada stage
  depende do output anterior e deve emitir o próximo prompt cold-start. Use
  FAN-OUT quando peças independentes precisam de um prompt cada, possivelmente
  seguidas por um collector. Dispara em pedidos como "prompt que gera o
  próximo", "cada etapa em um chat novo", "um prompt por tarefa", "handoff
  cold-start", "executar por etapas em chats separados" ou "um prompt por
  pendência". Não use para tarefa direta de um passo, exploração aberta ou
  subagentes paralelos na mesma sessão.
license: MIT
metadata:
  version: "2.3.0"
---

# Prompt Chain

Transforma uma tarefa multi-etapas em prompts autocontidos, cada um rodando em um chat novo com o contexto completo carregado. Dois modos:

- **CHAIN** — sequencial. Cada prompt executa um stage e termina emitindo o prompt do próximo stage com o contexto acumulado já dentro dele. O usuário copia e cola entre chats; a chain se propaga sozinha até `CHAIN COMPLETE`. Use quando as peças têm dependência de ordem.
- **FAN-OUT** — independente. Um prompt autocontido por peça, todos compartilhando o mesmo contexto estável mas sem propagação entre eles. O usuário abre cada um no seu próprio chat, em qualquer ordem (ou ao mesmo tempo). Use quando as peças não dependem umas das outras.

**Prompts carregam trabalho, não autoridade ampliada.** Fatos, propostas, decisões do operador e permissões mantêm seu status ao atravessar chats. Um stage posterior não pode promover silenciosamente uma conclusão do modelo a decisão do operador nem ampliar uma autorização.

## Dois modos — como rotear

Faça uma pergunta: **as peças dependem do output ou do estado uma da outra?**

- **Sim → CHAIN.** O Stage 2 precisa do que o Stage 1 produziu (refatorar → validar; outline → draft; pesquisar → sintetizar). A ordem carrega peso, então o estado dinâmico precisa viajar pra frente.
- **Não → FAN-OUT.** Cada peça é uma tarefa fechada que apenas compartilha contexto estável (propagar uma decisão em três repos; corrigir cinco achados de auditoria não relacionados; um prompt por pendência). Sem ordem, sem estado dinâmico compartilhado.

Casos de borda:
- **Quase tudo independente, uma dependência** → FAN-OUT para as peças independentes + uma CHAIN curta para o par dependente, tratada como uma peça do fan-out. Não force tudo a ser sequencial.
- **Mesma sessão, paralelo de verdade, sem necessidade de isolamento** → não é esta skill. Use subagents em paralelo — eles rodam concorrentes dentro de uma sessão. FAN-OUT é pra quando você quer especificamente *chats isolados* (cold start, hand-off, pessoas / modelos / momentos diferentes) sem dependência de ordem.

Tudo daqui até "Modo FAN-OUT" descreve CHAIN. A seção FAN-OUT cobre só o que muda para prompts independentes.

## Quando usar

- Tarefa grande com fases distintas (P0 → P1 → P2), cada uma com entregáveis próprios
- Usuário quer isolar contexto entre etapas (novo chat = memória limpa, cache frio, execução isolada)
- Usuário pede explicitamente "um prompt que gera o próximo" (CHAIN) ou "um prompt por tarefa / por pendência" (FAN-OUT)
- Trabalho que se beneficia de pausar entre stages para revisar output antes de continuar
- Várias peças independentes que compartilham contexto e cada uma merece um chat isolado e hand-offable (FAN-OUT)
- Ambientes onde o mesmo agente não pode rodar tudo (limite de sessão, política de auditoria, troca de modelo)

## Quando NÃO usar

- Tarefa de um passo só → resolva direto, sem overhead
- Tarefa cujo estado intermediário cabe numa sessão sem risco de estouro → uma lista de tarefas mais execução direta é melhor
- Tarefa exploratória sem entregáveis discretos → ambos os modos pressupõem peças com Definition of Done claro
- Paralelismo na mesma sessão sem necessidade de chats isolados → use subagents em paralelo (rodam concorrentes numa sessão). Querer chats *isolados* para peças sem dependência de ordem não é motivo pra evitar a skill — isso é o modo FAN-OUT

## Mental model

Uma chain é uma sequência de stages. Cada stage:
1. Recebe um prompt autocontido (pasteável cold em chat novo)
2. Executa uma fatia do trabalho
3. Emite o prompt do próximo stage com contexto atualizado

Separe **contexto estável de contexto dinâmico**.

- **Estável** — workspace path, design system, voz da marca, restrições globais, objetivo final. Copiado verbatim em todos os stages.
- **Dinâmico** — estado atual dos arquivos, decisões tomadas, bloqueios encontrados. Atualizado stage a stage.

Se a chain perder contexto estável, o próximo chat refaz decisões. Se perder contexto dinâmico, refaz trabalho. Ambas as falhas destroem o valor.

No modo **FAN-OUT** não há carry-forward dinâmico — cada prompt é contexto estável mais uma tarefa fechada. Isso faz do contexto estável a *única* coisa mantendo as peças coerentes, então completá-lo bem importa ainda mais (ver "Modo FAN-OUT" abaixo).

## Como montar uma chain

### Passo 1 — Enquadre o trabalho e extraia contexto estável

Antes de decompor, separe:

- **Pedido original, verbatim** — as palavras do operador, não um resumo do plano.
- **Objetivo final** — o que significa "chain completa"? Enunciado único e verificável.
- **Classe e risco do trabalho** — produção, pessoal/pré-produção ou one-shot; o que um revert não desfaz.
- **Orçamento / checkpoint** — o limite de fatia ou tempo e o que acontece quando ele chega.
- **Undo** — como reverter o trabalho se o stage estiver errado.
- **Workspace** — caminho absoluto + convenções (pasta de escrita, naming, idioma).
- **Restrições que não mudam** — design system, compliance, voz da marca, formato de output.
- **Autoridade** — o que está autorizado, o que exige nova aprovação e o que está fora de escopo.
- **Decisões do operador** — apenas o que o usuário definiu explicitamente e não será reaberto.
- **Ambiente alvo e audiência** — o que o próximo chat acessa e quem receberá o prompt.

O frame e o bloco de autoridade entram em todos os stages sem mudança. Fatos observados, propostas do stage, estado atual e tentativas falhas são dinâmicos; seus rótulos viajam junto.

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

## WORK FRAME — COPIAR VERBATIM

### Pedido original
> [as palavras exatas do operador]

### Feito
[enunciado único e verificável do que completa a chain]

### Classe e risco do trabalho
[produção / pessoal-pré-produção / one-shot; baixo / médio / alto; o que um revert não desfaz]

### Orçamento / checkpoint
[limite de fatia ou tempo; retornar ao coordenador quando chegar]

### Undo
[como reverter este trabalho]

### Coordenador
[chat, pessoa ou papel que revisa o relatório de cada stage e autoriza continuação]

## WORKSPACE
Absolute path: `[caminho absoluto]`
Ambiente alvo: [agente com acesso ao workspace / agente só de chat / outro cliente nomeado]
[Destino / audiência: quem recebe este prompt e o que consegue acessar]
[Convenções relevantes: pasta de escrita, naming, idioma]

## AUTORIDADE — COPIAR VERBATIM
- Autorizado nesta chain: [ações exatas permitidas pelo pedido original]
- Exige nova aprovação: [publicar / enviar / abrir PR / push / deploy / merge / pagar / excluir / mudar permissões, salvo autorização exata acima]
- Fora de escopo: [superfícies e ações que esta chain não toca]

## CONTEXTO HERDADO — LEITURA OBRIGATÓRIA

### Objetivo da chain
[Enunciado único do que significa chain completa]

### Decisões do operador — congeladas
- [somente decisão explícita 1 do operador — não reabrir]
- [somente decisão explícita 2 do operador — não reabrir]

### Fatos observados
- [fato sustentado por evidência; incluir fonte ou caminho]

### Propostas do stage — não vinculantes até ratificação
- [recomendação ou julgamento produzido por um stage]

### Estado atual auditado ([YYYY-MM-DD])
- ✅ EXISTE: [arquivos criados por stages anteriores]
- ❌ NÃO EXISTE: [arquivos faltantes]
- ⚠️ [nuances, warnings, gotchas]
- ⛔ FAILED: [abordagens já tentadas que não funcionaram, com o erro — não repetir]

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
N. **OBRIGATÓRIO**: bloco `### RELATÓRIO DO STAGE AO COORDENADOR`
N+1. **OBRIGATÓRIO QUANDO O STATUS É COMPLETO**: bloco `### PRÓXIMO PROMPT — STAGE N+1` (ou `### CHAIN COMPLETE` se N = TOTAL). Quando o status é pausado, emitir `### CHAIN PAUSED` no lugar.

## PROPAGATION PROTOCOL — CRÍTICO
Quando o stage estiver completo, emita um bloco de código markdown contendo o prompt completo e autocontido para Stage N+1. Quando estiver pausado, emita `### CHAIN PAUSED` e nenhum prompt do próximo stage. O próximo chat terá ZERO memória deste. O prompt de Stage N+1 deve:

- Abrir com `# STAGE N+1/TOTAL — [NOME]`
- Copiar verbatim CHAIN META, WORK FRAME, WORKSPACE, AUTORIDADE e todo CONTEXTO HERDADO estável deste prompt
- Atualizar "Fatos observados", "Propostas do stage" e "Estado atual auditado" com o que você acabou de fazer
- Atualizar "Decisões do operador — congeladas" só com decisão explícita do usuário registrada neste stage; nunca promover uma proposta por conta própria
- Substituir TAREFA pela lista de ações do Stage N+1 (ver CHAIN META acima)
- Incluir o mesmo PROPAGATION PROTOCOL para Stage N+2 (ou substituir por FINAL TERMINATION se Stage N+1 for o último)
- Retornar o relatório do stage e o próximo prompt ao coordenador; não iniciar Stage N+1 neste chat

Se este stage não puder ser completado (bloqueio, ambiguidade, input faltante), emita no lugar do próximo prompt um bloco `### CHAIN PAUSED` (ver protocolos).
````

## Protocolos de transição

### PROPAGATION PROTOCOL (stage → próximo stage)

Toda resposta **completa** de stage não-final termina com o header abaixo. Uma resposta pausada usa `### CHAIN PAUSED` no lugar e não pode conter o prompt do próximo stage.

```
### PRÓXIMO PROMPT — STAGE N+1
```

Seguido por um bloco de código markdown fechado. **Atenção ao escape de fences**: como o conteúdo do próximo prompt contém crases triplas, use fence com **4 crases** no bloco externo (ou `~~~~` como alternativa). Isso evita que o parser feche o bloco cedo.

Princípios:
- **Nunca abrevie com "igual ao anterior"** — o próximo chat não tem o anterior
- **Copiar contexto estável verbatim é o comportamento correto**, não redundância
- **Mantenha os rótulos de autoridade** — atualize Fatos observados, Propostas do stage, Estado atual auditado, Abordagens falhas e TAREFA DESTE STAGE; nunca renomeie proposta como decisão do operador
- **Mantenha o PROPAGATION PROTOCOL intacto** dentro do próximo stage, apontando para o stage seguinte
- **Ajuste o "Current stage"** e atualize o DoD de Stage N+1 com base no que foi feito agora
- **Propague permissão exatamente** — uma autorização não se amplia porque um stage posterior se beneficiaria dela. Se o pedido original não autorizou o efeito externo exato, prepare o artefato e pause para aprovação
- **Minimize antes de propagar** — nunca copie credenciais, API keys ou tokens. Substitua por placeholder (`[API_KEY — no seu env]`). Dados pessoais ou confidenciais só viajam quando o destino nomeado precisa deles e está autorizado a recebê-los; caso contrário, redija ou referencie arquivo local acessível
- **Registre o que falhou** — acrescente à lista `⛔ FAILED` toda abordagem que este stage tentou e não funcionou, com o erro. Um chat novo sem memória vai repetir o beco sem saída de bom grado, a menos que o prompt proíba
- **Referencie arquivos em vez de colá-los** quando o ambiente alvo lê o workspace (Claude Code): passe caminhos, não conteúdo. Conteúdo inline só pra ambientes de chat puro (claude.ai, Cowork) onde a próxima sessão não abre arquivos
- **Vigie o orçamento de contexto** — se o contexto herdado passar de mais ou menos um terço do prompt, pode: mantenha decisões, estado atual e abordagens falhas; corte narração e tudo que o próximo chat consegue re-derivar dos arquivos

### RELATÓRIO DO STAGE AO COORDENADOR

Todo stage retorna antes da chain avançar. Emita este bloco antes do próximo prompt:

```markdown
### RELATÓRIO DO STAGE AO COORDENADOR

- Status: [completo / pausado]
- Entregáveis: [caminhos ou outputs]
- Evidência: [checks executados e resultado observado]
- Fatos observados adicionados: [...]
- Propostas do stage aguardando ratificação: [...]
- Decisões do operador registradas neste stage: [nenhuma / citar a decisão e seu escopo exato]
- Decisão ou aprovação necessária do operador: [nenhuma / uma pergunta estreita]
```

O coordenador revisa o relatório e pode aceitar o próximo prompt, revisá-lo ou parar. Um relatório com `Status: pausado` deve ser seguido por `CHAIN PAUSED`, nunca pelo prompt do próximo stage. Gerar o prompt de Stage N+1 nunca autoriza o chat atual a executar Stage N+1.

### PROTOCOLO DE AUTORIZAÇÃO

Efeitos externos incluem publicar, enviar mensagem, abrir PR, fazer push, deploy ou merge, gastar dinheiro, excluir dados e mudar acesso ou permissões. Execute um deles somente quando o pedido original ou decisão explícita posterior do operador autorizar esse efeito exato para este escopo. Sem autorização clara, prepare tudo que for reversível, nomeie a ação pendente no relatório e emita `CHAIN PAUSED` com uma pergunta única de aprovação.

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

**Refine durante a pausa:** se o ambiente consegue perguntar ao usuário interativamente, use essa capacidade naquele momento. Apresente o bloqueio como pergunta direta com 2–4 opções concretas, cada uma com seu trade-off, e aplique a resposta antes de emitir o prompt de retomada. Emita também o bloco `CHAIN PAUSED` para manter o estado portátil. Em ambientes sem pergunta interativa, use a pergunta escrita no bloco.

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
- Decisões do operador ratificadas: [...]
- Propostas do stage ainda aguardando ratificação: [...]
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
- [ ] Ambiente e cliente alvo — determinam as tools e os arquivos do workspace disponíveis
- [ ] Pedido original, ponto de feito, orçamento/checkpoint, undo e coordenador
- [ ] Autoridade exata: ações autorizadas, ações com nova aprovação e superfícies fora de escopo
- [ ] Design system / tokens inline no prompt em ambientes de chat puro; caminho de arquivo basta quando o ambiente alvo lê o workspace
- [ ] Voz e tom da marca (se relevante)
- [ ] Compliance / regras invioláveis (se houver)
- [ ] Convenções (naming, formato de data, idioma)
- [ ] Objetivo final da chain (não só deste stage)
- [ ] Decisões, fatos e propostas ficam em blocos separados
- [ ] Zero segredos; dados pessoais ou confidenciais são minimizados para o destino nomeado

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

## WORK FRAME — COPIAR VERBATIM

### Pedido original
> Refatore styles.css e valide o comportamento responsivo em stages cold-start separados. Não altere o resultado visual.

### Feito
styles.css fica abaixo de 600 linhas e renderiza de forma idêntica em 320px, 768px e 1440px.

### Classe e risco do trabalho
Pessoal/pré-produção; risco médio porque regressões visuais podem sobreviver a um build limpo.

### Orçamento / checkpoint
Dois stages. Retornar ao coordenador depois de cada um.

### Undo
Reverter o commit do stage ou restaurar styles.css pelo controle de versão.

### Coordenador
O chat que criou esta chain.

## WORKSPACE
Absolute path: `/Users/nome/projeto/`
Ambiente alvo: Claude Code

## AUTORIDADE — COPIAR VERBATIM
- Autorizado nesta chain: editar styles.css e rodar checks locais
- Exige nova aprovação: commit, push, deploy ou modificação do HTML
- Fora de escopo: markup, JavaScript, dependências e ambientes públicos

## CONTEXTO HERDADO

### Objetivo da chain
Reduzir styles.css de 1200 → < 600 linhas mantendo output visual idêntico em 320px, 768px e 1440px.

### Decisões do operador — congeladas
- Usar CSS custom properties (não Sass)
- Manter convenção BEM
- Sem pré-processadores

### Fatos observados
- styles.css tem 1247 linhas e valores repetidos

### Propostas do stage — não vinculantes até ratificação
- Nenhuma ainda

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
2. Bloco `### RELATÓRIO DO STAGE AO COORDENADOR`
3. Bloco `### PRÓXIMO PROMPT — STAGE 2`

## PROPAGATION PROTOCOL
[...instrução completa como no template...]
````

**Stage 2 — emitido pelo agente que rodou o Stage 1**, já com:
- Estado atual atualizado (styles.css agora tem X linhas, Y tokens extraídos)
- TAREFA trocada para validação responsiva
- PROPAGATION PROTOCOL substituído por FINAL TERMINATION (próxima emissão será `### CHAIN COMPLETE`)

## Modo FAN-OUT

Mesmo isolamento e segurança de cold-start de uma chain, menos a propagação. Use quando as peças compartilham contexto estável mas não dependem do output uma da outra — ver a regra de roteamento no topo.

### Como montar um fan-out

1. **Enquadre o conjunto uma vez** — leve o mesmo WORK FRAME, WORKSPACE, AUTORIDADE, decisões do operador e contexto estável para todas as peças.
2. **Liste as peças independentes** — uma linha cada, com seu próprio Definition of Done. Se duas peças acabam compartilhando estado dinâmico, elas não são independentes — colapse num CHAIN de 2 stages e trate essa chain como uma peça do fan-out.
3. **Redija um prompt autocontido por peça** — cada um carrega o contexto estável completo, a tarefa daquela peça e devolve um resultado estruturado ao coordenador. Sem CHAIN META, PROPAGATION PROTOCOL ou emissão de próximo prompt.
4. **Adicione um collector quando o conjunto tem resultado combinado** — síntese, resolução de conflitos ou veredito global dependem de todos os resultados exigidos. O collector é passo dependente depois do fan-out, não outra peça independente.
5. **Opcionalmente redija um dispatcher** — um prompt-raiz que guarda o contexto uma vez e emite os N prompts-peça, além do collector quando necessário. O dispatcher gera prompts; não os executa.

### Template canônico de prompt FAN-OUT

Copie-colando verbatim, ajustando o conteúdo. Toda peça do fan-out usa essa estrutura.

````markdown
# [NOME DA TAREFA] — peça K de N (independente)
# Conjunto: "[NOME DO FAN-OUT]"

## WORK FRAME — COPIAR VERBATIM
[Pedido original, Feito, Classe e risco, Orçamento / checkpoint, Undo, Coordenador]

## WORKSPACE
Absolute path: `[caminho absoluto]`
Ambiente alvo: [agente com acesso ao workspace / agente só de chat / outro cliente nomeado]
[Destino / audiência]
[Convenções: pasta de escrita, naming, idioma]

## AUTORIDADE — COPIAR VERBATIM
- Autorizado nesta peça: [ações exatas]
- Exige nova aprovação: [efeitos externos ainda não autorizados]
- Fora de escopo: [ações e superfícies intocáveis]

## CONTEXTO COMPARTILHADO — LEITURA OBRIGATÓRIA

### Decisões do operador — congeladas
- [somente decisões explícitas do operador]

### Fatos observados
- [fatos sustentados por evidência e compartilhados por todas as peças]

### Propostas compartilhadas — não vinculantes até ratificação
- [recomendação herdada do modelo relevante para todas as peças]

### Contexto estável compartilhado
[A especificação estável, design system, voz e restrições invioláveis. Idêntico em todos os N prompts.]

## TAREFA DESTA PEÇA
1. [ação concreta com critério de "feito"]
2. ...

## RESTRIÇÕES
- [o que NÃO fazer — arquivos intocáveis, decisões congeladas]

## DELIVERABLES
1. [arquivo / output]
2. O envelope de resultado abaixo

## RESULTADO PARA O COORDENADOR — OBRIGATÓRIO
- Peça: K de N — [nome]
- Status: [completa / bloqueada]
- Entregáveis: [caminhos ou outputs]
- Evidência: [checks executados e resultado observado]
- Fatos observados adicionados: [...]
- Propostas do stage aguardando ratificação: [...]
- Decisões do operador registradas nesta peça: [nenhuma / citar a decisão e seu escopo exato]
- Decisão ou aprovação necessária do operador: [nenhuma / uma pergunta estreita]

## NOTA DE INDEPENDÊNCIA
Este prompt é autocontido e não compartilha estado dinâmico com as outras peças de "[NOME DO FAN-OUT]". Rode no seu próprio chat, em qualquer ordem. Não há próximo prompt a emitir — quando a tarefa e os deliverables estiverem prontos, pare. Se travar, pergunte ao usuário direto (ver abaixo) em vez de adivinhar.
````

Uma peça de fan-out não tem CHAIN META, estado dinâmico compartilhado com outras peças, PROPAGATION PROTOCOL ou `CHAIN COMPLETE` por peça. Ela abre, faz sua tarefa fechada, devolve o envelope de resultado e termina.

### Dispatcher (prompt-raiz opcional)

Quando você quer que um chat gere o conjunto inteiro, use um dispatcher: enuncie o frame e o contexto estável uma vez, liste as N peças e instrua o agente a emitir N prompts autocontidos, sem propagação. Se houver resultado combinado, o dispatcher também emite um collector. Ele é gerador, não executor. Use fence com **4 crases** (ou `~~~~`) em cada bloco emitido.

### Collector (quando o conjunto tem resultado combinado)

Rode o collector somente depois de cada peça exigida devolver `RESULTADO PARA O COORDENADOR` ou o coordenador aceitar explicitamente uma ausência. Entregue a ele o frame original, o contexto compartilhado com todos os rótulos de status intactos e os envelopes — não os chats completos de produção.

```markdown
# COLLECTOR — [NOME DO FAN-OUT]

## WORK FRAME / WORKSPACE / AUTORIDADE / CONTEXTO COMPARTILHADO
[copiar os mesmos blocos verbatim, incluindo propostas compartilhadas não vinculantes]

## INPUTS EXIGIDOS
- Resultado da peça exigida 1: [colar RESULTADO PARA O COORDENADOR]
- Resultado da peça exigida 2: [colar RESULTADO PARA O COORDENADOR]
- ...
- Resultado da peça exigida N: [colar RESULTADO PARA O COORDENADOR]

## TAREFA
1. Verificar se toda peça exigida está presente ou foi dispensada explicitamente pelo coordenador.
2. Reconciliar conflitos, duplicações e lacunas sem inventar evidência ausente.
3. Produzir o entregável combinado e um relatório de conclusão do conjunto.

## CONCLUSÃO
Emitir `### SET COMPLETE` somente quando o enunciado de Feito combinado for verdadeiro. Caso contrário, emitir `### SET PAUSED` com uma pergunta estreita ao coordenador.
```

### CHAIN vs FAN-OUT num relance

| | CHAIN | FAN-OUT |
|---|---|---|
| Ordem | Sequencial, carrega peso | Nenhuma — qualquer ordem, até simultânea |
| Entre prompts | Cada um emite o próximo (propagação) | Nada — totalmente independentes |
| Estado dinâmico | Viaja stage a stage | Nenhum — só contexto estável |
| Conclusão | Último stage emite `CHAIN COMPLETE` | Cada peça devolve resultado; collector emite `SET COMPLETE` quando há resultado combinado |
| Bloqueio | `CHAIN PAUSED` (contamina downstream se adivinhar) | Cada prompt pausa sozinho; os outros não são afetados |
| Artefato de build | Um prompt-semente (Stage 1) | N prompts, opcionalmente dispatcher e collector |

### Bloqueios em fan-out

Cada prompt resolve seu bloqueio isolado. Uma peça travada devolve seu envelope com uma pergunta estreita enquanto as outras seguem. Use a capacidade de perguntar ao usuário do ambiente, quando houver; senão escreva a pergunta e pare. **Pausar ainda é melhor que adivinhar.** Credenciais e tokens nunca viajam. Dados pessoais ou confidenciais são minimizados para o destino nomeado.

### Sinal de fan-out bem aplicado

- Cada prompt-peça cola cold no seu próprio chat sem edição manual
- Todas as peças compartilham contexto estável *idêntico* — preencha uma vez, preencha bem
- Nenhuma peça espera por outra, e nenhuma referencia "o chat anterior"
- Toda peça devolve um envelope de resultado ao coordenador nomeado
- Um resultado combinado só fica completo quando o collector vê todos os resultados exigidos ou uma dispensa explícita
- Se você se pegar passando o output de uma peça pra outra, ela não era independente — devia ter sido uma CHAIN

## Sinal de skill bem aplicada

A chain está bem montada quando:

- Cada prompt emitido é colável cold em chat novo sem edição manual
- O último stage emite `### CHAIN COMPLETE` com todos os deliverables listados
- O usuário não precisou explicar nada de novo entre stages
- Se um stage falhou, emitiu `### CHAIN PAUSED` com pergunta direta — não adivinhou
- Nenhum stage ampliou autoridade nem promoveu proposta não ratificada a decisão do operador

O valor da skill: o usuário passa de *"preciso explicar de novo cada vez que abro um chat"* para *"colou, chain rodou"*.
