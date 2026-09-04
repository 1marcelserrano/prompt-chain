from __future__ import annotations

import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from build_skill import build_archive  # noqa: E402
from validate_repo import (  # noqa: E402
    validate_behavior_evals,
    validate_markdown_links,
    validate_package,
    validate_skill_file,
    validate_trigger_evals,
)


class RepositoryToolTests(unittest.TestCase):
    def test_build_is_deterministic_and_contains_only_source_files(self) -> None:
        source = REPO_ROOT / "skills" / "prompt-chain"
        with tempfile.TemporaryDirectory() as temporary:
            first = Path(temporary) / "first.skill"
            second = Path(temporary) / "second.skill"
            build_archive(source, first)
            build_archive(source, second)
            self.assertEqual(first.read_bytes(), second.read_bytes())
            with zipfile.ZipFile(first) as archive:
                members = sorted(name for name in archive.namelist() if not name.endswith("/"))
            expected = sorted(
                f"prompt-chain/{path.relative_to(source).as_posix()}"
                for path in source.rglob("*")
                if path.is_file()
            )
            self.assertEqual(members, expected)

    def test_package_validation_detects_a_stale_member(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "prompt-chain"
            source.mkdir()
            skill = source / "SKILL.md"
            skill.write_text("original", encoding="utf-8")
            package = root / "prompt-chain.skill"
            build_archive(source, package)
            skill.write_text("changed", encoding="utf-8")
            errors = validate_package(source, package)
            self.assertTrue(any("stale member" in error for error in errors))

    def test_frontmatter_rejects_v220_shape(self) -> None:
        description = "x" * 1025
        with tempfile.TemporaryDirectory() as temporary:
            skill = Path(temporary) / "SKILL.md"
            skill.write_text(
                "---\n"
                "name: prompt-chain\n"
                "version: 2.2.0\n"
                f"description: {description}\n"
                "changelog: old\n"
                "---\n",
                encoding="utf-8",
            )
            errors, _ = validate_skill_file(skill)
            self.assertTrue(any("unexpected frontmatter keys" in error for error in errors))
            self.assertTrue(any("maximum is 1024" in error for error in errors))

    def test_trigger_eval_fixture_is_balanced_and_valid(self) -> None:
        path = REPO_ROOT / "evals" / "trigger-evals.json"
        self.assertEqual(validate_trigger_evals(path), [])
        cases = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(sum(case["should_trigger"] for case in cases), 8)
        self.assertEqual(sum(not case["should_trigger"] for case in cases), 8)

    def test_behavior_eval_fixture_is_valid(self) -> None:
        path = REPO_ROOT / "evals" / "behavior-evals.json"
        self.assertEqual(validate_behavior_evals(path), [])

    def test_link_validation_ignores_raw_runs_but_checks_maintained_docs(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            raw_run = root / "benchmark" / "runs" / "date" / "output.md"
            raw_run.parent.mkdir(parents=True)
            raw_run.write_text("[raw placeholder](missing)", encoding="utf-8")
            maintained = root / "README.md"
            maintained.write_text("[maintained link](missing)", encoding="utf-8")
            errors = validate_markdown_links(root)
            self.assertEqual(len(errors), 1)
            self.assertIn("README.md", errors[0])


if __name__ == "__main__":
    unittest.main()
