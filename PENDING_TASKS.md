# Pending Tasks for google-docs-mcp

Tasks below break work into small, individually pickable work items. Paths are relative to this file unless noted.

---

- [ ] Remove hardcoded default identity in `docs_edit.py` legacy token export path.
- [ ] Remove or harden `/tmp/docs_edit_token_cache.json` handling for credential data.
- [ ] Implement OAuth `state` validation in local and headless auth flows in `auth_setup.py`.
- [ ] Escape Drive query user input in `docs_list` query composition in `server.py`.
- [ ] Reconcile `docs_add_comment` anchor format with `docs_read_comments` parsing.
- [ ] Update README examples where response key uses `plain_text` but docs show `full_text`.
- [ ] Add tests for auth flow state handling and comment anchor parsing.
- [ ] Add deterministic dependency lock or constraints file for release use.
