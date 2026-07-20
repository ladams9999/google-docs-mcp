# Project Plan for google-docs-mcp

google-docs-mcp provides MCP-accessible, in-place Google Docs editing and comment workflows built around text anchors. The project goal is to keep editing reliable for agents while reducing security and operational risk in auth, token handling, and runtime distribution.

## Goals

- Maintain reliable text-anchor editing semantics for all core tools.
- Harden auth and credential handling based on `SECURITY_ANALYSIS.md` findings.
- Improve reproducibility and operator safety for setup and runtime usage.
- Keep docs synchronized with real behavior and known limitations.

## Phase 1: Security Hardening

- Remove hardcoded identity and insecure token cache fallback behavior.
- Add OAuth state validation for local and headless auth flows.
- Escape or sanitize user-provided list query terms before Drive query composition.
- Review and reduce default OAuth scopes to least privilege practical baseline.

## Phase 2: Functional Correctness and Consistency

- Align comment anchor read/write format handling.
- Add regression tests around comment anchoring and list query behavior.
- Verify docs examples match current response payload keys (`plain_text` vs `full_text`).

## Phase 3: Supply-Chain and Release Hygiene

- Add pinned runtime guidance (immutable commit refs) in README examples.
- Introduce dependency lock/constraints strategy for repeatable installs.
- Define release checklist including security and docs verification.

## Success Criteria

- All Phase 1 findings resolved with tests or explicit rationale.
- README quick-start uses stable, auditable install guidance.
- Pending task list remains under active triage with completed items recorded.

