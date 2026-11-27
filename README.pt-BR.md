# Prompt Chain

**Quando um trabalho é grande demais para uma conversa só, o Claude divide em etapas e escreve um texto pronto para cada uma. Você cola cada texto numa conversa nova, e nada se perde pelo caminho.**

[Página de apresentação](https://mscreative.systems/arsenal/prompt-chain) • [Instalar](#instalar) • [Como usar](#como-usar) • [Se der errado](#se-der-errado) • [O que foi testado](#o-que-foi-testado) • [Comunidade](#comunidade-gratuita)

Este arquivo é para quem nunca instalou uma skill. A versão técnica, em inglês, está no [README.md](./README.md).

---

Uma skill é um conjunto de instruções que ensina o Claude a fazer uma tarefa do jeito certo. Você instala uma vez e depois chama pelo nome. Esta ensina o Claude a quebrar um trabalho de várias fases em etapas e a escrever, para cada etapa, um texto (um prompt, que é o texto que você manda para o Claude) que se explica sozinho. Você não precisa saber programar.

## Antes e depois

| Antes | Depois |
|-------|--------|
| Você pede tudo numa conversa só. Ela fica longa, o Claude passa a responder pior e, se o chat acaba, você perde o ponto onde estava. | O primeiro texto abre a cadeia. Cada conversa fecha a sua etapa e entrega o texto da próxima, já com o contexto dentro. Você cola numa conversa nova e segue. |

Cada texto leva junto o que importa: o que foi pedido, o que já foi decidido, o que o Claude pode ou não fazer. Se você perder uma conversa, abra o último texto bom e continue. Se quiser passar uma etapa para outra pessoa, ela consegue assumir só com o texto.

## Instalar

Leva uns três minutos, sem terminal.

**O que você precisa ter:**

- Uma conta no Claude, no site ou no aplicativo para computador.
- Nas configurações do Claude, a opção de executar código e criar arquivos ligada (em inglês, "Code execution and file creation"). O Claude pede isso para aceitar skills enviadas.
- Se o seu Claude é da empresa, o administrador pode precisar liberar o envio de skills.

**Passo a passo:**

1. [Baixe o arquivo prompt-chain.skill](https://github.com/1marcelserrano/prompt-chain/raw/main/prompt-chain.skill). Guarde onde for fácil achar, como a pasta Downloads.
2. Abra o Claude e entre em Customize, o menu onde ficam as suas skills.
3. Clique em + Add e escolha enviar uma skill (Upload a skill). Selecione o arquivo baixado.
4. Confira se a chave ao lado de prompt-chain está ligada.

Se o Claude recusar o arquivo, troque o final do nome de `.skill` para `.zip` e envie de novo.

<details>
<summary>Para quem já usa o terminal</summary>

```bash
npx skills add 1marcelserrano/prompt-chain
```

Ou, copiando a pasta à mão:

```bash
git clone https://github.com/1marcelserrano/prompt-chain.git
cp -r prompt-chain/skills/prompt-chain ~/.claude/skills/
```

Para conferir, abra uma sessão nova do Claude Code e pergunte "que skills você tem?". A prompt-chain deve aparecer na lista.

</details>

## Como usar

1. **Abra uma conversa nova** e escreva: "executar por etapas em chats separados".
2. **Descreva o trabalho** que você quer dividir, com as suas palavras. Pode ser uma pesquisa seguida de um resumo e de um texto, uma reforma de documentos, um lançamento.
3. **Receba o plano das etapas** e o primeiro texto pronto. Copie esse texto.
4. **Abra uma conversa nova e cole.** Quando aquela conversa terminar a etapa dela, ela entrega o texto da seguinte. Repita até o fim.

Outras frases que ativam a skill: "cada etapa em um novo chat", "prompt que gera o próximo", "um prompt por pendência", "prompt autocontido autopropagante". Em linguagem natural também deve funcionar: descreva o trabalho de várias fases e peça para dividir em etapas, uma por conversa.

## Dois modos

O Claude escolhe o modo com uma pergunta: as partes dependem do resultado umas das outras?

| Modo | Quando serve | Como você usa |
|------|--------------|---------------|
| Cadeia (CHAIN) | Uma etapa precisa da anterior, como pesquisar, resumir e depois escrever | Cada etapa termina entregando o texto da seguinte, até fechar |
| Paralelo (FAN-OUT) | As partes não dependem umas das outras e só dividem o mesmo contexto | Cada parte tem o seu texto, em qualquer ordem, e um texto final junta os resultados quando preciso |

Se alguma etapa travar por falta de informação ou de autorização, a cadeia para e pergunta. Ela não chuta.

## Se der errado

| Problema | O que fazer |
|----------|-------------|
| A skill não aparece na lista | Confira se a chave ao lado dela está ligada e se a opção de executar código e criar arquivos está ligada nas configurações. Em conta de empresa, o administrador pode ter desligado o envio de skills. |
| O Claude recusou o arquivo | Troque o final do nome de `.skill` para `.zip` e envie de novo. |
| O Claude não dividiu o trabalho em etapas | Abra uma conversa nova e escreva: divida este trabalho em etapas, uma por conversa. |
| Você perdeu uma conversa no meio da cadeia | Abra o último texto que funcionou e cole numa conversa nova. Cada texto se explica sozinho. |

## O que ela faz e o que não faz

| Faz | Não faz |
|-----|---------|
| Divide o trabalho em etapas, cada uma com a sua entrega | Não executa as etapas por você, quem cola cada texto numa conversa nova é você |
| Escreve, para cada etapa, um texto que se explica sozinho e leva junto o que importa da anterior | Não serve para tarefa de um passo só, nem para explorar sem saber o que entregar |
| Escolhe entre cadeia e paralelo conforme o trabalho | Não substitui os ajudantes em paralelo (subagentes) quando tudo cabe numa conversa só |
| Mantém o peso de cada coisa: o que é fato, sugestão, decisão sua ou autorização não muda de status ao passar de uma conversa para outra | Não amplia permissão de uma etapa para a outra |

## Para quem é

Para quem toca trabalho longo com IA e já viu a conversa perder o fio no meio, ou precisa passar uma etapa para outra pessoa, outro modelo ou outro dia.

## Privacidade

A skill não guarda nada e não usa nenhum serviço externo. Os textos que ela escreve vão para onde você colar, então evite colocar dados sensíveis num texto que vai para uma conversa de outra pessoa.

## O que foi testado

Sem rodeio, para você saber no que está pisando:

- O pacote da skill e o repositório passam nos testes automáticos do projeto (veja o [CHANGELOG](./CHANGELOG.md)).
- O mesmo caminho de envio (Customize, Skills, + Add, Upload a skill) foi testado pelo autor com outra skill, a Fila de Prioridades: o Claude aceitou o arquivo `.skill` direto, sem renomear, e a skill já entrou ativada.
- **Ainda não provado:** o envio do `prompt-chain.skill` em si, a frase "executar por etapas em chats separados" numa conta de verdade e um passo a passo seguido por quem não é o autor.

## Comunidade gratuita

Se você quer construir skills como essa, e conversar com quem está fazendo o mesmo, entre na comunidade gratuita:

**[Entrar na comunidade no Skool](https://www.skool.com/marcel-1662/about)**

## Conhecer por dentro

Exemplos de cadeias e de paralelo, modelos para começar e a comparação com outras ferramentas estão no [README em inglês](./README.md). O texto completo da skill em português está em [skills/prompt-chain/SKILL.pt-BR.md](./skills/prompt-chain/SKILL.pt-BR.md).

## Contribuir

Pull requests são bem-vindos. Veja o [CONTRIBUTING.md](./CONTRIBUTING.md).

## Licença

MIT. Veja o [LICENSE](./LICENSE).

---

<sub>Forged at [MSCREATIVE.SYSTEMS™](https://mscreative.systems), Barcelona</sub>
