import hashlib
import io
import json
from pathlib import Path
from unittest import TestCase, mock
import tempfile
from tools import fetch_inputs, publish


class ArchiveToolsTest(TestCase):
    def test_digest_and_cached_transfer(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "input"
            raw = b"sample"
            with mock.patch.object(
                fetch_inputs, "urlopen", return_value=io.BytesIO(raw)
            ) as http:
                digest = hashlib.sha256(raw).hexdigest()
                fetch_inputs.download("https://example.org/file", path, digest)
                fetch_inputs.download("https://example.org/file", path, digest)
                self.assertEqual(http.call_count, 1)
                self.assertEqual(
                    fetch_inputs.file_hash(path, "sha1", True),
                    hashlib.sha1(b"blob 6\0sample").hexdigest(),
                )

    def test_digest_mismatch_preserves_old_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "input"
            path.write_bytes(b"old")
            with (
                mock.patch.object(
                    fetch_inputs, "urlopen", return_value=io.BytesIO(b"new")
                ),
                self.assertRaises(ValueError),
            ):
                fetch_inputs.download("https://example.org/file", path, "f" * 64)
            self.assertEqual(path.read_bytes(), b"old")

    def test_publish_preflight_preserves_existing_history(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            root.joinpath("delivery.json").write_text(
                json.dumps(
                    {
                        "account": "alice",
                        "repositories": [{"name": "lab", "commit": "a" * 40}],
                    }
                )
            )
            calls = []

            def fake(*argv, **kwargs):
                calls.append(argv)
                if argv[:3] == ("gh", "api", "user"):
                    return "alice"
                if "--paginate" in argv:
                    return "alice/lab"
                if argv[:2] == ("git", "bundle"):
                    return "a" * 40 + " refs/heads/main"
                return "b" * 40

            with (
                mock.patch.object(publish, "call", side_effect=fake),
                self.assertRaisesRegex(ValueError, "Name conflict"),
            ):
                publish.main(root, True)
            self.assertFalse(any("push" in c or "POST" in c for c in calls))
