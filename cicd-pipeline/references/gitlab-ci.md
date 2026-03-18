# GitLab CI Reference

## Configuration Structure

```yaml
stages:
  - build
  - test
  - deploy

variables:
  NODE_VERSION: "20"

cache:
  paths:
    - node_modules/

build-job:
  stage: build
  image: node:20
  script:
    - npm ci
    - npm run build
  artifacts:
    paths:
      - dist/

test-job:
  stage: test
  script:
    - npm test
```

## Stages

Default stages: `.pre` → `build` → `test` → `deploy` → `.post`

Custom stages:
```yaml
stages:
  - build
  - test
  - security-scan
  - package
  - deploy
```

## Job Keywords

| Keyword | Description |
|---------|-------------|
| `script` | Commands to execute (required) |
| `image` | Docker image for job |
| `services` | Linked service containers |
| `before_script` | Commands before main script |
| `after_script` | Commands after main script |
| `variables` | Job-specific variables |
| `cache` | Files to cache between runs |
| `artifacts` | Files to preserve after job |
| `dependencies` | Jobs to get artifacts from |
| `needs` | DAG dependency (parallel jobs) |
| `rules` | Conditional job execution |
| `only/except` | Legacy branch filtering |
| `when` | When to run (on_success, on_failure, always, manual, delayed) |
| `allow_failure` | Don't fail pipeline if job fails |
| `timeout` | Job timeout |
| `parallel` | Number of parallel instances |
| `tags` | Runner selection tags |
| `environment` | Deployment environment |
| `coverage` | Coverage regex pattern |

## Rules (Modern Alternative to only/except)

```yaml
deploy:
  script: deploy.sh
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
      when: manual
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
      when: never
    - when: on_success
```

## Cache vs Artifacts

**Cache**: Persist between pipeline runs (dependencies)
```yaml
cache:
  key: ${CI_COMMIT_REF_SLUG}
  paths:
    - node_modules/
```

**Artifacts**: Pass files between jobs and preserve after pipeline
```yaml
artifacts:
  name: "$CI_JOB_NAME-$CI_COMMIT_REF_NAME"
  paths:
    - dist/
  expire_in: 1 week
```

## CI/CD Variables

Predefined variables:
- `CI_COMMIT_SHA` - Commit revision
- `CI_COMMIT_REF_NAME` - Branch/tag name
- `CI_PROJECT_DIR` - Full path to repository
- `CI_JOB_ID` - Unique job ID
- `CI_PIPELINE_ID` - Pipeline ID
- `CI_REGISTRY` - Container registry URL
- `CI_REGISTRY_IMAGE` - Project registry image URL

Custom variables:
```yaml
variables:
  DEPLOY_SERVER: "production.example.com"
  DATABASE_NAME:
    value: "mydb"
    description: "Database name for deployment"
```

## Environments

```yaml
deploy_production:
  stage: deploy
  script:
    - deploy.sh
  environment:
    name: production
    url: https://example.com
    on_stop: stop_production
  only:
    - main
```

## Parent-Child Pipelines

```yaml
# .gitlab-ci.yml
trigger_child:
  trigger:
    include: child-pipeline.yml
    strategy: depend
```

## API Endpoints

- `GET /projects/:id/pipelines` - List pipelines
- `POST /projects/:id/pipeline` - Create pipeline
- `GET /projects/:id/pipelines/:pipeline_id` - Get pipeline
- `GET /projects/:id/jobs` - List jobs
- `GET /projects/:id/jobs/:job_id/trace` - Get job logs