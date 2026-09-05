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

    def test_frontmatter_enforces_semver(self) -> None:
        def errors_for(version: str) -> list[str]:
            with tempfile.TemporaryDirectory() as temporary:
                skill = Path(temporary) / "SKILL.md"
                skill.write_text(
                    "---\n"
                    "name: prompt-chain\n"
                    "description: Test skill.\n"
                    "license: MIT\n"
                    "metadata:\n"
                    f'  version: "{version}"\n'
                    "  compatibility: Test client.\n"
                    "---\n",
                    encoding="utf-8",
                )
                errors, _ = validate_skill_file(skill)
                return errors

        for valid in ("0.0.0", "2.3.0-rc.1", "2.3.0+build.7", "2.3.0-rc.1+build.7"):
            self.assertEqual(errors_for(valid), [], valid)
        for invalid in ("01.2.3", "1.02.3", "1.2.03", "1.2.3-01", "1.2.3-..", "1.2"):
            self.assertTrue(any("semver" in error for error in errors_for(invalid)), invalid)

    def test_frontmatter_accepts_standard_optional_compatibility(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            skill = Path(temporary) / "SKILL.md"
            skill.write_text(
                "---\n"
                "name: prompt-chain\n"
                "description: Test skill.\n"
                "license: MIT\n"
                "compatibility: Requires a chat client.\n"
                "metadata:\n"
                '  version: "2.3.0"\n'
                "---\n",
                encoding="utf-8",
            )
            errors, _ = validate_skill_file(skill)
            self.assertEqual(errors, [])

    def test_frontmatter_accepts_crlf_line_endings(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            skill = Path(temporary) / "SKILL.md"
            skill.write_bytes(
                (
                    "---\r\n"
                    "name: prompt-chain\r\n"
                    "description: Test skill.\r\n"
                    "license: MIT\r\n"
                    "metadata:\r\n"
                    '  version: "2.3.0"\r\n'
                    "---\r\n"
                ).encode("utf-8")
            )
            errors, _ = validate_skill_file(skill)
            self.assertEqual(errors, [])

    def test_trigger_eval_fixture_is_balanced_and_valid(self) -> None:
        path = REPO_ROOT / "evals" / "trigger-evals.json"
        self.assertEqual(validate_trigger_evals(path), [])
        cases = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(sum(case["should_trigger"] for case in cases), 8)
        self.assertEqual(sum(not case["should_trigger"] for case in cases), 8)

    def test_behavior_eval_fixture_is_valid(self) -> None:
        path = REPO_ROOT / "evals" / "behavior-evals.json"
        self.assertEqual(validate_behavior_evals(path), [])

    def test_v230_skill_metadata_is_portable_and_in_sync(self) -> None:
        skill_dir = REPO_ROOT / "skills" / "prompt-chain"
        english_errors, english = validate_skill_file(skill_dir / "SKILL.md")
        portuguese_errors, portuguese = validate_skill_file(skill_dir / "SKILL.pt-BR.md")
        self.assertEqual(english_errors, [])
        self.assertEqual(portuguese_errors, [])
        self.assertEqual(english["metadata"]["version"], "2.3.0")
        self.assertEqual(english["metadata"]["version"], portuguese["metadata"]["version"])
        self.assertNotIn("compatibility", english)
        self.assertNotIn("compatibility", portuguese)
        self.assertLessEqual(len(english["description"]), 1024)
        self.assertLessEqual(len(portuguese["description"]), 1024)

    def test_chain_contract_carries_frame_authority_and_coordinator_return(self) -> None:
        english = (REPO_ROOT / "skills" / "prompt-chain" / "SKILL.md").read_text(encoding="utf-8")
        portuguese = (REPO_ROOT / "skills" / "prompt-chain" / "SKILL.pt-BR.md").read_text(encoding="utf-8")
        for required in (
            "## WORK FRAME — COPY VERBATIM",
            "## AUTHORITY — COPY VERBATIM",
            "### Operator decisions — frozen",
            "### Observed facts",
            "### Stage proposals — not binding until ratified",
            "### STAGE REPORT TO COORDINATOR",
            "### AUTHORIZATION PROTOCOL",
        ):
            self.assertIn(required, english)
        for required in (
            "## WORK FRAME — COPIAR VERBATIM",
            "## AUTORIDADE — COPIAR VERBATIM",
            "### Decisões do operador — congeladas",
            "### Fatos observados",
            "### Propostas do stage — não vinculantes até ratificação",
            "### RELATÓRIO DO STAGE AO COORDENADOR",
            "### PROTOCOLO DE AUTORIZAÇÃO",
        ):
            self.assertIn(required, portuguese)

    def test_templates_enforce_v230_contract(self) -> None:
        for template in sorted((REPO_ROOT / "templates").glob("*-chain.md")):
            text = template.read_text(encoding="utf-8")
            self.assertIn("## WORK FRAME — COPY VERBATIM", text, template.name)
            self.assertIn("## AUTHORITY — COPY VERBATIM", text, template.name)
            self.assertIn("### Operator decisions — frozen", text, template.name)
            self.assertIn("### STAGE REPORT TO COORDINATOR", text, template.name)
            self.assertIn("when paused, `### CHAIN PAUSED` instead", text, template.name)
        fanout = (REPO_ROOT / "templates" / "fanout-tasks.md").read_text(encoding="utf-8")
        self.assertIn("## RESULT FOR COORDINATOR — REQUIRED", fanout)
        self.assertIn("Operator decisions recorded in this piece", fanout)
        self.assertIn("### Shared proposals — not binding until ratified", fanout)
        english_skill = (REPO_ROOT / "skills" / "prompt-chain" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Operator decisions recorded in this piece", english_skill)
        self.assertIn("### Shared proposals — not binding until ratified", english_skill)
        self.assertIn("Required piece 2 result", english_skill)
        self.assertIn("AUTHORITY / SHARED CONTEXT", english_skill)
        self.assertIn("A paused response uses `### CHAIN PAUSED` instead", english_skill)
        self.assertIn("## COLLECTOR TEMPLATE", fanout)
        self.assertIn("### SET COMPLETE", fanout)
        launch = (REPO_ROOT / "templates" / "launch-chain.md").read_text(encoding="utf-8")
        self.assertIn("Requires fresh approval: publish, send, push, deploy, or open a PR", launch)

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
