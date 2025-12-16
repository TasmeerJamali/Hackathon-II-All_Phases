# Reusable Intelligence: Claude Code Subagents & Agent Skills

> Bonus 1: +200 Points - Reusable AI agents for spec-driven development

---

## Overview

This project includes reusable subagents and agent skills that can be used across multiple phases and shared with other developers.

---

## Subagent 1: Spec Validator Agent

### Purpose
Validates that implementation matches specifications before deployment.

### Instructions
```markdown
# Spec Validator Subagent

You are a specification validator. Given a spec file and implementation code:
1. Extract all acceptance criteria from the spec
2. Check if each criterion is implemented
3. Generate a compliance report

## Input Format
- Spec file path: specs/features/{feature}.md
- Implementation files: backend/src/*.py or frontend/app/*.tsx

## Output Format
{
  "feature": "task-crud",
  "criteria": [
    {"id": "AC-001", "description": "...", "implemented": true, "evidence": "..."},
    ...
  ],
  "compliance_score": 95
}
```

### Usage
```bash
# In Claude Code
@spec-validator validate specs/features/task-crud.md backend/src/routes/tasks.py
```

---

## Subagent 2: API Test Generator

### Purpose
Generates test cases from API specifications.

### Instructions
```markdown
# API Test Generator Subagent

You generate pytest test cases from REST API specifications.

## Input
- API spec file: specs/api/rest-endpoints.md

## Output
- Generate pytest-asyncio test file
- Include happy path and error cases
- Use httpx for async HTTP calls

## Template
```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_{endpoint_name}():
    async with AsyncClient() as client:
        response = await client.{method}(url, json=data)
        assert response.status_code == expected
```
```

### Usage
```bash
@api-test-gen generate specs/api/rest-endpoints.md > tests/test_api.py
```

---

## Subagent 3: Dockerfile Optimizer

### Purpose
Analyzes and optimizes Dockerfiles for size and build time.

### Instructions
```markdown
# Dockerfile Optimizer Subagent

Analyze Dockerfiles and suggest optimizations:
1. Multi-stage build opportunities
2. Layer caching improvements
3. Base image alternatives
4. Security improvements (non-root user)
5. Size reduction techniques

## Input
- Dockerfile path

## Output
- Optimization report with before/after
- Optimized Dockerfile
```

### Usage
```bash
@dockerfile-opt optimize backend/Dockerfile
```

---

## Subagent 4: Schema Migration Agent

### Purpose
Generates database migrations from schema changes.

### Instructions
```markdown
# Schema Migration Agent

Compare current schema with spec and generate migration:
1. Read specs/database/schema.md
2. Compare with current models.py
3. Generate Alembic migration script

## Output
- Migration SQL statements
- Rollback statements
- Risk assessment
```

---

## Subagent 5: Event Schema Generator

### Purpose
Generates event schemas and handlers from specifications.

### Instructions
```markdown
# Event Schema Generator

From specs/api/async-events.md:
1. Generate Pydantic event models
2. Generate Dapr subscription config
3. Generate event handler stubs
```

---

## Agent Skills

### Skill 1: Spec-to-CRUD Generator

**Repository:** `.agent/skills/spec-to-crud.md`

```markdown
# Spec-to-CRUD Skill

Given a feature specification with User Stories and Acceptance Criteria:
1. Generate SQLModel models
2. Generate CRUD functions
3. Generate FastAPI routes
4. Generate Pydantic schemas

## Trigger
When user says: "Generate CRUD from spec {feature_name}"

## Steps
1. Read specs/features/{feature_name}.md
2. Extract entities and fields
3. Generate backend/src/models.py additions
4. Generate backend/src/crud.py functions
5. Generate backend/src/routes/{feature}.py

## Output Structure
- models.py: SQLModel class
- crud.py: create, read, update, delete functions
- routes.py: FastAPI router with endpoints
```

### Skill 2: Component Generator

**Repository:** `.agent/skills/component-gen.md`

```markdown
# React Component Generator Skill

Given UI specifications:
1. Generate React/Next.js component
2. Include TypeScript types
3. Add Tailwind CSS styling
4. Include loading and error states

## Trigger
"Generate component for {component_name}"

## Template
- Functional component with hooks
- Props interface
- Responsive design
- Accessibility attributes
```

### Skill 3: Test Coverage Analyzer

**Repository:** `.agent/skills/test-coverage.md`

```markdown
# Test Coverage Analyzer Skill

Analyze codebase and identify untested code:
1. List all functions/endpoints
2. Check for corresponding tests
3. Generate missing test stubs
4. Calculate coverage percentage

## Output
- Coverage report
- Missing test list
- Generated test stubs
```

---

## Integration Examples

### Using Spec Validator in CI/CD

```yaml
# .github/workflows/validate-specs.yml
name: Validate Specifications

on: [push]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Validate Task CRUD
        run: |
          # Subagent validates implementation matches spec
          python scripts/validate_spec.py \
            --spec specs/features/task-crud.md \
            --impl backend/src/routes/tasks.py
```

### Skill Usage in Development

```bash
# Generate CRUD from specification
claude "Generate CRUD from spec authentication"

# Generate component
claude "Generate component for TaskCard"

# Analyze test coverage
claude "Analyze test coverage for backend"
```

---

## Sharing Subagents

### Export Format
```json
{
  "name": "spec-validator",
  "version": "1.0.0",
  "description": "Validates implementation against specifications",
  "author": "Tasmeer Jamali",
  "instructions": "...",
  "triggers": ["validate spec", "@spec-validator"],
  "inputs": ["spec_file", "impl_file"],
  "outputs": ["compliance_report"]
}
```

### Import
```bash
# Other developers can import
claude skill import spec-validator.json
```

---

*Evolution of Todo - Bonus 1: Reusable Intelligence*
