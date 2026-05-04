from __future__ import annotations

import argparse
import logging
from pathlib import Path

from repo_onboarding.render import normalize_role, render_discovery, render_onboarding
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
        command_parser.add_argument(
            "--role",
            default="all",
            help="Onboarding role focus: all, ceo, analyst, frontend, backend, data-governance, project-manager.",
        )
        command_parser.add_argument(
            "--update",
            action="store_true",
            help="Refresh onboarding while preserving the Manual Notes block.",
        )

    args = parser.parse_args(argv)
    try:
        analysis = analyze_repo(Path(args.repo), max_files=args.max_files)
    except Exception as exc:
        log.error("%s", exc)
        return 1

    out_dir = Path(args.out).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    try:
        role = normalize_role(args.role)
    except ValueError as exc:
        log.error("%s", exc)
        return 2

    written: list[Path] = []
    if args.command in {"discovery", "all"}:
        path = out_dir / "discovery.md"
        path.write_text(render_discovery(analysis), encoding="utf-8")
        written.append(path)
    if args.command in {"onboarding", "all"}:
        path = out_dir / _onboarding_filename(role)
        manual_notes = _read_manual_notes(path) if args.update else ""
        path.write_text(render_onboarding(analysis, role=role, manual_notes=manual_notes), encoding="utf-8")
        written.append(path)

    for path in written:
        log.info("Wrote %s", path)
    return 0


def _onboarding_filename(role: str) -> str:
    return "onboarding.md" if role == "all" else f"onboarding_{role}.md"


def _read_manual_notes(path: Path) -> str:
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8", errors="ignore")
    start = "<!-- MANUAL_NOTES:START -->"
    end = "<!-- MANUAL_NOTES:END -->"
    if start not in text or end not in text:
        return ""
    return text.split(start, 1)[1].split(end, 1)[0].strip()
