# prompt-chain

**Break complex multi-step tasks into self-propagating prompts that survive context limits.**

[Install](#install) • [How it works](#how-it-works) • [When to use](#when-to-use) • [Why](#why)

---

A Claude skill for chaining work across fresh chat sessions. Each prompt
generates the next, carrying full context forward. Cold-start safe.
Context-limit immune.

## How it works

| Without prompt-chain | With prompt-chain |
|----------------------|-------------------|
| One mega-prompt, context fills up, output degrades, you lose state when the chat dies. | A first prompt sets the chain. Each chat finishes its phase and outputs the next self-contained prompt. You paste it into a new chat. State carries. |

Same work. Half the friction. No mid-session collapse.

## Install

```bash
# Via skills CLI (recommended)
npx skills add 1marcelserrano/prompt-chain

# Or manually
git clone https://github.com/1marcelserrano/prompt-chain.git
cp -r prompt-chain/skills/prompt-chain ~/.claude/skills/
```

## When to use

Trigger phrases (EN + PT-BR):

- "execute in stages across separate chats"
- "split this across sessions"
- "self-propagating prompt"
- "prompt that generates the next"
- "chain of prompts"
- "cold start between chats"
- "executar por etapas em chats separados"
- "cada etapa em um novo chat"
- "prompt autocontido autopropagante"

Natural language works too. Just describe the multi-phase task and ask
for it to be split.

## Why

- **Context limits stop being a wall.** Each phase runs in a fresh session with only what it needs.
- **Phases isolate failures.** A broken phase 3 doesn't poison phases 4-7.
- **Resumable.** Lost the chat? Open the last good prompt, continue.
- **Hand-offable.** Each prompt is self-contained — you or someone else can pick up any link.

## What it does / doesn't

| Does | Doesn't |
|------|---------|
| Break P0 → P1 → P2 → ... structure | Execute the phases for you |
| Pass context forward via prompt text | Use external state stores |
| Auto-detect chainable patterns | Force-chain trivial single-step tasks |
| Work in any chat-based Claude interface | Require a specific platform |

## Contributing

PRs welcome. See [CONTRIBUTING.md](./CONTRIBUTING.md).

## License

MIT — see [LICENSE](./LICENSE).

---

<sub>Forged at [MSCREATIVE.SYSTEMS™](https://mscreative.systems) — Barcelona</sub>
