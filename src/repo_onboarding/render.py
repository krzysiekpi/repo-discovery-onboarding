from __future__ import annotations

from datetime import datetime

from repo_onboarding.scanner import RepoAnalysis


def render_discovery(analysis: RepoAnalysis) -> str:
    generated = datetime.now().strftime("%Y-%m-%d")
    return "\n".join([
        f"# Repository Discovery Report - {analysis.repo_name}",
        "",
        f"Generated: {generated}",
        f"Repository path: `{analysis.repo_root}`",
        "",
        "## 1. Snapshot",
        "",
        _snapshot(analysis),
        "",
        "## 2. Technology Signals",
        "",
        _language_table(analysis),
        "",
        "## 3. Repository Shape",
        "",
        _repo_shape(analysis),
        "",
        "## 4. Inferred Commands",
        "",
        _commands(analysis),
        "",
        "## 5. Tests, CI, and Operations",
        "",
        _ops(analysis),
        "",
        "## 6. Risks and Open Questions",
        "",
        _risks(analysis),
        "",
        "## 7. Suggested Next Steps",
        "",
        _next_steps(analysis),
        "",
    ])


def render_onboarding(analysis: RepoAnalysis) -> str:
    generated = datetime.now().strftime("%Y-%m-%d")
    return "\n".join([
        f"# Developer Onboarding Guide - {analysis.repo_name}",
        "",
        f"Generated: {generated}",
        "",
        "## 1. First 30 Minutes",
        "",
        _first_30_minutes(analysis),
        "",
        "## 2. Local Setup",
        "",
        _local_setup(analysis),
        "",
        "## 3. Architecture Tour",
        "",
        _architecture_tour(analysis),
        "",
        "## 4. Common Commands",
        "",
        _commands(analysis),
        "",
        "## 5. First Change Checklist",
        "",
        "\n".join([
            "- Create a small branch and make one isolated change.",
            "- Run the test or lint command listed above before opening a PR.",
            "- Update docs if the change affects setup, behavior, or public APIs.",
            "- Ask the maintainer to confirm any missing environment variables or external services.",
        ]),
        "",
        "## 6. Maintainer Questions",
        "",
        _maintainer_questions(analysis),
        "",
    ])


def _snapshot(analysis: RepoAnalysis) -> str:
    lines = [
        f"- Files scanned: {analysis.files_scanned}{' (truncated)' if analysis.files_truncated else ''}",
    ]
    if analysis.git.get("branch"):
        lines.append(f"- Current branch: `{analysis.git['branch']}`")
    if analysis.git.get("latest_commit"):
        lines.append(f"- Latest commit: `{analysis.git['latest_commit']}`")
    if analysis.git.get("remote"):
        lines.append(f"- Origin remote: `{analysis.git['remote']}`")
    if analysis.package_managers:
        lines.append(f"- Package managers / build systems: {', '.join(analysis.package_managers)}")
    return "\n".join(lines)


def _language_table(analysis: RepoAnalysis) -> str:
    if not analysis.languages:
        return "No common source file extensions were detected."
    lines = ["| Language | Files | Lines |", "|---|---:|---:|"]
    for item in analysis.languages[:12]:
        lines.append(f"| {item['language']} | {item['files']} | {item['lines']} |")
    return "\n".join(lines)


def _repo_shape(analysis: RepoAnalysis) -> str:
    lines = []
    if analysis.top_level_dirs:
        lines.append("Top-level directories:")
        lines.extend(f"- `{name}/`" for name in analysis.top_level_dirs)
    if analysis.key_files:
        lines.append("")
        lines.append("Key files:")
        for category, paths in analysis.key_files.items():
            joined = ", ".join(f"`{path}`" for path in paths[:10])
            lines.append(f"- {category}: {joined}")
    if analysis.dependencies:
        lines.append("")
        lines.append("Dependency manifests:")
        for source, deps in analysis.dependencies.items():
            preview = ", ".join(deps[:12]) if deps else "none listed"
            if len(deps) > 12:
                preview += f", ... ({len(deps)} total)"
            lines.append(f"- `{source}`: {preview}")
    return "\n".join(lines) if lines else "No strong repository structure signals were detected."


def _commands(analysis: RepoAnalysis) -> str:
    if not analysis.commands:
        return "No package scripts or Makefile targets were detected. Ask the maintainer for install, test, and run commands."
    lines = ["| Name | Command | Source | Details |", "|---|---|---|---|"]
    for command in analysis.commands[:20]:
        details = command["details"].replace("|", "\\|")
        lines.append(f"| {command['name']} | `{command['command']}` | `{command['source']}` | `{details}` |")
    return "\n".join(lines)


def _ops(analysis: RepoAnalysis) -> str:
    lines = []
    if analysis.test_signals:
        lines.append("Test files detected:")
        lines.extend(f"- `{path}`" for path in analysis.test_signals[:12])
    else:
        lines.append("- No obvious test files detected.")

    if analysis.ci_signals:
        lines.append("")
        lines.append("CI workflows:")
        lines.extend(f"- `{path}`" for path in analysis.ci_signals)
    else:
        lines.append("- No GitHub Actions workflows detected.")

    if analysis.env_signals:
        lines.append("")
        lines.append("Environment examples:")
        lines.extend(f"- `{path}`" for path in analysis.env_signals)
    return "\n".join(lines)


def _risks(analysis: RepoAnalysis) -> str:
    lines = [f"- {risk}" for risk in analysis.risks] or ["- No major setup risks detected from static scan."]
    if analysis.todos:
        lines.append("")
        lines.append("Sample TODO/FIXME/HACK markers:")
        for todo in analysis.todos[:8]:
            lines.append(f"- `{todo['path']}:{todo['line']}` - {todo['text']}")
    return "\n".join(lines)


def _next_steps(analysis: RepoAnalysis) -> str:
    steps = [
        "Confirm the intended local setup command with the maintainer.",
        "Run the highest-confidence test command and record the result.",
        "Identify the main entrypoint and one safe starter issue for a new contributor.",
    ]
    if not analysis.env_signals:
        steps.insert(1, "Create or request an `.env.example` with non-secret placeholder values.")
    if not analysis.ci_signals:
        steps.append("Add a minimal CI workflow once the test command is confirmed.")
    return "\n".join(f"- {step}" for step in steps)


def _first_30_minutes(analysis: RepoAnalysis) -> str:
    docs = analysis.docs[:8]
    lines = [
        "1. Read the root README first.",
        "2. Skim the top-level directories to understand the product boundaries.",
        "3. Find the app entrypoint and the test command before editing code.",
        "4. Run the smallest available test or lint command.",
    ]
    if docs:
        lines.append("")
        lines.append("Useful docs detected:")
        lines.extend(f"- `{path}`" for path in docs)
    return "\n".join(lines)


def _local_setup(analysis: RepoAnalysis) -> str:
    lines = ["Use these steps as a starting point; confirm project-specific secrets with the maintainer."]
    if "npm" in analysis.package_managers or "pnpm" in analysis.package_managers or "yarn" in analysis.package_managers:
        installer = "pnpm install" if "pnpm" in analysis.package_managers else "yarn install" if "yarn" in analysis.package_managers else "npm install"
        lines.append(f"- Install JavaScript dependencies: `{installer}`")
    if "python/pyproject" in analysis.package_managers:
        lines.append("- Install Python package locally: `python -m pip install -e .`")
    elif "pip" in analysis.package_managers:
        lines.append("- Install Python requirements: `python -m pip install -r requirements.txt`")
    if "go" in analysis.package_managers:
        lines.append("- Download Go modules: `go mod download`")
    if analysis.env_signals:
        lines.append(f"- Copy the environment example and fill local values: `{analysis.env_signals[0]}`")
    else:
        lines.append("- Ask for required environment variables; no `.env.example` was detected.")
    return "\n".join(lines)


def _architecture_tour(analysis: RepoAnalysis) -> str:
    if not analysis.top_level_dirs:
        return "No top-level directories were detected beyond excluded build/cache folders."
    lines = ["Start with these directories:"]
    for directory in analysis.top_level_dirs[:12]:
        lines.append(f"- `{directory}/` - inspect ownership and entrypoints")
    return "\n".join(lines)


def _maintainer_questions(analysis: RepoAnalysis) -> str:
    questions = [
        "What command starts the app locally?",
        "What command is required before a PR is considered safe?",
        "Which external services are required for a full local run?",
        "Where is the product boundary between core app, workers, scripts, and infrastructure?",
    ]
    if not analysis.env_signals:
        questions.append("Can you provide a non-secret environment example file?")
    if not analysis.ci_signals:
        questions.append("Is CI intentionally absent, or should a basic workflow be added?")
    return "\n".join(f"- {question}" for question in questions)
