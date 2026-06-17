# Contributing

English | [한국어](./CONTRIBUTING-ko_kr.md)

`service-ontology-lite` is a small static inspection tool for service maps, release audits, and AI-agent edit-risk checks.

## Scope

Accepted contributions should stay inside the public-safe core:

```text
schema
CLI
MCP stdio server
generic scanner
generic audit rules
sample Next.js/Vercel app
report format
documentation
```

Do not add project-specific production data, real tokens, private incident runbooks, customer data, or domain-specific commercial scoring rules.

## Development setup

```bash
python3 -m pip install -e .
python3 -m pip install pytest ruff build
```

## Release gate

Run this before opening a pull request:

```bash
python3 -m compileall -q src tests
python3 -m pytest -q
python3 -m ruff check .
python3 -m build --sdist --wheel
```

## Documentation changes

For README changes, keep English and Korean pages aligned:

```text
README.md
README-ko_kr.md
```

If a command, output field, or limitation changes in one language, update the other page in the same pull request.

## Security boundary

The scanner must remain static by default:

```text
no application code execution
no network access to target apps
no .env reads
no secret collection
no production-only schemas or runbooks
```

If a change requires runtime inspection or network access, document it as a separate opt-in feature before implementation.
