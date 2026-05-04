from __future__ import annotations

import json
import re
import subprocess
import ast
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


EXCLUDED_DIRS = {
    ".git",
    ".claude",
    ".codex",
    ".cursor",
    ".taskmaster",
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
    "dist-types",
    "build",
    "coverage",
    "dev-dist",
    "playwright-report",
    "test-results",
    ".next",
    ".vite",
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
    directory_profiles: list[dict[str, Any]] = field(default_factory=list)
    detected_domains: list[dict[str, str]] = field(default_factory=list)
    key_files: dict[str, list[str]] = field(default_factory=dict)
    manifests: list[dict[str, str]] = field(default_factory=list)
    package_managers: list[str] = field(default_factory=list)
    dependencies: dict[str, list[str]] = field(default_factory=dict)
    commands: list[dict[str, str]] = field(default_factory=list)
    entrypoints: list[str] = field(default_factory=list)
    api_routes: list[dict[str, str]] = field(default_factory=list)
    frontend_routes: list[dict[str, str]] = field(default_factory=list)
    frontend_api_calls: list[dict[str, str]] = field(default_factory=list)
    workflow_summaries: list[dict[str, Any]] = field(default_factory=list)
    backend_signals: list[str] = field(default_factory=list)
    frontend_signals: list[str] = field(default_factory=list)
    data_signals: list[str] = field(default_factory=list)
    business_signals: list[str] = field(default_factory=list)
    business_artifacts: list[dict[str, str]] = field(default_factory=list)
    client_domains: list[str] = field(default_factory=list)
    readme_summary: list[str] = field(default_factory=list)
    doc_headings: list[dict[str, str]] = field(default_factory=list)
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

    directory_profiles = _directory_profiles(rel_files)
    analysis = RepoAnalysis(
        repo_root=root,
        repo_name=root.name,
        files_scanned=len(files),
        files_truncated=truncated,
        git=_git_summary(root),
        languages=_language_summary(files),
        top_level_dirs=_top_level_dirs(root),
        directory_profiles=directory_profiles,
        detected_domains=_detected_domains(directory_profiles),
        key_files=_key_files(rel_files),
        manifests=_manifests(root, rel_files),
        package_managers=_package_managers(root, rel_files),
        dependencies=_dependencies(root, rel_files),
        commands=_commands(root, rel_files),
        entrypoints=_entrypoints(root, rel_files),
        api_routes=_api_routes(root, files),
        frontend_routes=_frontend_routes(root, files),
        frontend_api_calls=_frontend_api_calls(root, files),
        workflow_summaries=_workflow_summaries(root, files),
        backend_signals=_area_signals(root, files, "backend"),
        frontend_signals=_area_signals(root, files, "frontend"),
        data_signals=_area_signals(root, files, "data"),
        business_signals=_area_signals(root, files, "business"),
        business_artifacts=_business_artifacts(root, files),
        client_domains=_client_domains(root),
        readme_summary=_readme_summary(root),
        doc_headings=_doc_headings(root, files),
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
    if path.name in {".DS_Store", ".gitkeep"}:
        return True
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


def _directory_profiles(rel_files: list[str]) -> list[dict[str, Any]]:
    grouped: dict[str, list[str]] = {}
    for rel in rel_files:
        parts = rel.split("/")
        if len(parts) < 2:
            continue
        top = parts[0]
        if top.startswith(".") and top != ".github":
            continue
        grouped.setdefault(top, []).append(rel)

    profiles = []
    for top, files in sorted(grouped.items()):
        language_counts: Counter[str] = Counter()
        for rel in files:
            language = LANGUAGE_BY_EXTENSION.get(Path(rel).suffix.lower())
            if language:
                language_counts[language] += 1
        profiles.append({
            "name": top,
            "files": len(files),
            "purpose": _directory_purpose(top),
            "languages": [language for language, _ in language_counts.most_common(3)],
            "notable_files": _notable_files(files)[:4],
        })
    return profiles[:30]


def _detected_domains(directory_profiles: list[dict[str, Any]]) -> list[dict[str, str]]:
    domains = []
    for profile in directory_profiles:
        name = profile["name"]
        files = profile["files"]
        if files < 2 and name not in {"web", "clients", "agents", "semantic_layer", "governance", "PRD", "prd"}:
            continue
        if name in {".github", "tests", "docs"} and files < 8:
            continue
        evidence = ", ".join(f"`{path}`" for path in profile["notable_files"][:3]) or f"`{name}/`"
        domains.append({
            "slug": _slugify(name),
            "status": "Confirmed" if files >= 4 else "Likely",
            "why": profile["purpose"],
            "evidence": evidence,
            "first_read": profile["notable_files"][0] if profile["notable_files"] else f"{name}/",
        })
    return domains[:18]


def _slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "domain"


def _directory_purpose(name: str) -> str:
    purposes = {
        ".github": "CI and repository automation",
        "agents": "automation or agent workflows",
        "apps": "application surfaces and local tooling",
        "clients": "client, tenant, or customer-specific artifacts",
        "connectors": "external-system connector abstractions",
        "docs": "architecture, setup, audit, and project documentation",
        "evals": "evaluation harnesses or fixtures",
        "examples": "sample inputs and usage examples",
        "governance": "quality gates, contracts, maturity checks, and freshness/audit logic",
        "llm": "LLM provider adapters and model-call abstractions",
        "pipelines": "offline processing pipelines and artifact generation helpers",
        "scripts": "one-off or operational command-line scripts",
        "semantic_layer": "shared dimensions, metric loading, and semantic-layer primitives",
        "tests": "unit/integration tests and fixtures",
        "tools": "shared utility layer used by agents, scripts, and apps",
        "web": "FastAPI backend plus React/Vite frontend",
        "packages": "monorepo packages or services",
        "mockup": "static mockups or product prototypes",
        "prd": "product requirements and planning docs",
        "PRD": "product requirements and planning docs",
    }
    return purposes.get(name, "repository area")


def _notable_files(files: list[str]) -> list[str]:
    priority_names = ("README.md", "pyproject.toml", "package.json", "requirements.txt", "__main__.py", "main.py", "server.py")
    notable = [rel for rel in sorted(files) if Path(rel).name in priority_names]
    if len(notable) < 4:
        notable.extend(rel for rel in sorted(files) if rel not in notable and Path(rel).suffix.lower() in {".md", ".py", ".tsx", ".yml", ".yaml"})
    return notable


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


def _manifests(root: Path, rel_files: list[str]) -> list[dict[str, str]]:
    manifest_names = {
        "package.json": "npm package",
        "package-lock.json": "npm lockfile",
        "pnpm-lock.yaml": "pnpm lockfile",
        "yarn.lock": "yarn lockfile",
        "pyproject.toml": "python project",
        "requirements.txt": "python requirements",
        "Makefile": "make targets",
        "go.mod": "go module",
        "Cargo.toml": "rust crate",
        "docker-compose.yml": "docker compose",
        "docker-compose.yaml": "docker compose",
        "Dockerfile": "docker image",
    }
    manifests = []
    for rel in sorted(rel_files):
        name = Path(rel).name
        kind = manifest_names.get(name)
        if kind:
            manifests.append({"path": rel, "kind": kind})
    return manifests[:80]


def _package_managers(root: Path, rel_files: list[str]) -> list[str]:
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
    names = {Path(rel).name for rel in rel_files}
    found = [name for name, marker in markers.items() if marker in names]
    # Preserve the old root-marker behavior for callers that inspect local fixtures.
    for name, marker in markers.items():
        if (root / marker).exists() and name not in found:
            found.append(name)
    return found


def _dependencies(root: Path, rel_files: list[str]) -> dict[str, list[str]]:
    deps: dict[str, list[str]] = {}
    for rel in sorted(rel_files):
        path = root / rel
        name = path.name
        if name == "package.json":
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                js_deps = sorted(set(data.get("dependencies", {})) | set(data.get("devDependencies", {})))
                deps[rel] = js_deps[:40]
            except Exception:
                deps[rel] = ["Could not parse package.json"]
        elif name == "pyproject.toml":
            try:
                text = path.read_text(encoding="utf-8")
                parsed = _pyproject_dependencies(text)
                if parsed:
                    deps[rel] = parsed[:40]
            except Exception:
                deps[rel] = ["Could not parse pyproject.toml"]
        elif name == "requirements.txt":
            lines = [
                line.strip()
                for line in path.read_text(encoding="utf-8", errors="ignore").splitlines()
                if line.strip() and not line.strip().startswith("#")
            ]
            deps[rel] = lines[:40]
        if len(deps) >= 20:
            break
    return deps


def _commands(root: Path, rel_files: list[str]) -> list[dict[str, str]]:
    commands: list[dict[str, str]] = []
    for rel in sorted(rel_files):
        path = root / rel
        name = path.name
        parent = Path(rel).parent.as_posix()
        prefix = "" if parent == "." else f"cd {parent} && "
        if name == "package.json":
            try:
                scripts = json.loads(path.read_text(encoding="utf-8")).get("scripts", {})
                for script_name, command in sorted(scripts.items()):
                    commands.append({
                        "source": rel,
                        "name": script_name,
                        "command": f"{prefix}npm run {script_name}",
                        "details": command,
                    })
            except Exception:
                pass
        elif name == "pyproject.toml":
            try:
                scripts = _pyproject_scripts(path.read_text(encoding="utf-8"))
                for script_name, target in sorted(scripts.items()):
                    commands.append({
                        "source": rel,
                        "name": script_name,
                        "command": f"{prefix}{script_name}",
                        "details": str(target),
                    })
            except Exception:
                pass
        elif name == "Makefile":
            for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
                if line and not line.startswith(("\t", ".", "#")) and ":" in line:
                    target = line.split(":", 1)[0].strip()
                    if target:
                        commands.append({
                            "source": rel,
                            "name": target,
                            "command": f"{prefix}make {target}",
                            "details": "",
                        })

    if not any(command["name"] == "pytest" for command in commands) and _has_tests(rel_files):
        commands.append({
            "source": "tests/",
            "name": "pytest",
            "command": "python -m pytest",
            "details": "inferred from Python tests",
        })
    return commands[:80]


def _entrypoints(root: Path, rel_files: list[str]) -> list[str]:
    entrypoints: list[str] = []
    strong_names = {
        "__main__.py",
        "main.py",
        "app.py",
        "server.py",
        "api.py",
        "manage.py",
        "asgi.py",
        "wsgi.py",
        "index.ts",
        "index.tsx",
        "main.ts",
        "main.tsx",
        "App.tsx",
    }
    for rel in sorted(rel_files):
        path = root / rel
        if path.name in strong_names:
            entrypoints.append(rel)
        elif path.name == "pyproject.toml":
            scripts = _pyproject_scripts(path.read_text(encoding="utf-8", errors="ignore"))
            for script_name, target in sorted(scripts.items()):
                entrypoints.append(f"{rel} [{script_name} -> {target}]")
        elif path.name == "package.json":
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                continue
            for field in ("main", "module", "bin"):
                value = data.get(field)
                if value:
                    entrypoints.append(f"{rel} [{field}: {value}]")
        if len(entrypoints) >= 30:
            break
    return entrypoints


def _api_routes(root: Path, files: list[Path]) -> list[dict[str, str]]:
    routes: list[dict[str, str]] = []
    route_pattern = re.compile(r"""@\w+\.(get|post|put|patch|delete)\(\s*['"]([^'"]+)['"]""")
    router_pattern = re.compile(r"""APIRouter\([^)]*prefix\s*=\s*['"]([^'"]+)['"]""")
    def_pattern = re.compile(r"""^\s*(?:async\s+)?def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(""")
    for path in sorted(files):
        rel = path.relative_to(root).as_posix()
        if not rel.endswith(".py"):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if "FastAPI" not in text and "APIRouter" not in text and "@app." not in text and "@router." not in text:
            continue
        prefix = ""
        prefix_match = router_pattern.search(text)
        if prefix_match:
            prefix = prefix_match.group(1).rstrip("/")
        function_actions = _python_function_actions(text)
        pending: list[dict[str, str]] = []
        for line_no, line in enumerate(text.splitlines(), start=1):
            match = route_pattern.search(line)
            if match:
                method = match.group(1).upper()
                route = match.group(2)
                full_route = f"{prefix}{route}" if prefix and route.startswith("/") else route
                pending.append({"method": method, "route": full_route, "path": rel, "line": str(line_no), "handler": ""})
                continue
            def_match = def_pattern.search(line)
            if def_match and pending:
                route = pending.pop(0)
                route["handler"] = def_match.group(1)
                route["actions"] = ", ".join(function_actions.get(route["handler"], [])[:5])
                routes.append(route)
                if len(routes) >= 40:
                    return routes
    return routes


def _python_function_actions(text: str) -> dict[str, list[str]]:
    try:
        module = ast.parse(text)
    except SyntaxError:
        return {}
    actions: dict[str, list[str]] = {}
    for node in ast.walk(module):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        calls = []
        for statement in node.body:
            for child in ast.walk(statement):
                if isinstance(child, ast.Call):
                    name = _call_name(child.func)
                    if name and not _ignore_call_name(name):
                        calls.append(name)
        actions[node.name] = _dedupe(calls)
    return actions


def _ignore_call_name(name: str) -> bool:
    ignored_exact = {"dict", "list", "str", "int", "len", "bool", "Path", "isinstance", "set"}
    ignored_prefixes = ("HTTPException", "app.", "router.", "body.get", "path.strip", "reason.strip", "edited_by.strip")
    return name in ignored_exact or name.startswith(ignored_prefixes)


def _call_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = _call_name(node.value)
        return f"{base}.{node.attr}" if base else node.attr
    return ""


def _dedupe(values: list[str]) -> list[str]:
    seen = set()
    result = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result


def _frontend_routes(root: Path, files: list[Path]) -> list[dict[str, str]]:
    routes: list[dict[str, str]] = []
    patterns = [
        re.compile(r"""path\s*=\s*['"]([^'"]+)['"]"""),
        re.compile(r"""\bpath\s*:\s*['"](/[^\s'"]*)['"]"""),
    ]
    element_pattern = re.compile(r"""element\s*=\s*\{\s*<([A-Za-z0-9_]+)""")
    for path in sorted(files):
        rel = path.relative_to(root).as_posix()
        if not rel.endswith((".tsx", ".jsx", ".ts", ".js")):
            continue
        lower = rel.lower()
        if ".test." in lower or ".spec." in lower:
            continue
        if not any(token in lower for token in ("frontend/", "routes", "app.")):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if "Route" not in text and "path" not in text:
            continue
        lines = text.splitlines()
        for line_no, line in enumerate(lines, start=1):
            for pattern in patterns:
                match = pattern.search(line)
                if match:
                    window = "\n".join(lines[line_no - 1: line_no + 8])
                    element_match = element_pattern.search(window)
                    routes.append({
                        "route": match.group(1),
                        "path": rel,
                        "line": str(line_no),
                        "element": element_match.group(1) if element_match else "",
                    })
                    break
            if len(routes) >= 40:
                return routes
    return routes


def _frontend_api_calls(root: Path, files: list[Path]) -> list[dict[str, str]]:
    calls: list[dict[str, str]] = []
    method_start_pattern = re.compile(r"""^\s{2}([A-Za-z0-9_]+):\s*""")
    helper_pattern = re.compile(r"""(getJSON|postJSON|putJSON)<[^>]+>\(\s*([`'"][\s\S]*?[`'"])""")
    for path in sorted(files):
        rel = path.relative_to(root).as_posix()
        if not rel.endswith((".ts", ".tsx", ".js", ".jsx")):
            continue
        if not rel.lower().endswith(("api.ts", "api.tsx", "api.js")):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        lines = text.splitlines()
        for index, line in enumerate(lines):
            start_match = method_start_pattern.search(line)
            if not start_match:
                continue
            name = start_match.group(1)
            window = "\n".join(lines[index:index + 8])
            helper_match = helper_pattern.search(window)
            if not helper_match:
                continue
            helper, expression = helper_match.groups()
            route = _extract_route_expression(expression)
            calls.append({
                "name": name,
                "method": {"getJSON": "GET", "postJSON": "POST", "putJSON": "PUT"}.get(helper, helper),
                "route": route,
                "path": rel,
                "line": str(index + 1),
            })
            if len(calls) >= 60:
                return calls
    return calls


def _extract_route_expression(expression: str) -> str:
    expression = expression.strip()
    match = re.search(r"""[`'"]([^`'"]+)""", expression)
    if not match:
        return expression[:100]
    return match.group(1)


def _workflow_summaries(root: Path, files: list[Path]) -> list[dict[str, Any]]:
    summaries: list[dict[str, Any]] = []
    for path in sorted(files):
        rel = path.relative_to(root).as_posix()
        if not rel.startswith("agents/") or not rel.endswith("workflow.py"):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
            module = ast.parse(text)
        except (OSError, SyntaxError):
            continue
        doc = ast.get_docstring(module) or ""
        functions = [
            node.name
            for node in module.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and not node.name.startswith("_")
        ]
        imports = _module_imports(module)
        dataclasses = _contract_classes(root, rel)
        summaries.append({
            "path": rel,
            "workflow": rel.split("/")[1] if "/" in rel else rel,
            "doc": _clean_summary(doc),
            "functions": functions[:6],
            "imports": imports[:8],
            "contracts": dataclasses[:8],
        })
        if len(summaries) >= 20:
            break
    return summaries


def _module_imports(module: ast.Module) -> list[str]:
    names: list[str] = []
    for node in module.body:
        if isinstance(node, ast.ImportFrom) and node.module:
            for alias in node.names:
                names.append(f"{node.module}.{alias.name}")
        elif isinstance(node, ast.Import):
            for alias in node.names:
                names.append(alias.name)
    return names


def _contract_classes(root: Path, workflow_rel: str) -> list[str]:
    contract_path = root / Path(workflow_rel).parent / "contracts.py"
    if not contract_path.exists():
        return []
    try:
        module = ast.parse(contract_path.read_text(encoding="utf-8", errors="ignore"))
    except (OSError, SyntaxError):
        return []
    return [node.name for node in module.body if isinstance(node, ast.ClassDef)]


def _clean_summary(text: str) -> str:
    return " ".join(line.strip() for line in text.splitlines() if line.strip())[:180]


def _area_signals(root: Path, files: list[Path], area: str) -> list[str]:
    signals: list[str] = []
    group_counts: Counter[str] = Counter()
    for path in sorted(files, key=lambda candidate: _area_priority(candidate.relative_to(root).as_posix(), area)):
        rel = path.relative_to(root).as_posix()
        lower = rel.lower()
        suffix = path.suffix.lower()
        text = ""
        if suffix in {".py", ".ts", ".tsx", ".js", ".jsx", ".json", ".yml", ".yaml", ".md", ".toml", ".sql"}:
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")[:20000]
            except OSError:
                text = ""

        signal = _area_signal_for_file(rel, lower, text, area)
        if signal and signal not in signals:
            group = _area_group(rel, area)
            if area in {"backend", "data", "business"} and group_counts[group] >= 3:
                continue
            group_counts[group] += 1
            signals.append(signal)
        if len(signals) >= 18:
            break
    return signals


def _area_group(rel: str, area: str) -> str:
    parts = rel.split("/")
    if area == "backend" and len(parts) >= 2 and parts[0] == "agents":
        return "agents"
    if area == "data" and len(parts) >= 3 and parts[0] == "clients":
        return "/".join(parts[:2])
    return parts[0] if parts else rel


def _area_priority(rel: str, area: str) -> tuple[int, str]:
    lower = rel.lower()
    if area == "backend":
        for index, prefix in enumerate(("web/api/", "apps/", "agents/", "connectors/", "pipelines/", "tools/", "llm/")):
            if lower.startswith(prefix):
                return (index, lower)
    if area == "frontend" and any(token in lower for token in ("web/frontend/", "frontend/", "ui/", "components/", "pages/")):
        return (0, lower)
    if area == "data":
        for index, prefix in enumerate(("semantic_layer/", "clients/", "governance/", "pipelines/", "agents/validate_semantic_layer/")):
            if lower.startswith(prefix):
                return (index, lower)
    if area == "business" and any(token in lower for token in ("clients/", "docs/", "governance/", "examples/", "prd/")):
        return (0, lower)
    return (1, lower)


def _area_signal_for_file(rel: str, lower: str, text: str, area: str) -> str:
    lower_text = text.lower()
    name = Path(lower).name
    if name in {"__init__.py", ".gitignore", "package-lock.json", "pnpm-lock.yaml", "yarn.lock"} or lower.endswith(".tsbuildinfo"):
        return ""
    if area in {"backend", "data", "frontend"} and lower.startswith(("tests/", ".github/")):
        return ""
    if area == "backend":
        if any(lower.startswith(prefix) for prefix in ("web/api/", "apps/", "agents/", "connectors/", "pipelines/", "tools/", "llm/")):
            return f"`{rel}` - backend/service module path"
        if any(token in text for token in ("FastAPI(", "APIRouter", "Flask(", "Django", "argparse.ArgumentParser", "typer.")):
            return f"`{rel}` - backend entrypoint/framework signal"
        if any(token in lower_text for token in ("sqlalchemy", "pydantic", "requests.", "openai", "anthropic")) and rel.endswith(".py"):
            return f"`{rel}` - integration or service dependency signal"
    elif area == "frontend":
        if any(token in lower for token in ("web/frontend/", "frontend/", "ui/", "components/", "pages/")):
            return f"`{rel}` - frontend application path"
        frontend_source = lower.endswith((".tsx", ".jsx", ".css", ".scss")) or lower.endswith("package.json")
        if frontend_source and any(token in lower_text for token in ("react", "vite", "next", "tsx", "tailwind", "lucide-react")):
            return f"`{rel}` - frontend framework signal"
    elif area == "data":
        if any(lower.startswith(prefix) for prefix in ("semantic_layer/", "clients/", "pipelines/", "governance/", "agents/validate_semantic_layer/")):
            return f"`{rel}` - data or domain asset path"
        data_source = lower.endswith((".sql", ".yml", ".yaml"))
        if lower.endswith(".sql") or (data_source and any(token in lower_text for token in ("metric", "dbt", "warehouse", "snowflake", "semantic layer"))):
            return f"`{rel}` - data model or metric signal"
    elif area == "business":
        business_path = any(token in lower for token in ("clients/", "docs/", "governance/", "examples/", "prd/"))
        business_text = any(token in lower_text for token in (
            "stakeholder",
            "customer",
            "client",
            "business",
            "metric",
            "kpi",
            "revenue",
            "governance",
            "workflow",
            "onboarding",
        ))
        if business_path and business_text:
            return f"`{rel}` - business usage or domain context"
    return ""


def _client_domains(root: Path) -> list[str]:
    clients = root / "clients"
    if not clients.exists() or not clients.is_dir():
        return []
    names = []
    for path in sorted(clients.iterdir()):
        if path.is_dir() and not path.name.startswith("."):
            names.append(path.name)
    return names[:40]


def _business_artifacts(root: Path, files: list[Path]) -> list[dict[str, str]]:
    artifacts: list[dict[str, str]] = []
    keywords = {
        "prd": "product requirements",
        "profile": "client profile",
        "stakeholders": "stakeholder map",
        "requirements": "requirements",
        "metrics": "metric definition",
        "knowledge_base": "knowledge base",
        "onboarding": "onboarding guide",
        "brief": "business brief",
        "constraints": "business/data constraints",
        "artifact_index": "artifact registry",
        "evidence": "evidence pack",
    }
    for path in sorted(files):
        rel = path.relative_to(root).as_posix()
        lower = rel.lower()
        if not lower.startswith(("clients/", "semantic_layer/", "governance/", "docs/", "examples/", "prd/")):
            continue
        kind = ""
        for token, label in keywords.items():
            if token in lower:
                kind = label
                break
        if not kind:
            continue
        artifacts.append({"path": rel, "kind": kind, "title": _artifact_title(path)})
        if len(artifacts) >= 30:
            break
    return artifacts


def _artifact_title(path: Path) -> str:
    if path.suffix.lower() in {".md", ".markdown"}:
        try:
            for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
                stripped = line.strip()
                if not stripped or stripped in {"---", "```"}:
                    continue
                if stripped.startswith(("<!--", "*Generated:", "*Updated:")):
                    continue
                if stripped.startswith("#"):
                    return stripped.lstrip("#").strip()[:120]
                if path.suffix.lower() in {".md", ".markdown"}:
                    return stripped[:120]
        except OSError:
            return ""
    return ""


def _readme_summary(root: Path) -> list[str]:
    path = root / "README.md"
    if not path.exists():
        return []
    try:
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except OSError:
        return []

    summary: list[str] = []
    in_project_section = False
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        heading = stripped.lstrip("#").strip().lower() if stripped.startswith("#") else ""
        if heading:
            in_project_section = any(token in heading for token in ("project", "projekcie", "overview", "about", "opis"))
            if len(summary) < 1 and stripped.startswith("# "):
                title = stripped.lstrip("#").strip()
                summary.append(f"README title: {title}")
            continue
        if stripped.startswith(("-", "*", "```", "|", "[", "![", "<", ">")):
            continue
        if len(stripped) < 24:
            continue
        if in_project_section or len(summary) < 3:
            summary.append(_shorten(stripped, 220))
        if len(summary) >= 5:
            break
    return summary


def _shorten(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    shortened = text[:limit].rsplit(" ", 1)[0].rstrip(".,;:")
    return f"{shortened}..."


def _doc_headings(root: Path, files: list[Path]) -> list[dict[str, str]]:
    headings: list[dict[str, str]] = []
    for path in sorted(files, key=lambda candidate: _doc_sort_key(candidate.relative_to(root).as_posix())):
        rel = path.relative_to(root).as_posix()
        lower = rel.lower()
        if not lower.endswith(".md"):
            continue
        if not (lower == "readme.md" or lower.startswith(("docs/", "web/readme", "clients/"))):
            continue
        try:
            lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        except OSError:
            continue
        for line_no, line in enumerate(lines, start=1):
            stripped = line.strip()
            if not stripped.startswith("#"):
                continue
            level = len(stripped) - len(stripped.lstrip("#"))
            if level > 3:
                continue
            title = stripped.lstrip("#").strip()
            if not title:
                continue
            headings.append({"path": rel, "line": str(line_no), "heading": title})
            if len(headings) >= 40:
                return headings
    return headings


def _has_tests(rel_files: list[str]) -> bool:
    return any(
        rel.lower().startswith(("tests/", "test/"))
        or "/tests/" in rel.lower()
        or Path(rel.lower()).name.startswith("test_")
        for rel in rel_files
    )


def _legacy_dependencies(root: Path) -> dict[str, list[str]]:
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
    marker_pattern = re.compile(r"\b(TODO|FIXME|HACK)\b")
    hits: list[dict[str, str]] = []
    for path in files:
        if path.suffix.lower() in BINARY_EXTENSIONS:
            continue
        try:
            lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        except OSError:
            continue
        for index, line in enumerate(lines, start=1):
            if marker_pattern.search(line):
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
