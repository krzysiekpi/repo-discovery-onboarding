from __future__ import annotations

import json
import subprocess
from pathlib import Path

from repo_onboarding.cli import main
from repo_onboarding.render import render_discovery, render_onboarding
from repo_onboarding.scanner import analyze_repo


def _sample_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "startup-app"
    repo.mkdir()
    (repo / "src").mkdir()
    (repo / "tests").mkdir()
    (repo / ".github" / "workflows").mkdir(parents=True)
    (repo / "README.md").write_text("# Startup App\n\nLocal app docs.\n", encoding="utf-8")
    (repo / ".env.example").write_text("API_KEY=\n", encoding="utf-8")
    (repo / "package.json").write_text(
        json.dumps({
            "scripts": {"dev": "vite", "test": "vitest run"},
            "dependencies": {"react": "^19.0.0"},
            "devDependencies": {"vitest": "^3.0.0"},
        }),
        encoding="utf-8",
    )
    (repo / "pyproject.toml").write_text(
        "[project]\nname = 'startup-app'\ndependencies = ['fastapi']\n",
        encoding="utf-8",
    )
    (repo / "src" / "app.py").write_text("def main():\n    return 'ok'\n", encoding="utf-8")
    (repo / "tests" / "test_app.py").write_text("def test_ok():\n    assert True\n", encoding="utf-8")
    (repo / ".github" / "workflows" / "ci.yml").write_text("name: ci\n", encoding="utf-8")
    subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True)
    return repo


def test_analyze_repo_detects_core_signals(tmp_path: Path) -> None:
    repo = _sample_repo(tmp_path)

    analysis = analyze_repo(repo)

    assert analysis.repo_name == "startup-app"
    assert "npm" in analysis.package_managers
    assert "python/pyproject" in analysis.package_managers
    assert any(item["language"] == "Python" for item in analysis.languages)
    assert any(command["command"] == "npm run test" for command in analysis.commands)
    assert analysis.test_signals
    assert analysis.ci_signals
    assert analysis.env_signals == [".env.example"]


def test_renderers_include_expected_sections(tmp_path: Path) -> None:
    analysis = analyze_repo(_sample_repo(tmp_path))

    discovery = render_discovery(analysis)
    onboarding = render_onboarding(analysis)

    assert "# Repository Discovery Report - startup-app" in discovery
    assert "## 6. Risks and Open Questions" in discovery
    assert "# Developer Onboarding Guide - startup-app" in onboarding
    assert "## 2. Local Setup" in onboarding


def test_cli_writes_requested_files(tmp_path: Path) -> None:
    repo = _sample_repo(tmp_path)
    out = tmp_path / "out"

    code = main(["all", "--repo", str(repo), "--out", str(out)])

    assert code == 0
    assert (out / "discovery.md").exists()
    assert (out / "onboarding.md").exists()
