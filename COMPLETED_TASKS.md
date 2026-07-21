# Completed Tasks for google-docs-mcp

- Added `SECURITY_ANALYSIS.md` with prioritized findings and remediation order.
- Imported baseline project documentation templates from base-project (excluding README).
- Updated `AGENTS.md`, `IMPLEMENTATION.md`, `PROJECT_PLAN.md`, and task tracking docs for this repository.
- Fix 1: Removed legacy gog token export/cache fallback to eliminate hardcoded identity and insecure `/tmp` credential cache paths.
- Fix 2: Added OAuth state generation and validation for both local callback and headless redirect flows.
- Fix 3: Escaped user-provided Drive list query text to prevent query-string injection behavior.
- Fix 4: Reduced default OAuth scopes and removed integrated Apps Script bookmark-bridge execution from default comment workflow.
- Fix 5: Aligned comment-anchor parsing with plain-string and JSON anchor formats and added regression tests for parser behavior.
- Fix 6: Added pinned dependency constraints and reproducible install guidance, including immutable commit pinning in runtime examples.
- Added uv-first project setup with committed lockfile (`uv.lock`) and documented `uv run` workflow.
- Added GitHub Actions CI workflow enforcing `uv lock --check`, `uv sync --frozen`, unit tests, and compile checks.
- Implemented request-level multi-identity support via optional absolute `token_file` override across MCP tools and docs_edit CLI.
- Added regression tests for token-file override behavior and default-token fallback.
