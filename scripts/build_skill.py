#!/usr/bin/env python3
"""Build prompt-chain.skill deterministically from the canonical skill folder."""

from __future__ import annotations

import argparse
import tempfile
import zipfile
from pathlib import Path


FIXED_TIME = (1980, 1, 1, 0, 0, 0)
IGNORED_NAMES = {".DS_Store", "Thumbs.db"}


def _zip_info(name: str, mode: int) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(name, FIXED_TIME)
    info.create_system = 3
    info.external_attr = (mode & 0xFFFF) << 16
    info.compress_type = zipfile.ZIP_DEFLATED
    return info


def source_files(source_dir: Path) -> list[Path]:
    return sorted(
        path
        for path in source_dir.rglob("*")
        if path.is_file()
        and path.name not in IGNORED_NAMES
        and "__pycache__" not in path.parts
    )


def build_archive(source_dir: Path, output_path: Path) -> None:
    source_dir = source_dir.resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    root_name = source_dir.name

    with zipfile.ZipFile(
        output_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
    ) as archive:
        directory = _zip_info(f"{root_name}/", 0o40755)
        archive.writestr(directory, b"")
        for path in source_files(source_dir):
            relative = path.relative_to(source_dir).as_posix()
            archive.writestr(
                _zip_info(f"{root_name}/{relative}", 0o100644),
                path.read_bytes(),
                compress_type=zipfile.ZIP_DEFLATED,
                compresslevel=9,
            )


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source",
        type=Path,
        default=repo_root / "skills" / "prompt-chain",
    )
    parser.add_argument(
        "--output", type=Path, default=repo_root / "prompt-chain.skill"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit non-zero when the checked-in package is not reproducible.",
    )
    args = parser.parse_args()

    if args.check:
        with tempfile.TemporaryDirectory() as temporary:
            candidate = Path(temporary) / "prompt-chain.skill"
            build_archive(args.source, candidate)
            if not args.output.exists() or candidate.read_bytes() != args.output.read_bytes():
                print(f"STALE: rebuild {args.output} from {args.source}")
                return 1
        print(f"OK: {args.output} is reproducible")
        return 0

    build_archive(args.source, args.output)
    print(f"Built {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
