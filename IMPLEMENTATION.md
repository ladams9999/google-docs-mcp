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

## Auth and Credential Flow

- Primary token path is `~/.google-docs-mcp/token.json`.
- Token loading is driven by env vars and fallback paths in `docs_edit.py`.
- OAuth client credentials may come from token payload or env var overrides.
- Request-level override is supported via optional `token_file` on tools.
- `token_file` must be an absolute path and is used only for that request.

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

## Environment and Tooling

- Primary local workflow uses `uv`.
- `uv.lock` is committed for reproducible dependency resolution.
- Use `uv sync` to provision `.venv`.
- Use `uv run ...` for commands (server, auth setup, tests).

## Multi-Account Token Selection

- MCP tools in `server.py` now accept optional `token_file`.
- `docs_edit.py` resolves token sources in this order:
	1. request `token_file` override (absolute path required),
	2. environment/default token behavior.
- This allows one server process to serve multiple identities using distinct token files.

## CI

- Workflow file: `.github/workflows/ci.yml`.
- CI gates currently enforce:
	- lockfile consistency (`uv lock --check`),
	- frozen dependency sync (`uv sync --frozen`),
	- unit tests (`uv run python -m unittest discover -s tests -p "test_*.py"`),
	- compile pass (`uv run python -m compileall -q .`).
