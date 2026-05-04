from __future__ import annotations

import argparse
import logging
from pathlib import Path

from repo_onboarding.render import render_discovery, render_onboarding
from repo_onboarding.scanner import analyze_repo


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="repo-onboarding",
        description="Generate discovery and onboarding markdown docs from a local repository path.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    for name in ("discovery", "onboarding", "all"):
        command_parser = subparsers.add_parser(name)
        command_parser.add_argument("--repo", required=True, help="Path to the repository to analyze.")
        command_parser.add_argument(
            "--out",
            default="repo-onboarding-output",
            help="Output directory for generated markdown files.",
        )
        command_parser.add_argument(
            "--max-files",
            type=int,
            default=5000,
            help="Maximum files to scan before truncating large repositories.",
        )

    args = parser.parse_args(argv)
    try:
        analysis = analyze_repo(Path(args.repo), max_files=args.max_files)
    except Exception as exc:
        log.error("%s", exc)
        return 1

    out_dir = Path(args.out).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    written: list[Path] = []
    if args.command in {"discovery", "all"}:
        path = out_dir / "discovery.md"
        path.write_text(render_discovery(analysis), encoding="utf-8")
        written.append(path)
    if args.command in {"onboarding", "all"}:
        path = out_dir / "onboarding.md"
        path.write_text(render_onboarding(analysis), encoding="utf-8")
        written.append(path)

    for path in written:
        log.info("Wrote %s", path)
    return 0
