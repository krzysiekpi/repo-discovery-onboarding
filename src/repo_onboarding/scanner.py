from __future__ import annotations

import json
import re
import subprocess
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


EXCLUDED_DIRS = {
    ".git",
    ".claude",
    ".codex",
    ".hg",
    ".svn",
    ".venv",
    ".codex-pdf-venv",
    "venv",
    "env",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "node_modules",
    "dist",
    "build",
    "coverage",
    ".next",
    ".turbo",
    "target",
    "tmp",
    "runs",
    "reports",
    "worktrees",
}

BINARY_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".ico",
    ".pdf",
    ".zip",
    ".gz",
    ".tar",
    ".woff",
    ".woff2",
    ".ttf",
    ".eot",
    ".mp4",
    ".mov",
    ".sqlite",
    ".db",
}

LANGUAGE_BY_EXTENSION = {
    ".py": "Python",
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".go": "Go",
    ".rs": "Rust",
    ".java": "Java",
    ".kt": "Kotlin",
    ".rb": "Ruby",
    ".php": "PHP",
    ".cs": "C#",
    ".sql": "SQL",
    ".sh": "Shell",
    ".md": "Markdown",
    ".yml": "YAML",
    ".yaml": "YAML",
    ".json": "JSON",
    ".toml": "TOML",
    ".css": "CSS",
    ".scss": "CSS",
    ".html": "HTML",
}


@dataclass
class RepoAnalysis:
    repo_root: Path
    repo_name: str
    files_scanned: int
    files_truncated: bool
    git: dict[str, str] = field(default_factory=dict)
    languages: list[dict[str, Any]] = field(default_factory=list)
    top_level_dirs: list[str] = field(default_factory=list)
    key_files: dict[str, list[str]] = field(default_factory=dict)
    package_managers: list[str] = field(default_factory=list)
    dependencies: dict[str, list[str]] = field(default_factory=dict)
    commands: list[dict[str, str]] = field(default_factory=list)
    test_signals: list[str] = field(default_factory=list)
    ci_signals: list[str] = field(default_factory=list)
    docs: list[str] = field(default_factory=list)
    env_signals: list[str] = field(default_factory=list)
    todos: list[dict[str, str]] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)


def analyze_repo(repo_root: Path | str, *, max_files: int = 5000) -> RepoAnalysis:
    root = Path(repo_root).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        raise FileNotFoundError(f"Repository path does not exist or is not a directory: {root}")

    files = list(_iter_repo_files(root, max_files=max_files + 1))
    truncated = len(files) > max_files
    files = files[:max_files]
    rel_files = [path.relative_to(root).as_posix() for path in files]

    analysis = RepoAnalysis(
        repo_root=root,
        repo_name=root.name,
        files_scanned=len(files),
        files_truncated=truncated,
        git=_git_summary(root),
        languages=_language_summary(files),
        top_level_dirs=_top_level_dirs(root),
        key_files=_key_files(rel_files),
        package_managers=_package_managers(root),
        dependencies=_dependencies(root),
        commands=_commands(root),
        test_signals=_test_signals(rel_files),
        ci_signals=_ci_signals(rel_files),
        docs=_docs(rel_files),
        env_signals=_env_signals(rel_files),
        todos=_todos(root, files),
    )
    analysis.risks = _risks(analysis)
    return analysis


def _iter_repo_files(root: Path, *, max_files: int) -> list[Path]:
    collected: list[Path] = []
    for path in root.rglob("*"):
        if len(collected) >= max_files:
            break
        if _is_excluded(path, root):
            continue
        if path.is_file() and path.suffix.lower() not in BINARY_EXTENSIONS:
            collected.append(path)
    return collected


def _is_excluded(path: Path, root: Path) -> bool:
    rel_parts = path.relative_to(root).parts
    for part in rel_parts:
        if part in EXCLUDED_DIRS:
            return True
        if part.endswith(".egg-info"):
            return True
        if part.startswith(".venv"):
            return True
    return path.is_file() and _is_sensitive_env_file(path.name)


def _is_sensitive_env_file(name: str) -> bool:
    lower = name.lower()
    if lower in {".env", ".env.local", ".env.production", ".env.development", ".env.test"}:
        return True
    if lower.startswith(".env.") and "example" not in lower and "sample" not in lower:
        return True
    return False


def _git_summary(root: Path) -> dict[str, str]:
    return {
        "branch": _git(root, "rev-parse", "--abbrev-ref", "HEAD"),
        "latest_commit": _git(root, "log", "-1", "--pretty=%h %s"),
        "remote": _git(root, "remote", "get-url", "origin"),
    }


def _git(root: Path, *args: str) -> str:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=root,
            capture_output=True,
            text=True,
            check=False,
            timeout=5,
        )
    except Exception:
        return ""
    return result.stdout.strip() if result.returncode == 0 else ""


def _language_summary(files: list[Path]) -> list[dict[str, Any]]:
    counts: Counter[str] = Counter()
    line_counts: Counter[str] = Counter()
    for path in files:
        language = LANGUAGE_BY_EXTENSION.get(path.suffix.lower())
        if not language:
            continue
        counts[language] += 1
        if path.suffix.lower() in BINARY_EXTENSIONS:
            continue
        try:
            line_counts[language] += len(path.read_text(encoding="utf-8", errors="ignore").splitlines())
        except OSError:
            continue

    return [
        {"language": language, "files": counts[language], "lines": line_counts[language]}
        for language, _ in counts.most_common()
    ]


def _top_level_dirs(root: Path) -> list[str]:
    dirs = []
    for path in sorted(root.iterdir()):
        if not path.is_dir() or path.name in EXCLUDED_DIRS or path.name.endswith(".egg-info"):
            continue
        if path.name.startswith(".") and path.name != ".github":
            continue
        if path.name.startswith(".venv"):
            continue
        dirs.append(path.name)
    return dirs[:30]


def _key_files(rel_files: list[str]) -> dict[str, list[str]]:
    buckets = {
        "readme": [],
        "package": [],
        "docker": [],
        "ci": [],
        "config": [],
        "database": [],
    }
    for rel in rel_files:
        name = Path(rel).name.lower()
        if name.startswith("readme"):
            buckets["readme"].append(rel)
        if name in {"package.json", "pyproject.toml", "requirements.txt", "go.mod", "cargo.toml", "pom.xml", "gemfile"}:
            buckets["package"].append(rel)
        if name in {"dockerfile", "docker-compose.yml", "docker-compose.yaml"}:
            buckets["docker"].append(rel)
        if rel.startswith(".github/workflows/"):
            buckets["ci"].append(rel)
        if name in {".env.example", "settings.py", "config.py", "appsettings.json"} or name.endswith(".config.js"):
            buckets["config"].append(rel)
        if name in {"schema.sql", "migrations"} or "migration" in rel.lower():
            buckets["database"].append(rel)
    return {key: sorted(values)[:20] for key, values in buckets.items() if values}


def _package_managers(root: Path) -> list[str]:
    markers = {
        "npm": "package.json",
        "npm lockfile": "package-lock.json",
        "pnpm": "pnpm-lock.yaml",
        "yarn": "yarn.lock",
        "pip": "requirements.txt",
        "python/pyproject": "pyproject.toml",
        "poetry": "poetry.lock",
        "uv": "uv.lock",
        "go": "go.mod",
        "cargo": "Cargo.toml",
    }
    return [name for name, marker in markers.items() if (root / marker).exists()]


def _dependencies(root: Path) -> dict[str, list[str]]:
    deps: dict[str, list[str]] = {}
    package_json = root / "package.json"
    if package_json.exists():
        try:
            data = json.loads(package_json.read_text(encoding="utf-8"))
            js_deps = sorted(set(data.get("dependencies", {})) | set(data.get("devDependencies", {})))
            deps["package.json"] = js_deps[:40]
        except Exception:
            deps["package.json"] = ["Could not parse package.json"]

    pyproject = root / "pyproject.toml"
    if pyproject.exists():
        try:
            text = pyproject.read_text(encoding="utf-8")
            deps["pyproject.toml"] = _pyproject_dependencies(text)[:40]
        except Exception:
            deps["pyproject.toml"] = ["Could not parse pyproject.toml"]

    requirements = root / "requirements.txt"
    if requirements.exists():
        lines = [
            line.strip()
            for line in requirements.read_text(encoding="utf-8", errors="ignore").splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]
        deps["requirements.txt"] = lines[:40]
    return deps


def _commands(root: Path) -> list[dict[str, str]]:
    commands: list[dict[str, str]] = []
    package_json = root / "package.json"
    if package_json.exists():
        try:
            scripts = json.loads(package_json.read_text(encoding="utf-8")).get("scripts", {})
            for name, command in sorted(scripts.items()):
                commands.append({"source": "package.json", "name": name, "command": f"npm run {name}", "details": command})
        except Exception:
            pass

    pyproject = root / "pyproject.toml"
    if pyproject.exists():
        try:
            scripts = _pyproject_scripts(pyproject.read_text(encoding="utf-8"))
            for name, target in sorted(scripts.items()):
                commands.append({"source": "pyproject.toml", "name": name, "command": name, "details": str(target)})
        except Exception:
            pass

    if (root / "Makefile").exists():
        for line in (root / "Makefile").read_text(encoding="utf-8", errors="ignore").splitlines():
            if line and not line.startswith(("\t", ".", "#")) and ":" in line:
                target = line.split(":", 1)[0].strip()
                if target:
                    commands.append({"source": "Makefile", "name": target, "command": f"make {target}", "details": ""})
    return commands[:60]


def _pyproject_dependencies(text: str) -> list[str]:
    match = re.search(r"(?ms)^dependencies\s*=\s*\[(.*?)\]", _section(text, "project"))
    if not match:
        return []
    return re.findall(r"""['"]([^'"]+)['"]""", match.group(1))


def _pyproject_scripts(text: str) -> dict[str, str]:
    section = _section(text, "project.scripts")
    scripts: dict[str, str] = {}
    for line in section.splitlines():
        match = re.match(r"""^\s*([A-Za-z0-9_.-]+)\s*=\s*['"]([^'"]+)['"]\s*$""", line)
        if match:
            scripts[match.group(1)] = match.group(2)
    return scripts


def _section(text: str, name: str) -> str:
    pattern = rf"(?ms)^\[{re.escape(name)}\]\s*(.*?)(?=^\[|\Z)"
    match = re.search(pattern, text)
    return match.group(1) if match else ""


def _test_signals(rel_files: list[str]) -> list[str]:
    signals = []
    for rel in rel_files:
        lower = rel.lower()
        if lower.startswith(("tests/", "test/")) or "/tests/" in lower:
            signals.append(rel)
        elif Path(lower).name.startswith("test_") or Path(lower).name.endswith(".test.ts") or Path(lower).name.endswith(".spec.ts"):
            signals.append(rel)
    return sorted(signals)[:40]


def _ci_signals(rel_files: list[str]) -> list[str]:
    return sorted(rel for rel in rel_files if rel.startswith(".github/workflows/"))[:20]


def _docs(rel_files: list[str]) -> list[str]:
    docs = []
    for rel in rel_files:
        lower = rel.lower()
        if lower.startswith("docs/") or Path(lower).name.startswith("readme") or Path(lower).suffix == ".md":
            docs.append(rel)
    return sorted(docs, key=_doc_sort_key)[:60]


def _doc_sort_key(path: str) -> tuple[int, str]:
    lower = path.lower()
    if lower == "readme.md":
        return (0, lower)
    if lower.startswith("docs/"):
        return (1, lower)
    if lower.startswith("."):
        return (3, lower)
    return (2, lower)


def _env_signals(rel_files: list[str]) -> list[str]:
    names = {".env.example", ".env.sample", "env.example", "sample.env"}
    signals = [rel for rel in rel_files if Path(rel).name.lower() in names]
    return sorted(set(signals))


def _todos(root: Path, files: list[Path]) -> list[dict[str, str]]:
    markers = ("TODO", "FIXME", "HACK")
    hits: list[dict[str, str]] = []
    for path in files:
        if path.suffix.lower() in BINARY_EXTENSIONS:
            continue
        try:
            lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        except OSError:
            continue
        for index, line in enumerate(lines, start=1):
            if any(marker in line for marker in markers):
                hits.append({
                    "path": path.relative_to(root).as_posix(),
                    "line": str(index),
                    "text": line.strip()[:180],
                })
                if len(hits) >= 30:
                    return hits
    return hits


def _risks(analysis: RepoAnalysis) -> list[str]:
    risks = []
    if not analysis.docs:
        risks.append("No README/docs were detected; onboarding will depend on code inspection.")
    if not analysis.test_signals:
        risks.append("No tests were detected in common test locations.")
    if not analysis.ci_signals:
        risks.append("No GitHub Actions workflows were detected.")
    if not analysis.env_signals:
        risks.append("No environment example file was detected; local setup may require maintainer knowledge.")
    if analysis.files_truncated:
        risks.append("Scan reached the max-files limit; rerun with a higher --max-files value for full coverage.")
    if analysis.todos:
        risks.append(f"{len(analysis.todos)} TODO/FIXME/HACK markers detected in scanned files.")
    return risks
