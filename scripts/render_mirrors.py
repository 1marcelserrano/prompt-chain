#!/usr/bin/env python3
"""Render the repository's two downstream prompt-chain mirrors."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

from build_skill import source_files


SOURCE_REPOSITORY = "https://github.com/1marcelserrano/prompt-chain"
SOURCE_PATH = "skills/prompt-chain/SKILL.md"
VERSION_PATTERN = re.compile(r'^  version: "([^"]+)"$', re.MULTILINE)


def sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def invite_skill(source: str) -> str:
    """Add the legacy top-level version field required by ms-skills."""
    match = VERSION_PATTERN.search(source)
    if not match:
        raise ValueError("canonical metadata.version was not found")
    version = match.group(1)
    lines = source.splitlines(keepends=True)
    for index, line in enumerate(lines):
        if line.startswith("name:"):
            lines.insert(index + 1, f'version: "{version}"\n')
            return "".join(lines)
    raise ValueError("canonical name field was not found")


def invite_readme(source: str) -> str:
    """Turn the canonical per-skill README into a mirror pointer."""
    replacements = {
        "This directory is the canonical installable skill.":
            "This directory is a generated distribution mirror.",
        "see the [repo root README](../../README.md).":
            "see the [canonical README](https://github.com/1marcelserrano/prompt-chain#readme).",
        "- `README.md` — this file":
            "- `README.md` — this file\n- `MIRROR.json` — machine-readable source and integrity record",
    }
    rendered = source
    for current, replacement in replacements.items():
        if current not in rendered:
            raise ValueError(f"canonical README contract changed: {current}")
        rendered = rendered.replace(current, replacement, 1)
    anchor = "Compatible agents load `SKILL.md`; `SKILL.pt-BR.md` is the maintained translation.\n"
    if anchor not in rendered:
        raise ValueError("canonical README compatibility line was not found")
    note = (
        "\nBehavioral changes belong in the "
        "[public canonical repository](https://github.com/1marcelserrano/prompt-chain). "
        "`MIRROR.json` records the source version and hashes used for this copy.\n"
    )
    return rendered.replace(anchor, anchor + note, 1)


def manifest(
    target_repository: str,
    target_path: str,
    profile: str,
    version: str,
    source_bytes: bytes,
    rendered_files: dict[str, bytes],
) -> bytes:
    data = {
        "schema_version": 1,
        "generated_by": "scripts/render_mirrors.py",
        "source": {
            "repository": SOURCE_REPOSITORY,
            "path": SOURCE_PATH,
            "version": version,
            "sha256": sha256(source_bytes),
        },
        "target": {
            "repository": target_repository,
            "path": target_path,
            "profile": profile,
        },
        "files": {
            name: sha256(content)
            for name, content in sorted(rendered_files.items())
        },
    }
    return (json.dumps(data, indent=2, ensure_ascii=False) + "\n").encode()


def write_target(root: Path, files: dict[str, bytes], manifest_bytes: bytes) -> None:
    root.mkdir(parents=True, exist_ok=True)
    for name, content in files.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    (root / "MIRROR.json").write_bytes(manifest_bytes)


def render_mirrors(repo_root: Path, output_root: Path) -> dict[str, Path]:
    if output_root.exists() and any(output_root.iterdir()):
        raise ValueError(f"output directory must be empty: {output_root}")

    source_dir = repo_root / "skills" / "prompt-chain"
    source_bytes = (source_dir / "SKILL.md").read_bytes()
    source_text = source_bytes.decode("utf-8")
    version_match = VERSION_PATTERN.search(source_text)
    if not version_match:
        raise ValueError("canonical metadata.version was not found")
    version = version_match.group(1)

    private_files = {"SKILL.md": source_bytes}
    private_root = output_root / "mscs-skills" / "skills" / "Infrastructure" / "prompt-chain"
    write_target(
        private_root,
        private_files,
        manifest(
            "https://github.com/1marcelserrano/mscs-skills",
            "skills/Infrastructure/prompt-chain",
            "portable-exact",
            version,
            source_bytes,
            private_files,
        ),
    )

    invite_files = {
        path.relative_to(source_dir).as_posix(): path.read_bytes()
        for path in source_files(source_dir)
    }
    invite_files["SKILL.md"] = invite_skill(source_text).encode("utf-8")
    invite_files["README.md"] = invite_readme(
        (source_dir / "README.md").read_text(encoding="utf-8")
    ).encode("utf-8")
    invite_root = output_root / "ms-skills" / "skills" / "prompt-chain"
    write_target(
        invite_root,
        invite_files,
        manifest(
            "https://github.com/1marcelserrano/ms-skills",
            "skills/prompt-chain",
            "invite-frontmatter",
            version,
            source_bytes,
            invite_files,
        ),
    )

    return {"mscs-skills": private_root, "ms-skills": invite_root}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    targets = render_mirrors(repo_root, args.output.resolve())
    for name, path in targets.items():
        print(f"{name}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
