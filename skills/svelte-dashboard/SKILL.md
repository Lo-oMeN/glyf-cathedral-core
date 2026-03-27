---
name: svelte-dashboard
description: Build Svelte-based control plane dashboards for agent systems. Live status monitoring, message history viewer, rule editor, model swapper, and canvas for mechanics outputs. Embeds as the WebUI layer in the unified stack. Use when (1) creating the cathedral control plane interface, (2) building real-time agent status dashboards, (3) implementing message history with search and filtering, (4) creating rule/trigger configuration UIs, (5) visualizing 96-byte lattice states or geometric outputs from mechanics.
---

# Svelte Dashboard Skill

## Purpose

Create the control plane interface for the cathedral. Real-time status, message history, rule configuration, and geometric visualization — all in a lightweight Svelte app served from the gateway.

## Architecture

```
┌──────────────────────────────────────────┐
│           Svelte Dashboard               │
│                                          │
│  ┌──────────┐  ┌──────────┐  ┌─────────┐│
│  │  Status  │  │ History  │  │  Rules  ││
│  │  Panel   │  │  Viewer  │  │ Editor  ││
│  └──────────┘  └──────────┘  └─────────┘│
│                                          │
│  ┌─────────────────────────────────────┐ │
│  │         Canvas/Visualizer           │ │
│  │     (96-byte lattice display)       │ │
│  └─────────────────────────────────────┘ │
└──────────────────────────────────────────┘
```

## Quick Start

```bash
# Create new dashboard
cd /root/.openclaw/workspace/skills/svelte-dashboard/assets/template
npm install
npm run dev

# Or generate from template
node scripts/generate_dashboard.js --name cathedral-ui --output ./my-dashboard
```

## Core Components

### 1. Status Panel (`src/lib/StatusPanel.svelte`)

```svelte
<script>
  import { onMount } from 'svelte';
  
  let status = {
    mechanics: 'unknown',
    gateway: 'unknown',
    lastHeartbeat: null
  };
  
  onMount(async () => {
    const ws = new WebSocket('ws://gateway:8080/ws/status');
    ws.onmessage = (event) => {
      status = JSON.parse(event.data);
    };
  });
</script>

<div class="status-panel">
  <div class="indicator {status.mechanics}">
    Mechanics: {status.mechanics}
  </div>
  <div class="indicator {status.gateway}">
    Gateway: {status.gateway}
  </div>
  <div class="timestamp">
    Last heartbeat: {status.lastHeartbeat?.toLocaleTimeString()}
  </div>
</div>
```

### 2. Message History (`src/lib/MessageHistory.svelte`)

```svelte
<script>
  let messages = [];
  let filter = '';
  
  $: filteredMessages = messages.filter(m => 
    m.content.toLowerCase().includes(filter.toLowerCase())
  );
</script>

<div class="message-history">
  <input bind:value={filter} placeholder="Search messages..." />
  
  <div class="message-list">
    {#each filteredMessages as msg}
      <div class="message {msg.role}">
        <span class="timestamp">{msg.timestamp}</span>
        <span class="role">{msg.role}</span>
        <p class="content">{msg.content}</p>
      </div>
    {/each}
  </div>
</div>
```

### 3. Rule Editor (`src/lib/RuleEditor.svelte`)

```svelte
<script>
  let rules = [];
  let newRule = { trigger: '', action: '' };
  
  async function saveRule() {
    await fetch('/api/rules', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newRule)
    });
    rules = [...rules, newRule];
    newRule = { trigger: '', action: '' };
  }
</script>

<div class="rule-editor">
  <h3>Agent Rules</h3>
  
  <div class="new-rule">
    <input bind:value={newRule.trigger} placeholder="When..." />
    <input bind:value={newRule.action} placeholder="Then..." />
    <button on:click={saveRule}>Add Rule</button>
  </div>
  
  <div class="rules-list">
    {#each rules as rule, i}
      <div class="rule">
        <span>When: {rule.trigger}</span>
        <span>Then: {rule.action}</span>
        <button on:click={() => deleteRule(i)}>×</button>
      </div>
    {/each}
  </div>
</div>
```

### 4. Lattice Visualizer (`src/lib/LatticeVisualizer.svelte`)

```svelte
<script>
  import { onMount } from 'svelte';
  
  let canvas;
  let latticeState = new Array(96).fill(0);
  
  onMount(() => {
    const ctx = canvas.getContext('2d');
    drawLattice(ctx, latticeState);
  });
  
  function drawLattice(ctx, state) {
    const phi = 1.618033988749895;
    const goldenAngle = 137.507764;
    
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Draw 96-byte lattice as φ-spiral
    for (let i = 0; i < 96; i++) {
      const angle = i * goldenAngle * (Math.PI / 180);
      const radius = 10 * Math.pow(phi, i / 16);
      
      const x = canvas.width/2 + radius * Math.cos(angle);
      const y = canvas.height/2 + radius * Math.sin(angle);
      
      const intensity = state[i] / 255;
      ctx.fillStyle = `rgba(255, 215, 0, ${intensity})`;
      ctx.beginPath();
      ctx.arc(x, y, 3, 0, Math.PI * 2);
      ctx.fill();
    }
  }
</script>

<canvas 
  bind:this={canvas} 
  width="400" 
  height="400"
  class="lattice-canvas"
/>
```

## API Integration

### Dashboard ↔ Gateway Communication

```typescript
// src/lib/api.ts
export const api = {
  async getStatus() {
    const res = await fetch('/api/status');
    return res.json();
  },
  
  async getMessages(limit = 100) {
    const res = await fetch(`/api/messages?limit=${limit}`);
    return res.json();
  },
  
  async getRules() {
    const res = await fetch('/api/rules');
    return res.json();
  },
  
  async updateRule(id: string, rule: Rule) {
    const res = await fetch(`/api/rules/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(rule)
    });
    return res.json();
  },
  
  subscribeToStatus(callback: (status: Status) => void) {
    const ws = new WebSocket('ws://' + window.location.host + '/ws/status');
    ws.onmessage = (event) => callback(JSON.parse(event.data));
    return () => ws.close();
  }
};
```

## Styling (Cathedral Theme)

```css
/* src/app.css */
:root {
  --bg-void: #0a0a0a;
  --gold-primary: #FFD700;
  --gold-dim: #B8860B;
  --text-primary: #e0e0e0;
  --text-secondary: #888888;
  --accent-phi: #DAA520;
}

body {
  background: var(--bg-void);
  color: var(--text-primary);
  font-family: 'Inter', sans-serif;
}

.status-indicator {
  border-radius: 50%;
  width: 12px;
  height: 12px;
}

.status-indicator.healthy { background: var(--gold-primary); }
.status-indicator.degraded { background: var(--gold-dim); }
.status-indicator.down { background: #ff4444; }
```

## Building for Production

```bash
# Static build for embedding in gateway
npm run build

# Output: build/ directory with index.html and static assets
# Gateway serves this at /ui/ route
```

## Assets

The skill includes a complete starter template in `assets/template/`:
- SvelteKit project structure
- Pre-built components (Status, History, Rules, Visualizer)
- Cathedral theme styling
- WebSocket integration
- API client utilities

## References

- **Svelte tutorial**: See `references/svelte_basics.md`
- **WebSocket patterns**: See `references/websocket_integration.md`
- **Canvas visualization**: See `references/canvas_drawing.md`

## See Also

- `gateway-modifier` skill — Adding dashboard routes to NanoClaw
- `docker-orchestration` skill — Serving the built dashboard
