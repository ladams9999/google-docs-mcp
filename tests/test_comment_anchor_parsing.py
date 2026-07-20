import unittest

from anchor_utils import extract_named_range_id


class TestCommentAnchorParsing(unittest.TestCase):
    def test_plain_named_range_anchor(self):
        anchor = "kix.abc123"
        self.assertEqual(extract_named_range_id(anchor), "kix.abc123")

    def test_json_named_range_anchor(self):
        anchor = '{"a": [{"t": "r", "v": "kix.range987"}]}'
        self.assertEqual(extract_named_range_id(anchor), "kix.range987")

    def test_empty_anchor_returns_none(self):
        self.assertIsNone(extract_named_range_id(""))
        self.assertIsNone(extract_named_range_id("   "))

    def test_invalid_json_anchor_returns_none(self):
        anchor = '{"a": [invalid]}'
        self.assertIsNone(extract_named_range_id(anchor))


if __name__ == "__main__":
    unittest.main()
