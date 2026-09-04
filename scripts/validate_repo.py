#!/usr/bin/env python3
"""Validate the prompt-chain source, eval fixtures, links, and package."""

from __future__ import annotations

import argparse
import json
import re
import tempfile
import zipfile
from pathlib import Path
from urllib.parse import unquote

import yaml

from build_skill import build_archive, source_files


ALLOWED_FRONTMATTER = {
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
}
SEMVER = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$")
MARKDOWN_LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def load_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing opening frontmatter delimiter")
    parts = text.split("---", 2)
    if len(parts) != 3:
        raise ValueError("missing closing frontmatter delimiter")
    data = yaml.safe_load(parts[1])
    if not isinstance(data, dict):
        raise ValueError("frontmatter must be a mapping")
    return data


def validate_skill_file(path: Path) -> tuple[list[str], dict | None]:
    errors: list[str] = []
    try:
        data = load_frontmatter(path)
    except (OSError, ValueError, yaml.YAMLError) as error:
        return [f"{path}: invalid frontmatter: {error}"], None

    unexpected = sorted(set(data) - ALLOWED_FRONTMATTER)
    if unexpected:
        errors.append(f"{path}: unexpected frontmatter keys: {', '.join(unexpected)}")
    if data.get("name") != "prompt-chain":
        errors.append(f"{path}: name must be prompt-chain")

    description = data.get("description")
    if not isinstance(description, str) or not description.strip():
        errors.append(f"{path}: description must be a non-empty string")
    elif len(description) > 1024:
        errors.append(
            f"{path}: description is {len(description)} characters; maximum is 1024"
        )

    if data.get("license") != "MIT":
        errors.append(f"{path}: license must be MIT")
    compatibility = data.get("compatibility")
    if not isinstance(compatibility, str) or not compatibility.strip():
        errors.append(f"{path}: compatibility must describe the supported environment")

    metadata = data.get("metadata")
    if not isinstance(metadata, dict):
        errors.append(f"{path}: metadata must be a mapping")
    else:
        version = metadata.get("version")
        if not isinstance(version, str) or not SEMVER.fullmatch(version):
            errors.append(f"{path}: metadata.version must be a semver string")

    return errors, data


def validate_markdown_links(repo_root: Path) -> list[str]:
    errors: list[str] = []
    for markdown in sorted(repo_root.rglob("*.md")):
        if ".git" in markdown.parts:
            continue
        relative_parts = markdown.relative_to(repo_root).parts
        if relative_parts[:2] in {("benchmark", "runs"), ("evals", "runs")}:
            # Raw model outputs are evidence, not maintained repository prose.
            continue
        text = markdown.read_text(encoding="utf-8")
        for raw_target in MARKDOWN_LINK.findall(text):
            target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            path_part = unquote(target.split("#", 1)[0])
            if not path_part:
                continue
            resolved = (markdown.parent / path_part).resolve()
            if not resolved.exists():
                errors.append(
                    f"{markdown.relative_to(repo_root)}: broken local link {raw_target}"
                )
    return errors


def validate_package(source_dir: Path, package_path: Path) -> list[str]:
    errors: list[str] = []
    if not package_path.exists():
        return [f"missing package: {package_path}"]

    root_name = source_dir.name
    expected_files = {
        f"{root_name}/{path.relative_to(source_dir).as_posix()}": path.read_bytes()
        for path in source_files(source_dir)
    }
    try:
        with zipfile.ZipFile(package_path) as archive:
            actual_files = {
                name: archive.read(name)
                for name in archive.namelist()
                if not name.endswith("/")
            }
    except (OSError, zipfile.BadZipFile) as error:
        return [f"{package_path}: invalid package: {error}"]

    if set(actual_files) != set(expected_files):
        missing = sorted(set(expected_files) - set(actual_files))
        extra = sorted(set(actual_files) - set(expected_files))
        if missing:
            errors.append(f"{package_path}: missing members: {', '.join(missing)}")
        if extra:
            errors.append(f"{package_path}: extra members: {', '.join(extra)}")
    for name in sorted(set(actual_files) & set(expected_files)):
        if actual_files[name] != expected_files[name]:
            errors.append(f"{package_path}: stale member: {name}")

    with tempfile.TemporaryDirectory() as temporary:
        rebuilt = Path(temporary) / package_path.name
        build_archive(source_dir, rebuilt)
        if rebuilt.read_bytes() != package_path.read_bytes():
            errors.append(f"{package_path}: archive is not the deterministic build output")
    return errors


def validate_trigger_evals(path: Path) -> list[str]:
    try:
        cases = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return [f"{path}: invalid JSON: {error}"]
    errors: list[str] = []
    if not isinstance(cases, list):
        return [f"{path}: expected a list"]
    ids: set[str] = set()
    counts = {True: 0, False: 0}
    for index, case in enumerate(cases):
        label = f"{path}[{index}]"
        if not isinstance(case, dict):
            errors.append(f"{label}: expected an object")
            continue
        if not all(isinstance(case.get(key), str) and case[key].strip() for key in ("id", "prompt", "rationale")):
            errors.append(f"{label}: id, prompt, and rationale must be non-empty strings")
        if not isinstance(case.get("should_trigger"), bool):
            errors.append(f"{label}: should_trigger must be boolean")
        else:
            counts[case["should_trigger"]] += 1
        if case.get("id") in ids:
            errors.append(f"{label}: duplicate id {case.get('id')}")
        ids.add(case.get("id"))
    if counts[True] < 8 or counts[False] < 8:
        errors.append(f"{path}: need at least 8 trigger and 8 non-trigger cases")
    return errors


def validate_behavior_evals(path: Path) -> list[str]:
    try:
        cases = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return [f"{path}: invalid JSON: {error}"]
    errors: list[str] = []
    if not isinstance(cases, list):
        return [f"{path}: expected a list"]
    ids: set[str] = set()
    for index, case in enumerate(cases):
        label = f"{path}[{index}]"
        if not isinstance(case, dict):
            errors.append(f"{label}: expected an object")
            continue
        for key in ("id", "prompt", "risk"):
            if not isinstance(case.get(key), str) or not case[key].strip():
                errors.append(f"{label}: {key} must be a non-empty string")
        for key in ("expected", "forbidden"):
            value = case.get(key)
            if not isinstance(value, list) or not value or not all(
                isinstance(item, str) and item.strip() for item in value
            ):
                errors.append(f"{label}: {key} must be a non-empty string list")
        if case.get("id") in ids:
            errors.append(f"{label}: duplicate id {case.get('id')}")
        ids.add(case.get("id"))
    return errors


def validate_repo(repo_root: Path) -> list[str]:
    repo_root = repo_root.resolve()
    skill_dir = repo_root / "skills" / "prompt-chain"
    english = skill_dir / "SKILL.md"
    portuguese = skill_dir / "SKILL.pt-BR.md"
    errors: list[str] = []

    en_errors, en_data = validate_skill_file(english)
    pt_errors, pt_data = validate_skill_file(portuguese)
    errors.extend(en_errors)
    errors.extend(pt_errors)
    if en_data and pt_data:
        en_metadata = en_data.get("metadata")
        pt_metadata = pt_data.get("metadata")
        en_version = en_metadata.get("version") if isinstance(en_metadata, dict) else None
        pt_version = pt_metadata.get("version") if isinstance(pt_metadata, dict) else None
        if en_version != pt_version:
            errors.append("English and PT-BR metadata.version values differ")
        if en_data.get("name") != pt_data.get("name"):
            errors.append("English and PT-BR skill names differ")

    errors.extend(validate_markdown_links(repo_root))
    errors.extend(validate_trigger_evals(repo_root / "evals" / "trigger-evals.json"))
    errors.extend(validate_behavior_evals(repo_root / "evals" / "behavior-evals.json"))
    errors.extend(validate_package(skill_dir, repo_root / "prompt-chain.skill"))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "repo_root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1]
    )
    args = parser.parse_args()
    errors = validate_repo(args.repo_root)
    if errors:
        print("VALIDATION FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    print("VALIDATION PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
