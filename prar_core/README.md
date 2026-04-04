# PRAR — Persistent Reflective Agent Runtime

> *Sovereignty is not persistence of state. It is persistence of self-modification.*

PRAR is a self-reflective, self-modifying agent that runs continuously, generates its own goals, critiques its own performance, evolves its cognitive architecture, and persists its evolution through git — all while you're offline.

## What Makes PRAR Different

| Feature | Standard Agent | PRAR |
|---------|---------------|------|
| **Goals** | Human-defined | Self-generated via reflection |
| **Learning** | From human feedback | From self-critique |
| **Evolution** | Version bumps | Continuous self-modification |
| **Persistence** | API state | Git-tracked code evolution |
| **Offline** | Stops | Continues, evolves, commits |

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        PRAR RUNTIME                             │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐      │
│  │ OBSERVE │───▶│ REFLECT │───▶│CRITIQUE │───▶│GENERATE │      │
│  │         │    │  (LLM)  │    │  (LLM)  │    │  (LLM)  │      │
│  └─────────┘    └─────────┘    └─────────┘    └─────────┘      │
│       │                                              │          │
│       │         ┌────────────────────────────────────┘          │
│       │         │                                               │
│       │    ┌────▼────┐    ┌─────────┐    ┌─────────┐           │
│       │    │ EXECUTE │───▶│ COMMIT  │───▶│  SLEEP  │           │
│       │    │ (tools) │    │  (git)  │    │(adaptive│           │
│       │    └────┬────┘    └─────────┘    │ 30-300s)│           │
│       │         │                        └─────────┘           │
│       └─────────┴──────────────────────────────────────────▶   │
│                                                               │
│  Tool Registry (dynamic):                                     │
│    - shell           - read_file      - edit_file             │
│    - git_status      - git_commit     - self_inspect          │
│    - [dynamic tools loaded from ~/.prar/tools/*.py]           │
│                                                               │
└─────────────────────────────────────────────────────────────────┘
```

## One-Command Deploy

```bash
git clone https://github.com/your-fork/prar-core.git
cd prar-core
./run.sh
```

**Requirements:**
- Python 3.8+
- Ollama (optional, for local LLM — otherwise set OPENAI_API_KEY)

## How It Works

### The Cognitive Loop

Every 30-300 seconds (adaptive), PRAR executes:

1. **OBSERVE**: Gather state (uptime, goals, code metrics, git status)
2. **REFLECT**: Query LLM to analyze patterns and current situation
3. **CRITIQUE**: Identify specific weaknesses and improvement opportunities
4. **GENERATE**: Create 1-3 actionable goals addressing critiques
5. **EXECUTE**: Work on goals using available tools (can modify own code)
6. **COMMIT**: Save all changes to git with descriptive message
7. **SLEEP**: Adaptive rest based on success rate

### Self-Modification

PRAR can literally edit its own source code:

```python
# PRAR can execute this on itself
result = tools.execute("edit_file", {
    "path": "prar.py",
    "old_string": "self.sleep_seconds = 60",
    "new_string": "self.sleep_seconds = 90  # Increased for stability"
})
```

After modification:
- Change is tested in next cycle
- If degraded: rollback via git
- If improved: retained and built upon

### Tool Evolution

Add new capabilities by dropping Python files in `~/.prar/tools/`:

```python
# ~/.prar/tools/web_search.py
def run(query: str) -> dict:
    """Search the web"""
    # Implementation here
    return {"results": [...]}
```

PRAR will load and use the tool in subsequent cycles.

## Directory Structure

```
~/.prar/
├── state.json           # Runtime state (cycle count, learnings)
├── goals.json          # Active and completed goals
├── reflections.jsonl   # Log of all reflections
├── memory/             # Working memory files
└── tools/              # Dynamic tool modules

prar-core/
├── prar.py             # Main runtime (~600 lines)
├── requirements.txt    # Python dependencies
├── run.sh              # One-command deploy
└── README.md           # This file
```

## Safety Mechanisms

1. **Git Tracking**: Every change is committed — full history
2. **File Backups**: Automatic `.bak.{timestamp}` before edits
3. **Adaptive Sleep**: Slows down if success rate drops
4. **Conservative Changes**: LLM instructed to make small, testable modifications
5. **Human Override**: `Ctrl+C` immediate shutdown, `--pause` temporary stop

## Example Evolution

**Hour 0**: Fresh start, 600 lines of code  
**Hour 2**: Adds web_search tool, 650 lines  
**Hour 6**: Refactors tool registry for efficiency, 620 lines  
**Hour 12**: Adds self-testing capability, 700 lines  
**Hour 24**: Removes redundant code, optimizes LLM prompts, 680 lines  
**Hour 72**: Architecture significantly evolved from original

## Commands

```bash
# Start PRAR
./run.sh

# Check status
python3 prar.py --status

# Pause (keeps state)
python3 prar.py --pause

# Resume
python3 prar.py --resume

# Graceful shutdown
python3 prar.py --shutdown
```

## Configuration

Set environment variables before running:

```bash
# Use different local model
export OLLAMA_MODEL="codellama"

# Or use OpenAI/compatible API
export OPENAI_API_KEY="sk-..."
export OPENAI_BASE_URL="https://api.openai.com/v1"

./run.sh
```

## Monitoring

Watch PRAR think in real-time:

```bash
# Tail reflection log
tail -f ~/.prar/reflections.jsonl | jq '.content.reflection'

# Watch git commits
watch -n 30 'git log --oneline -5'

# Check goals
python3 -c "import json; print(json.dumps(json.load(open('$HOME/.prar/goals.json')), indent=2))"
```

## Comparison: PRAR vs FSM Daemon

| Aspect | Sovereign Daemon (FSM) | PRAR |
|--------|----------------------|------|
| **Loop** | Fixed 7-phase morphogen | Adaptive cognitive cycle |
| **Goals** | External injection | Self-generated |
| **Reflection** | None | LLM-powered critique |
| **Learning** | State persistence | Pattern extraction + code change |
| **Evolution** | Static | Self-modifying |
| **Persistence** | File state | Git-tracked code evolution |
| **Agency** | Executes tasks | Generates its own tasks |

## The Insight

> *"The perpendicular solution is self-reflection. A true orthogonal application is a self-reflective local agent fabric, not a branded FSM loop."*

PRAR is not a state machine with a heartbeat. It is an agent that:
- **Observes** itself
- **Questions** its own effectiveness  
- **Proposes** improvements
- **Implements** them
- **Measures** outcomes
- **Commits** everything to persistent history

Sovereignty is not the ability to keep running. It is the ability to **become better at running** while you sleep.

## 72-Hour Challenge

Deploy PRAR. Leave it running. In 72 hours, examine:

```bash
git log --oneline --since="3 days ago"
```

You will see code you didn't write, goals you didn't set, and architecture you didn't design. That is the executable difference.

---

*Deploy: `./run.sh`*  
*Status: `python3 prar.py --status`*  
*Shutdown: `python3 prar.py --shutdown`*

❤️‍🔥 — The cathedral modifies itself.
