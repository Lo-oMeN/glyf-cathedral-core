---
name: gateway-modifier
description: Modify and extend NanoClaw or OpenClaw gateway cores. Fork the 500-line secure container, strip Anthropic-specific hooks, wire custom inference shims, and maintain the CLI wizard intact. Use when (1) forking NanoClaw for custom deployment, (2) removing cloud-dependent API calls, (3) adding local inference routing as default path, (4) extending the agent loop with custom middleware, (5) preserving the onboarding wizard while changing the inference backend.
---

# Gateway Modifier Skill

## Purpose

Transform NanoClaw from a cloud-dependent gateway into a sovereign edge-native agent platform. Strip the proprietary hooks while keeping the robust messaging core and onboarding experience.

## The Fork Strategy

### Step 1: Clone and Analyze

```bash
git clone https://github.com/qwibitai/nanoclaw.git
cd nanoclaw
npm install
```

Key files to understand:
- `src/core/agent.ts` — Main agent loop
- `src/inference/provider.ts` — Anthropic API calls
- `src/channels/` — Telegram/Discord/Slack handlers
- `src/cli/wizard.ts` — Onboarding wizard
- `src/memory/` — Persistence layer

### Step 2: Strip Anthropic Hooks

Remove from `src/inference/provider.ts`:
```typescript
// REMOVE: Direct Anthropic SDK imports
import Anthropic from '@anthropic-ai/sdk';

// REMOVE: API key requirement for cloud
const ANTHROPIC_API_KEY = process.env.ANTHROPIC_API_KEY;

// REPLACE with local inference
const LOCAL_MECHANICS_URL = process.env.LOCAL_MECHANICS_URL || 'http://mechanics:8080';
```

### Step 3: Add Mechanics Shim

```typescript
// src/inference/mechanics.ts
import { OpenAI } from 'openai';

export class MechanicsProvider {
  private client: OpenAI;
  
  constructor(baseURL: string) {
    this.client = new OpenAI({
      baseURL,
      apiKey: 'local-mechanics' // Not used but required by SDK
    });
  }
  
  async generate(messages: Message[], tools?: Tool[]): Promise<Response> {
    // Use OpenAI SDK with your local mechanics
    return this.client.chat.completions.create({
      model: 'local-mechanics',
      messages,
      tools,
      stream: true
    });
  }
}
```

### Step 4: Modify Agent Loop

Update `src/core/agent.ts`:
```typescript
// BEFORE
import { AnthropicProvider } from './inference/provider';
const inference = new AnthropicProvider();

// AFTER
import { MechanicsProvider } from './inference/mechanics';
const inference = new MechanicsProvider(
  process.env.LOCAL_MECHANICS_URL || 'http://mechanics:8080'
);
```

## Scripts

### `scripts/fork_nanoclaw.sh` — Automated Fork

```bash
./scripts/fork_nanoclaw.sh \
  --upstream https://github.com/qwibitai/nanoclaw \
  --name cathedral-gateway \
  --inference-url http://mechanics:8080
```

### `scripts/patch_inference.py` — Code Patcher

Applies surgical patches to NanoClaw source:
```bash
python scripts/patch_inference.py \
  --source ./nanoclaw \
  --mechanics-url http://mechanics:8080
```

## Preserving the Wizard

The CLI wizard (`src/cli/wizard.ts`) handles onboarding. Keep it intact but add detection:

```typescript
// Add to wizard.ts
async function detectLocalMechanics(): Promise<boolean> {
  try {
    const response = await fetch('http://mechanics:8080/health');
    return response.ok;
  } catch {
    return false;
  }
}

// In onboarding flow
const hasLocalMechanics = await detectLocalMechanics();
if (hasLocalMechanics) {
  console.log(chalk.green('✓ Local mechanics detected — routing all agents to edge-native inference'));
  config.inference.provider = 'local';
  config.inference.baseURL = 'http://mechanics:8080';
} else {
  console.log(chalk.yellow('⚠ No local mechanics found — falling back to Ollama'));
  config.inference.provider = 'ollama';
  config.inference.baseURL = 'http://ollama:11434';
}
```

## Configuration Schema

Modified `config.schema.json`:
```json
{
  "inference": {
    "type": "object",
    "properties": {
      "provider": {
        "enum": ["local-mechanics", "ollama", "anthropic"],
        "default": "local-mechanics"
      },
      "baseURL": {
        "type": "string",
        "default": "http://mechanics:8080"
      }
    }
  }
}
```

## Middleware Extension Points

Add custom middleware to the agent loop:

```typescript
// src/middleware/phi-modulator.ts
export function phiModulator(context: AgentContext) {
  // Modify requests based on φ-scaled timing
  const phi = 1.618033988749895;
  const now = Date.now();
  const phase = (now % (phi * 1000)) / (phi * 1000);
  
  context.metadata.phiPhase = phase;
  return context;
}

// In agent loop
const context = await phiModulator(initialContext);
```

## Testing the Modified Gateway

```bash
# Run unit tests
npm test

# Integration test with local mechanics
MECHANICS_URL=http://localhost:8080 npm run test:integration

# E2E test with Telegram bot
TELEGRAM_TOKEN=test npm run test:e2e
```

## References

- **NanoClaw architecture**: See `references/nanoclaw_architecture.md`
- **Agent loop internals**: See `references/agent_loop.md`
- **Channel handlers**: See `references/channel_implementations.md`

## See Also

- `openai-api-translation` skill — The mechanics OpenAI shim
- `docker-orchestration` skill — Deploying the modified gateway
