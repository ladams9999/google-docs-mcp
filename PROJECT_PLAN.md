# Project Plan for google-docs-mcp

google-docs-mcp provides MCP-accessible, in-place Google Docs editing and comment workflows built around text anchors. The project goal is to keep editing reliable for agents while reducing security and operational risk in auth, token handling, and runtime distribution.

## Goals

- Maintain reliable text-anchor editing semantics for all core tools.
- Harden auth and credential handling based on `SECURITY_ANALYSIS.md` findings.
- Improve reproducibility and operator safety for setup and runtime usage.
- Keep docs synchronized with real behavior and known limitations.

## Phase 1: Security Hardening

- Completed: removed hardcoded identity and insecure token cache fallback behavior.
- Completed: added OAuth state validation for local and headless auth flows.
- Completed: escaped user-provided list query terms before Drive query composition.
- Completed: reduced default OAuth scopes to least privilege practical baseline.

## Phase 2: Functional Correctness and Consistency

- Completed: aligned comment anchor read/write format handling.
- Completed: added regression tests around comment anchor parsing behavior.
- Completed: verified docs examples match current response payload keys (`plain_text`).

## Phase 3: Supply-Chain and Release Hygiene

- Completed: added pinned runtime guidance (immutable commit refs) in README examples.
- Completed: introduced lockfile + constraints strategy for repeatable installs.
- Completed: added CI workflow for lock checks, frozen sync, tests, and compile pass.

## Phase 4: Maintenance and Expansion

- Add broader automated tests for auth flow edge cases and docs operations.
- Add release checklist section (tagging, changelog, smoke tests).
- Consider optional lint/type-check stage in CI once tooling choices are finalized.

## Success Criteria

- Security findings from the initial analysis are remediated in code and docs.
- CI enforces lock consistency and baseline quality checks on push and PR.
- README quick-start uses stable, auditable install guidance.

