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
    assert any(manifest["path"] == "package.json" for manifest in analysis.manifests)
    assert any(profile["name"] == "src" for profile in analysis.directory_profiles)
    assert analysis.entrypoints == ["src/app.py"]
    assert analysis.frontend_signals
    assert analysis.doc_headings
    assert analysis.test_signals
    assert analysis.ci_signals
    assert analysis.env_signals == [".env.example"]


def test_renderers_include_expected_sections(tmp_path: Path) -> None:
    analysis = analyze_repo(_sample_repo(tmp_path))

    discovery = render_discovery(analysis)
    onboarding = render_onboarding(analysis)

    assert "# Repository Discovery Report - startup-app" in discovery
    assert "## 4. Area Map" in discovery
    assert "## 5. Detected Domains" in discovery
    assert "## 6. Current Understanding" in discovery
    assert "## 9. Source-of-Truth Analysis" in discovery
    assert "## 10. Backend and Services" in discovery
    assert "## 11. API and UI Surface" in discovery
    assert "## 12. Frontend-to-API Contract" in discovery
    assert "## 14. Agent and Workflow Map" in discovery
    assert "## 19. Engagement Path" in discovery
    assert "## 20. Hard Questions" in discovery
    assert "## 21. Risks and Open Questions" in discovery
    assert "# Onboarding Guide - startup-app" in onboarding
    assert "## 5. Detected Repo Domains" in onboarding
    assert "## 6. Must-Read Files" in onboarding
    assert "## 7. Recommended Order of Learning" in onboarding
    assert "## 8. Role Tracks" in onboarding
    assert "### Analyst / Analytics Consultant" in onboarding
    assert "### Frontend Developer" in onboarding
    assert "### Backend Developer" in onboarding
    assert "### Project Manager / Product Owner" in onboarding

    focused = render_onboarding(analysis, role="frontend")
    assert "Role focus: Frontend Developer" in focused
    assert "### Frontend Developer" in focused
    assert "### Backend Developer" not in focused


def test_cli_writes_requested_files(tmp_path: Path) -> None:
    repo = _sample_repo(tmp_path)
    out = tmp_path / "out"

    code = main(["all", "--repo", str(repo), "--out", str(out)])

    assert code == 0
    assert (out / "discovery.md").exists()
    assert (out / "onboarding.md").exists()


def test_cli_writes_focused_onboarding_and_preserves_notes(tmp_path: Path) -> None:
    repo = _sample_repo(tmp_path)
    out = tmp_path / "out"
    out.mkdir()
    focused_path = out / "onboarding_frontend.md"
    focused_path.write_text(
        "\n".join([
            "# Old",
            "<!-- MANUAL_NOTES:START -->",
            "Keep this note.",
            "<!-- MANUAL_NOTES:END -->",
        ]),
        encoding="utf-8",
    )

    code = main(["onboarding", "--repo", str(repo), "--out", str(out), "--role", "frontend", "--update"])

    assert code == 0
    text = focused_path.read_text(encoding="utf-8")
    assert "Role focus: Frontend Developer" in text
    assert "### Frontend Developer" in text
    assert "### Backend Developer" not in text
    assert "Keep this note." in text
