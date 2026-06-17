# Security Policy

## Supported versions

`service-ontology-lite` is currently in private staging. Security fixes target the current `main` branch until the first public package release.

## Reporting a vulnerability

Report security issues privately to:

```text
hello@veris.kr
```

Include:

```text
affected command or module
minimal reproduction steps
expected impact
whether secrets, private routes, or production data were exposed
```

Do not open a public issue for vulnerabilities involving secret exposure, private project metadata, or bypassable security assumptions.

## Security model

`service-ontology-lite` is a static inspection tool.

By design, it should not:

```text
execute target application code
open network connections to target apps
read .env files
collect secret values
include production-only schemas, tokens, or incident runbooks
```

It emits structural metadata such as routes, auth labels, entities, external service names, cron handlers, and generic risk findings.

## Out of scope

This package does not replace:

```text
authentication tests
dependency vulnerability scanning
SAST/DAST
production penetration tests
framework-specific type checking
runtime traffic analysis
```
