import json
import os
import tempfile
import unittest
from pathlib import Path

import docs_edit


class TestTokenFileOverride(unittest.TestCase):
    def test_load_token_from_absolute_override_path(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            token_path = Path(tmpdir) / "override-token.json"
            payload = {
                "refresh_token": "rtok",
                "client_id": "cid",
                "client_secret": "csecret",
                "scopes": ["https://www.googleapis.com/auth/documents"],
            }
            token_path.write_text(json.dumps(payload))

            token = docs_edit._load_token(token_file_override=str(token_path))
            self.assertEqual(token["refresh_token"], "rtok")
            self.assertEqual(token["client_id"], "cid")

    def test_reject_relative_override_path(self):
        with self.assertRaises(ValueError):
            docs_edit._load_token(token_file_override="relative/token.json")

    def test_default_env_token_still_works_without_override(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            token_path = Path(tmpdir) / "env-token.json"
            payload = {
                "refresh_token": "env_rtok",
                "client_id": "env_cid",
                "client_secret": "env_secret",
                "scopes": ["https://www.googleapis.com/auth/documents"],
            }
            token_path.write_text(json.dumps(payload))

            prior = os.environ.get("GOOGLE_DOCS_MCP_TOKEN")
            os.environ["GOOGLE_DOCS_MCP_TOKEN"] = str(token_path)
            try:
                token = docs_edit._load_token()
            finally:
                if prior is None:
                    del os.environ["GOOGLE_DOCS_MCP_TOKEN"]
                else:
                    os.environ["GOOGLE_DOCS_MCP_TOKEN"] = prior

            self.assertEqual(token["refresh_token"], "env_rtok")


if __name__ == "__main__":
    unittest.main()
