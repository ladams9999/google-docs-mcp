# Implementation for google-docs-mcp

## Architecture

- `server.py`
	- Registers MCP tools via FastMCP and delegates business logic to `docs_edit.py`.
	- Exposes document edit, list/create, and comment lifecycle operations.
- `docs_edit.py`
	- Implements Docs and Drive API operations.
	- Uses text matching + index mapping helpers to avoid direct LLM-managed index edits.
	- Contains token loading and credential refresh behavior.
- `auth_setup.py`
	- Performs OAuth setup, exchanges auth codes, and writes token material to local token file.
- `appscript_probe.py`
	- Experimental Apps Script probe utility for comment API capability checks.

## Auth and Credential Flow

- Primary token path is `~/.google-docs-mcp/token.json`.
- Token loading is driven by env vars and fallback paths in `docs_edit.py`.
- OAuth client credentials may come from token payload or env var overrides.

## Current Security Notes

- See `SECURITY_ANALYSIS.md` for prioritized findings.
- Key hardening priorities:
	- remove/replace insecure legacy token fallback behavior,
	- validate OAuth state,
	- reduce default privilege scope set,
	- harden query construction in `docs_list`.

## Editing Semantics

- Read-before-write pattern is expected:
	1. fetch doc and paragraph map,
	2. resolve target by text anchor,
	3. apply batchUpdate request(s),
	4. verify with a subsequent read.
- `batch_replace` sorts operations from end to start to preserve index correctness.
- Rich-text insertion supports a constrained markdown-like subset to avoid ambiguous parsing.

## Documentation Maintenance Rules

- Keep `README.md` user-facing and operational.
- Keep `PROJECT_PLAN.md` focused on roadmap and priorities.
- Keep `PENDING_TASKS.md` granular and execution-ready.
- Keep `COMPLETED_TASKS.md` concise and dated when possible.
