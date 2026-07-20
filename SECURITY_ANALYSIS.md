# Security Analysis for google-docs-mcp

Reviewed on 2026-07-20.

## Status Update (Post-Remediation)

The original findings in this document were used as a baseline hardening backlog.
As of 2026-07-20, fixes have been implemented for Findings 1 through 9, including:
- removal of insecure legacy gog token fallback paths,
- OAuth state validation,
- list query escaping,
- scope reduction and removal of integrated Apps Script bookmark bridge,
- anchor parsing alignment with regression tests,
- dependency lock/constraints strategy,
- immutable-commit guidance and CI lock/test gates.

This analysis is retained as an audit record of the initial review and remediation plan.

## Scope

Files reviewed:
- auth_setup.py
- docs_edit.py
- server.py
- appscript_probe.py
- README.md
- pyproject.toml
- requirements.txt

Assessment focus:
- OAuth flow safety
- Token and credential handling
- API privilege scope and blast radius
- Input handling and injection risk
- Dependency and supply-chain posture
- Functional issues with security impact

## Findings (ordered by severity)

### 1) High: hardcoded personal fallback identity in token export path

Location:
- docs_edit.py:81

Details:
- `_export_gog_token` uses a default email value that is tied to a specific individual.
- This creates an account mix-up risk, leaks personal operational details, and can route auth workflows to the wrong identity when fallback logic is used.

Risk:
- Incorrect-account token export and privacy leakage.

Recommendation:
- Remove hardcoded identity defaults.
- Require explicit identity input for legacy export paths, or remove the legacy path entirely.

### 2) High: insecure token cache in temporary directory

Location:
- docs_edit.py:78
- docs_edit.py:141

Details:
- Gog fallback token data is written to `/tmp/docs_edit_token_cache.json`.
- No explicit permission hardening is applied to that cache file.
- The data contains refresh-token level credentials.

Risk:
- Credential disclosure on shared systems.

Recommendation:
- Remove this cache path, or write cache files with strict owner-only permissions and robust path controls.

### 3) Medium: OAuth state not verified in local or headless flow

Location:
- auth_setup.py:88
- auth_setup.py:147
- auth_setup.py:202

Details:
- `build_auth_url` includes a `state` parameter, but local callback handling and headless redirect parsing do not validate returned state.
- Current behavior accepts authorization code input without CSRF-style correlation checks.

Risk:
- OAuth flow hardening gap.

Recommendation:
- Generate a cryptographically random per-run state value.
- Validate state in both local callback and headless pasteback flows.

### 4) Medium: broad OAuth scope set increases blast radius

Location:
- auth_setup.py:39
- README.md:472

Details:
- Scope set includes full Drive plus multiple Apps Script scopes.
- This exceeds least privilege for many common edit-only workflows.

Risk:
- Compromise impact is larger than necessary.

Recommendation:
- Reduce scopes to minimum required for shipped features.
- Separate advanced features into optional auth profiles when possible.

### 5) Medium: Apps Script bridge can upload and execute script code as user

Location:
- docs_edit.py:255
- docs_edit.py:304
- docs_edit.py:334
- appscript_probe.py:98
- appscript_probe.py:146

Details:
- Runtime path updates script project content and triggers script execution via API.
- This capability is powerful and should be treated as high-trust functionality.

Risk:
- Significant privilege surface in agent-driven environments.

Recommendation:
- Gate this capability behind explicit opt-in.
- Prefer disabling by default or isolating in a separate utility.

### 6) Medium: Drive query string interpolation without escaping

Location:
- server.py:475

Details:
- `docs_list` appends user-provided query text directly into Drive query syntax.
- Unescaped quote and special characters can alter intended query semantics.

Risk:
- Query manipulation and reliability issues.

Recommendation:
- Escape query terms before interpolation, or use safer query construction patterns.

### 7) Low: comment-anchor parsing likely mismatched with anchor format

Location:
- docs_edit.py:1212
- server.py:436

Details:
- Comment creation sends anchor as a plain named-range id string.
- Comment read path tries to parse anchor as JSON and can silently fail to extract named range metadata.

Risk:
- Functional inconsistency and reduced auditability.

Recommendation:
- Align writer and reader anchor-format expectations and add tests for both.

### 8) Low: dependency strategy is minimum-only and unpinned

Location:
- pyproject.toml:13
- requirements.txt:1

Details:
- Dependencies are specified as open minimum versions.
- This can cause non-deterministic installs over time.

Risk:
- Supply-chain and reproducibility risk.

Recommendation:
- Add a locked dependency set for production or release workflows.

### 9) Medium: runtime install guidance pulls from moving Git branch targets

Location:
- README.md:24
- README.md:34

Details:
- Quick-start instructions run directly from Git URLs and include branch-target execution.
- Without pinning to a specific immutable commit, future upstream changes can alter executed code.

Risk:
- Supply-chain exposure and non-repeatable execution behavior.

Recommendation:
- Prefer pinned commit references for runtime execution examples.
- Document a reviewed versioning policy for operational use.

## Positive observations

- Token output from auth setup applies restrictive file mode (`chmod(0o600)`) at write time.
  - auth_setup.py:143
- HTTP requests in stdlib-based token and Apps Script paths use explicit timeouts.
  - auth_setup.py:111
  - docs_edit.py:234
  - docs_edit.py:251
  - appscript_probe.py:64
  - appscript_probe.py:75

## Recommended remediation order

1. Remove hardcoded identity and insecure `/tmp` token cache fallback.
2. Add OAuth state generation and validation in both auth modes.
3. Escape `docs_list` query input.
4. Reduce default OAuth scopes and isolate high-trust Apps Script operations.
5. Align comment-anchor read/write format handling and add regression tests.
6. Add lockfile or pinned constraints for reproducible dependency resolution.

## Suggested validation after fixes

- Auth flow tests:
  - valid state accepted
  - mismatched state rejected
- Token storage tests:
  - no insecure temp token cache writes
  - token file permissions are restrictive where supported
- Query safety tests:
  - quotes and backslashes in list query do not alter syntax
- Comment anchor tests:
  - add comment then read comment returns expected anchor metadata
