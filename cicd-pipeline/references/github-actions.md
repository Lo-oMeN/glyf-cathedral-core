# GitHub Actions Reference

## Workflow Structure

```yaml
name: Workflow Name

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  workflow_dispatch:  # Manual trigger

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build
        run: echo "Building..."
```

## Common Triggers (on)

| Event | Description |
|-------|-------------|
| `push` | Push to branch |
| `pull_request` | PR opened/synchronized |
| `pull_request_target` | PR from forks (dangerous) |
| `workflow_dispatch` | Manual trigger |
| `schedule` | Cron schedule |
| `release` | Release created/published |

## Runner Types

- `ubuntu-latest` / `ubuntu-22.04` / `ubuntu-20.04`
- `windows-latest` / `windows-2022` / `windows-2019`
- `macos-latest` / `macos-13` / `macos-12`
- Self-hosted runners

## Security Best Practices

1. **Pin actions to SHA** instead of tags:
   ```yaml
   # Bad
   - uses: actions/checkout@v4
   # Good
   - uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11
   ```

2. **Use least-privilege permissions**:
   ```yaml
   permissions:
     contents: read
     pull-requests: write
   ```

3. **Never use pull_request_target with untrusted code**

4. **Validate inputs** in workflow_dispatch

## Common Patterns

### Matrix Strategy
```yaml
strategy:
  matrix:
    node-version: [18.x, 20.x]
    os: [ubuntu-latest, windows-latest]
fail-fast: false
```

### Caching
```yaml
- uses: actions/cache@v3
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
```

### Secrets
```yaml
- name: Deploy
  env:
    API_KEY: ${{ secrets.API_KEY }}
  run: deploy.sh
```

## API Endpoints for Automation

- `GET /repos/{owner}/{repo}/actions/workflows` - List workflows
- `GET /repos/{owner}/{repo}/actions/runs` - List runs
- `POST /repos/{owner}/{repo}/actions/workflows/{workflow_id}/dispatches` - Trigger workflow
- `GET /repos/{owner}/{repo}/actions/runs/{run_id}/logs` - Get logs