# Skills Development Test Suite
# Safe environment for skill validation before production use

workspace: /root/.openclaw/workspace/skills-test/
logs: /root/.openclaw/workspace/skills-test/logs/

## Test Categories

### 1. File Operations
- read/write/edit validation
- Path resolution
- Permission handling
- Large file streaming

### 2. Process Management
- exec with timeout
- Background process handling
- Signal management
- Resource cleanup

### 3. Network Operations
- web_search result validation
- web_fetch extraction quality
- Browser automation stability
- Error handling (timeouts, 404s)

### 4. Memory Management
- memory_search recall accuracy
- memory_get snippet extraction
- Cross-session persistence
- File append vs overwrite safety

### 5. Voice & Audio
- Piper TTS generation
- Prosody modulation
- Audio file validation
- Reverb/acoustics processing

### 6. Cron & Scheduling
- Job creation syntax
- Schedule validation
- Session target correctness
- Delivery mode testing

## Test Runner

```python
# skills-test/runner.py
# Executes all tests, logs results, reports failures
```

## Safe Mode

- All file writes go to `/tmp/` or `skills-test/scratch/`
- Network calls use test endpoints where possible
- No external messages sent (dry-run mode)
- Git commits only to test branches

## Success Criteria

- 100% pass rate for file operations
- 100% pass rate for memory management
- >95% pass rate for network (external variance)
- All voice generation produces valid audio
- All cron jobs validate syntax before submission
