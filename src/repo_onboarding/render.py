from __future__ import annotations

from collections import Counter
from datetime import datetime

from repo_onboarding.scanner import RepoAnalysis


ROLE_LABELS = {
    "all": "All roles",
    "analyst": "Analyst / Analytics Consultant",
    "frontend": "Frontend Developer",
    "backend": "Backend Developer",
    "data-governance": "Data / Governance Engineer",
    "project-manager": "Project Manager / Product Owner",
}


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
        "## 4. Area Map",
        "",
        _area_map(analysis),
        "",
        "## 5. Detected Domains",
        "",
        _detected_domains_section(analysis),
        "",
        "## 6. Current Understanding",
        "",
        _current_understanding(analysis),
        "",
        "## 7. Business and Product Context",
        "",
        _business_context(analysis),
        "",
        "## 8. Business Artifacts and Operating Model",
        "",
        _business_artifacts(analysis),
        "",
        "## 9. Source-of-Truth Analysis",
        "",
        _source_of_truth_analysis(analysis),
        "",
        "## 10. Backend and Services",
        "",
        _area_section(analysis.backend_signals, analysis.entrypoints),
        "",
        "## 11. API and UI Surface",
        "",
        _surface_area(analysis),
        "",
        "## 12. Frontend-to-API Contract",
        "",
        _frontend_api_contract(analysis),
        "",
        "## 13. Frontend and User Experience",
        "",
        _frontend_experience(analysis),
        "",
        "## 14. Agent and Workflow Map",
        "",
        _workflow_map(analysis),
        "",
        "## 15. Data, Analytics, and Governance",
        "",
        _area_section(analysis.data_signals, []),
        "",
        "## 16. Likely User Journeys",
        "",
        _likely_user_journeys(analysis),
        "",
        "## 17. Inferred Commands",
        "",
        _commands(analysis),
        "",
        "## 18. Tests, CI, and Operations",
        "",
        _ops(analysis),
        "",
        "## 19. Engagement Path",
        "",
        _engagement_path(analysis),
        "",
        "## 20. Hard Questions",
        "",
        _hard_questions(analysis),
        "",
        "## 21. Risks and Open Questions",
        "",
        _risks(analysis),
        "",
        "## 22. Suggested Next Steps",
        "",
        _next_steps(analysis),
        "",
    ])


def render_onboarding(analysis: RepoAnalysis, *, role: str = "all", manual_notes: str = "") -> str:
    generated = datetime.now().strftime("%Y-%m-%d")
    role = normalize_role(role)
    return "\n".join([
        f"# Onboarding Guide - {analysis.repo_name}",
        "",
        f"Generated: {generated}",
        f"Role focus: {ROLE_LABELS[role]}",
        "",
        "## 1. Executive Orientation",
        "",
        _onboarding_orientation(analysis, role),
        "",
        "## 2. First Day Plan",
        "",
        _first_day_plan(analysis, role),
        "",
        "## 3. Local Setup and Verification",
        "",
        _local_setup(analysis),
        "",
        "## 4. Architecture Map",
        "",
        _area_map(analysis),
        "",
        "## 5. Detected Repo Domains",
        "",
        _detected_domains_section(analysis),
        "",
        "## 6. Must-Read Files",
        "",
        _must_read_files(analysis),
        "",
        "## 7. Recommended Order of Learning",
        "",
        _recommended_learning_order(analysis),
        "",
        "## 8. Role Tracks",
        "",
        _role_tracks(analysis, role),
        "",
        "## 9. Core User Journeys",
        "",
        _likely_user_journeys(analysis),
        "",
        "## 10. API, UI, and Workflow Contracts",
        "",
        _onboarding_contracts(analysis),
        "",
        "## 11. Business Source of Truth",
        "",
        _source_of_truth_analysis(analysis),
        "",
        "## 12. Common Commands",
        "",
        _commands(analysis),
        "",
        "## 13. First Contribution Paths",
        "",
        _first_contribution_paths(analysis),
        "",
        "## 14. Avoid in Week 1",
        "",
        _avoid_week_one(analysis),
        "",
        "## 15. Quality Bar",
        "",
        _quality_bar(analysis),
        "",
        "## 16. Maintainer Questions",
        "",
        _maintainer_questions(analysis),
        "",
        "## Manual Notes",
        "",
        "Notes below are preserved when rerunning with `--update`.",
        "",
        "<!-- MANUAL_NOTES:START -->",
        manual_notes.strip(),
        "<!-- MANUAL_NOTES:END -->",
        "",
    ])


def normalize_role(role: str) -> str:
    normalized = role.strip().lower().replace("_", "-")
    aliases = {
        "front-end": "frontend",
        "fronted": "frontend",
        "front": "frontend",
        "fe": "frontend",
        "back-end": "backend",
        "be": "backend",
        "data": "data-governance",
        "governance": "data-governance",
        "pm": "project-manager",
        "project": "project-manager",
        "manager": "project-manager",
    }
    normalized = aliases.get(normalized, normalized)
    if normalized not in ROLE_LABELS:
        valid = ", ".join(ROLE_LABELS)
        raise ValueError(f"Unknown onboarding role '{role}'. Use one of: {valid}.")
    return normalized


def _onboarding_orientation(analysis: RepoAnalysis, role: str) -> str:
    lines = [
        f"This repository is primarily a `{analysis.repo_name}` workspace with these strongest static signals:",
    ]
    if analysis.package_managers:
        lines.append(f"- Stack/build signals: {', '.join(analysis.package_managers)}.")
    if analysis.api_routes:
        lines.append(f"- API surface: {len(analysis.api_routes)} detected route(s), mostly under `web/api/main.py`.")
    if analysis.frontend_routes:
        concrete_routes = [route["route"] for route in analysis.frontend_routes if route["route"] != "*"]
        lines.append(f"- UI surface: {len(concrete_routes)} concrete React route(s): {', '.join(f'`{route}`' for route in concrete_routes[:8])}.")
    if analysis.workflow_summaries:
        workflows = ", ".join(f"`{item['workflow']}`" for item in analysis.workflow_summaries[:10])
        lines.append(f"- Workflow layer: {workflows}.")
    if analysis.business_artifacts:
        lines.append("- Business record: client profiles, requirements, KBs, metric YAMLs, constraints, evidence packs, and artifact indexes are first-class repo artifacts.")
    lines.append("")
    if role == "all":
        lines.append("Onboarding goal: understand one business workflow end to end, then make a small role-appropriate change with the right verification command.")
    else:
        lines.append(f"Onboarding goal for {ROLE_LABELS[role]}: follow the focused track below, trace one relevant workflow, then make one small verified contribution.")
    return "\n".join(lines)


def _first_day_plan(analysis: RepoAnalysis, role: str) -> str:
    docs = [item for item in analysis.doc_headings if item["path"] == "README.md"][:8]
    lines = [
        "1. Read the root `README.md` and the generated discovery report for this repo.",
        f"2. Use the `{ROLE_LABELS[role]}` track in Section 8; do not try to learn every folder first.",
        "3. Trace one user journey from Section 9 through UI/API/workflow/data artifacts.",
        "4. Run the smallest local verification command for your role.",
        "5. Write down the source-of-truth rule you used if business artifacts disagree.",
    ]
    if docs:
        lines.append("")
        lines.append("Root README anchors worth reading first:")
        lines.extend(f"- `README.md:{item['line']}` - {item['heading']}" for item in docs[:8])
    return "\n".join(lines)


def _role_tracks(analysis: RepoAnalysis, role: str) -> str:
    tracks = {
        "analyst": _analyst_track,
        "frontend": _frontend_track,
        "backend": _backend_track,
        "data-governance": _data_governance_track,
        "project-manager": _project_manager_track,
    }
    if role == "all":
        return "\n\n".join(renderer(analysis) for renderer in tracks.values())
    return tracks[role](analysis)


def _must_read_files(analysis: RepoAnalysis) -> str:
    files: list[str] = []
    for item in analysis.doc_headings:
        if item["path"] not in files:
            files.append(item["path"])
        if len(files) >= 3:
            break
    for domain in analysis.detected_domains:
        first = domain["first_read"]
        if first and first not in files:
            files.append(first)
        if len(files) >= 10:
            break
    for artifact in analysis.business_artifacts:
        if artifact["path"] not in files:
            files.append(artifact["path"])
        if len(files) >= 14:
            break
    if not files:
        return "- No strong must-read files were detected."
    return "\n".join(f"- `{path}`" for path in files[:14])


def _recommended_learning_order(analysis: RepoAnalysis) -> str:
    first_30 = [
        "Read the root README and this onboarding guide's executive orientation.",
        "Pick one role track and one detected repo domain.",
        "Open the first-read file for that domain.",
    ]
    first_day = [
        "Run local setup for the touched area.",
        "Trace one journey through UI/API/workflow/artifact boundaries.",
        "Identify the source-of-truth artifacts for one client or domain.",
    ]
    first_week = [
        "Make one small contribution from Section 13.",
        "Run the narrowest relevant verification command.",
        "Write down any unknown ownership, source-of-truth, or release-gate questions.",
    ]
    return "\n".join([
        "### First 30 minutes",
        *[f"- {item}" for item in first_30],
        "",
        "### First day",
        *[f"- {item}" for item in first_day],
        "",
        "### First week",
        *[f"- {item}" for item in first_week],
    ])


def _analyst_track(analysis: RepoAnalysis) -> str:
    artifacts = [item for item in analysis.business_artifacts if item["kind"] in {"client profile", "requirements", "knowledge base", "metric definition", "evidence pack", "business/data constraints"}]
    lines = ["### Analyst / Analytics Consultant", "", "Purpose: answer client questions without inventing metric logic or treating draft artifacts as verified truth."]
    lines.append("")
    lines.append("Read first:")
    for artifact in artifacts[:8]:
        lines.append(f"- `{artifact['path']}` - {artifact['kind']}")
    lines.append("")
    lines.append("Do first:")
    lines.extend([
        "- Pick one client folder and compare `profile.yaml`, requirements, metric YAML, evidence, constraints, and KB.",
        "- If values conflict, use Section 11 precedence and flag the conflict instead of smoothing it over.",
        "- Find one query or metric requirement and trace whether it has implemented semantics and evidence.",
    ])
    lines.append("")
    lines.append("Avoid: editing generated semantic YAML or evidence without noting validation status.")
    return "\n".join(lines)


def _frontend_track(analysis: RepoAnalysis) -> str:
    lines = ["### Frontend Developer", "", "Purpose: make the Studio/operator UI easier to inspect, launch, and safely edit client artifacts."]
    lines.append("")
    if analysis.frontend_routes:
        lines.append("UI routes:")
        for route in analysis.frontend_routes[:8]:
            component = f" -> `{route['element']}`" if route.get("element") else ""
            lines.append(f"- `{route['route']}`{component} from `{route['path']}:{route['line']}`")
    if analysis.frontend_api_calls:
        lines.append("")
        lines.append("Typed API client methods to understand:")
        for call in analysis.frontend_api_calls[:10]:
            lines.append(f"- `{call['name']}()` -> {call['method']} `{call['route']}`")
    lines.append("")
    lines.append("Do first:")
    lines.extend([
        "- Start at `web/frontend/src/App.tsx`, then inspect the page/component tied to your route.",
        "- Follow UI data loading through `web/frontend/src/lib/api.ts` before changing state shape.",
        "- Run frontend test/typecheck/build commands before handing off UI work.",
    ])
    lines.append("")
    lines.append("Avoid: adding UI states that hide whether an artifact is draft, generated, editable, or validation-required.")
    return "\n".join(lines)


def _backend_track(analysis: RepoAnalysis) -> str:
    lines = ["### Backend Developer", "", "Purpose: preserve the API/read-service/workflow boundary and keep artifact writes auditable."]
    if analysis.api_routes:
        lines.append("")
        lines.append("API routes to trace first:")
        for route in analysis.api_routes[:10]:
            actions = f" calls {route['actions']}" if route.get("actions") else ""
            lines.append(f"- {route['method']} `{route['route']}` -> `{route.get('handler', '')}()`{actions}")
    lines.append("")
    lines.append("Do first:")
    lines.extend([
        "- Start in `web/api/main.py` for API behavior and `apps/studio/console_backend.py` for read-service behavior.",
        "- For workflow launch/status, trace `launch_workflow()` into `web/api/jobs.py` and the matching `agents/*/workflow.py` wrapper.",
        "- Keep path traversal, edit policy, backup, and diff logging behavior intact when changing artifact writes.",
    ])
    lines.append("")
    lines.append("Avoid: duplicating repo-file parsing in the API when a canonical read-service helper already exists.")
    return "\n".join(lines)


def _data_governance_track(analysis: RepoAnalysis) -> str:
    lines = ["### Data / Governance Engineer", "", "Purpose: make generated analytics artifacts trustworthy enough for operators and client teams."]
    relevant = [signal for signal in analysis.data_signals if "semantic_layer" in signal or "constraints" in signal or "governance" in signal]
    if relevant:
        lines.append("")
        lines.append("Signals to inspect:")
        lines.extend(f"- {signal}" for signal in relevant[:10])
    if analysis.workflow_summaries:
        lines.append("")
        lines.append("Workflow wrappers:")
        for workflow in analysis.workflow_summaries[:10]:
            contracts = ", ".join(f"`{name}`" for name in workflow["contracts"])
            lines.append(f"- `{workflow['workflow']}` - {contracts}")
    lines.append("")
    lines.append("Do first:")
    lines.extend([
        "- Identify whether a metric is only requested, implemented, evidenced, or validated.",
        "- Use constraints/evidence files to distinguish reusable rules from analyst narrative.",
        "- Run the semantic-layer or pytest checks that cover the changed contract.",
    ])
    lines.append("")
    lines.append("Avoid: treating a KB sentence as authoritative when metric YAML or evidence says something different.")
    return "\n".join(lines)


def _project_manager_track(analysis: RepoAnalysis) -> str:
    lines = ["### Project Manager / Product Owner", "", "Purpose: keep the work tied to a client outcome, acceptance evidence, and an explicit source of truth."]
    lines.append("")
    lines.append("What to inspect:")
    lines.extend([
        "- Section 11 source-of-truth pressure: where client artifacts can disagree.",
        "- Section 9 core user journeys: which workflow the team is actually improving.",
        "- Section 15 quality bar: what must be true before work is considered done.",
    ])
    lines.append("")
    lines.append("Do first:")
    lines.extend([
        "- Pick the user journey and the artifact that proves it worked.",
        "- Define acceptance as a file, route, command, or validation result, not just a status update.",
        "- Ask which artifact is decision-grade and who owns corrections after generation.",
    ])
    lines.append("")
    lines.append("Avoid: planning around generic platform progress without naming the client artifact or workflow that changes.")
    return "\n".join(lines)


def _onboarding_contracts(analysis: RepoAnalysis) -> str:
    sections = []
    if analysis.frontend_api_calls:
        sections.append("Frontend API client:")
        sections.extend(f"- `{call['name']}()` -> {call['method']} `{call['route']}`" for call in analysis.frontend_api_calls[:12])
    if analysis.api_routes:
        sections.append("")
        sections.append("Backend handlers:")
        sections.extend(
            f"- {route['method']} `{route['route']}` -> `{route.get('handler', '')}()`"
            for route in analysis.api_routes[:12]
        )
    if analysis.workflow_summaries:
        sections.append("")
        sections.append("Workflow contracts:")
        sections.extend(
            f"- `{workflow['workflow']}`: {', '.join(f'`{name}`' for name in workflow['contracts'])}"
            for workflow in analysis.workflow_summaries[:10]
        )
    return "\n".join(sections) if sections else "No UI/API/workflow contracts were detected."


def _first_contribution_paths(analysis: RepoAnalysis) -> str:
    paths = [
        "Analyst: improve one KB/evidence/requirements inconsistency and document the precedence used.",
        "Frontend: improve one client detail panel or artifact reader state, then run frontend tests/typecheck.",
        "Backend: add or tighten one API response path without bypassing read-service helpers.",
        "Data/governance: add one validation fixture or constraint rule and prove it with tests.",
        "Project manager: convert one vague roadmap item into an artifact-backed acceptance checklist.",
    ]
    return "\n".join(f"- {path}" for path in paths)


def _avoid_week_one(analysis: RepoAnalysis) -> str:
    items = [
        "Do not edit generated semantic-layer artifacts unless validation expectations are explicit.",
        "Do not change artifact write behavior without preserving path traversal checks, backups, and edit logs.",
        "Do not treat analyst KB prose as authoritative when metric YAML, evidence, or constraints conflict.",
        "Do not start by refactoring shared utilities before tracing one concrete user journey.",
    ]
    if analysis.workflow_summaries:
        items.append("Do not modify workflow contracts casually; input/result classes are cross-surface integration points.")
    return "\n".join(f"- {item}" for item in items)


def _quality_bar(analysis: RepoAnalysis) -> str:
    lines = [
        "- Every change should name the role/user journey it improves.",
        "- Every business-facing claim should point to profile, requirements, metric YAML, evidence, constraints, or KB.",
        "- Generated artifacts need visible draft/validation status when shown or edited.",
        "- API changes should keep path traversal and artifact edit policy protections intact.",
        "- UI changes should preserve typed API contracts and error visibility.",
    ]
    if analysis.commands:
        lines.append("- Run the narrowest relevant command from Section 12 before opening a PR.")
    if analysis.ci_signals:
        lines.append(f"- Confirm CI coverage in `{analysis.ci_signals[0]}` for shared behavior.")
    return "\n".join(lines)


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
    if analysis.manifests:
        lines.append("")
        lines.append("Manifests and build files:")
        for manifest in analysis.manifests[:20]:
            lines.append(f"- `{manifest['path']}` - {manifest['kind']}")
    if analysis.dependencies:
        lines.append("")
        lines.append("Dependency manifests:")
        for source, deps in analysis.dependencies.items():
            preview = ", ".join(deps[:12]) if deps else "none listed"
            if len(deps) > 12:
                preview += f", ... ({len(deps)} total)"
            lines.append(f"- `{source}`: {preview}")
    return "\n".join(lines) if lines else "No strong repository structure signals were detected."


def _area_map(analysis: RepoAnalysis) -> str:
    if not analysis.directory_profiles:
        return "No directory profile could be built."
    lines = ["| Area | Files | Likely purpose | Languages | Notable files |", "|---|---:|---|---|---|"]
    for item in analysis.directory_profiles[:18]:
        languages = ", ".join(item["languages"]) if item["languages"] else ""
        notable = ", ".join(f"`{path}`" for path in item["notable_files"][:3])
        lines.append(f"| `{item['name']}/` | {item['files']} | {item['purpose']} | {languages} | {notable} |")
    return "\n".join(lines)


def _detected_domains_section(analysis: RepoAnalysis) -> str:
    if not analysis.detected_domains:
        return "No strong vertical repo domains were detected."
    lines = ["| Domain slug | Status | Why this is a separate slice | First read | Evidence |", "|---|---|---|---|---|"]
    for domain in analysis.detected_domains:
        lines.append(
            f"| `{domain['slug']}` | {domain['status']} | {domain['why']} | `{domain['first_read']}` | {domain['evidence']} |"
        )
    return "\n".join(lines)


def _current_understanding(analysis: RepoAnalysis) -> str:
    lines = ["### Product / Business", ""]
    if analysis.business_artifacts:
        lines.append("- Confirmed: client-specific profiles, requirements, KBs, evidence, constraints, and artifact indexes are stored in-repo.")
    else:
        lines.append("- Unknown: no strong in-repo business artifacts were detected.")
    if analysis.doc_headings:
        first = analysis.doc_headings[0]
        lines.append(f"- Confirmed: root documentation starts at `{first['path']}:{first['line']}` with `{first['heading']}`.")
    lines.append("- Unknown: exact production owner and release gate still need maintainer confirmation.")
    lines.append("")
    lines.append("### Repository Shape")
    if analysis.detected_domains:
        domains = ", ".join(f"`{domain['slug']}`" for domain in analysis.detected_domains[:8])
        lines.append(f"- Confirmed: meaningful repo slices include {domains}.")
    if analysis.api_routes and analysis.frontend_routes:
        lines.append("- Confirmed: this repo exposes both a backend API and a frontend UI surface.")
    if analysis.workflow_summaries:
        lines.append("- Confirmed: agent workflows use explicit input/result contract wrappers.")
    lines.append("- Likely: safest onboarding path is to follow one client artifact journey instead of reading the repo alphabetically.")
    return "\n".join(lines)


def _business_context(analysis: RepoAnalysis) -> str:
    lines = []
    if analysis.client_domains:
        preview = ", ".join(f"`{name}`" for name in analysis.client_domains[:20])
        lines.append(f"Client/domain folders detected: {preview}")
    if analysis.doc_headings:
        lines.append("")
        lines.append("Documentation map:")
        for item in analysis.doc_headings[:12]:
            lines.append(f"- `{item['path']}:{item['line']}` - {item['heading']}")
    if analysis.business_signals:
        lines.append("")
        lines.append("Business usage signals:")
        lines.extend(f"- {signal}" for signal in analysis.business_signals[:12])
    if not lines:
        return "No strong business-domain signals were detected from static paths/docs."
    return "\n".join(lines)


def _business_artifacts(analysis: RepoAnalysis) -> str:
    if not analysis.business_artifacts:
        return "No client, stakeholder, metric, evidence, or requirements artifacts were detected."
    lines = ["| Artifact | Kind | Extracted title/context |", "|---|---|---|"]
    for artifact in analysis.business_artifacts[:20]:
        title = artifact["title"].replace("|", "\\|") if artifact["title"] else ""
        lines.append(f"| `{artifact['path']}` | {artifact['kind']} | {title} |")
    return "\n".join(lines)


def _source_of_truth_analysis(analysis: RepoAnalysis) -> str:
    if not analysis.business_artifacts:
        return "No client artifacts were detected, so source-of-truth precedence cannot be inferred."
    by_client: dict[str, list[str]] = {}
    for artifact in analysis.business_artifacts:
        parts = artifact["path"].split("/")
        client = parts[1] if len(parts) > 1 and parts[0] == "clients" else "platform"
        by_client.setdefault(client, []).append(artifact["kind"])

    lines = ["| Scope | Artifact kinds present | Likely source-of-truth pressure |", "|---|---|---|"]
    for client, kinds in sorted(by_client.items())[:12]:
        counts = Counter(kinds)
        present = ", ".join(f"{kind} ({count})" for kind, count in counts.most_common())
        pressure = _source_truth_pressure(counts)
        lines.append(f"| `{client}` | {present} | {pressure} |")
    lines.append("")
    lines.append("Recommended precedence when facts conflict: `profile.yaml` for client identity and stack, requirements for intended metrics, metric YAML for implemented semantics, evidence pack for verified values, constraints for reusable filters, KB for analyst-facing interpretation.")
    return "\n".join(lines)


def _source_truth_pressure(counts: Counter[str]) -> str:
    if counts.get("client profile") and counts.get("requirements") and counts.get("metric definition") and counts.get("evidence pack"):
        return "High: intent, implementation, and verification all exist; conflicts need explicit precedence."
    if counts.get("client profile") and counts.get("knowledge base"):
        return "Medium: profile and narrative exist; verify metrics/evidence before treating as decision-grade."
    if counts.get("requirements") and not counts.get("metric definition"):
        return "Backlog risk: requirements exist without obvious implemented metric YAML."
    return "Low/unknown from static artifact inventory."


def _area_section(signals: list[str], entrypoints: list[str]) -> str:
    lines = []
    if entrypoints:
        lines.append("Likely entrypoints:")
        lines.extend(f"- `{entry}`" if not entry.startswith("`") else f"- {entry}" for entry in entrypoints[:12])
    if signals:
        if lines:
            lines.append("")
        lines.append("Signals:")
        lines.extend(f"- {signal}" for signal in signals[:14])
    return "\n".join(lines) if lines else "No strong signals detected in this area."


def _surface_area(analysis: RepoAnalysis) -> str:
    lines = []
    if analysis.api_routes:
        lines.append("Detected API routes:")
        lines.append("| Method | Route | Source |")
        lines.append("|---|---|---|")
        for route in analysis.api_routes[:20]:
            handler = f" -> `{route['handler']}()`" if route.get("handler") else ""
            actions = f"; calls: {route['actions']}" if route.get("actions") else ""
            lines.append(f"| {route['method']} | `{route['route']}` | `{route['path']}:{route['line']}`{handler}{actions} |")
    else:
        lines.append("Detected API routes: none from static FastAPI/router scan.")
    if analysis.frontend_routes:
        lines.append("")
        lines.append("Detected frontend routes:")
        lines.append("| Route | UI component | Source |")
        lines.append("|---|---|---|")
        for route in analysis.frontend_routes[:20]:
            element = f"`{route['element']}`" if route.get("element") else ""
            lines.append(f"| `{route['route']}` | {element} | `{route['path']}:{route['line']}` |")
    else:
        lines.append("")
        lines.append("Detected frontend routes: none from static React route scan.")
    return "\n".join(lines)


def _frontend_api_contract(analysis: RepoAnalysis) -> str:
    if not analysis.frontend_api_calls:
        return "No typed frontend API client calls were detected."
    lines = ["| Client method | HTTP | API path/template | Source |", "|---|---|---|---|"]
    for call in analysis.frontend_api_calls[:24]:
        lines.append(f"| `{call['name']}` | {call['method']} | `{call['route']}` | `{call['path']}:{call['line']}` |")
    return "\n".join(lines)


def _frontend_experience(analysis: RepoAnalysis) -> str:
    lines = []
    if analysis.frontend_routes:
        concrete = [route for route in analysis.frontend_routes if route["route"] != "*"]
        lines.append(f"Primary UI appears to expose {len(concrete)} concrete route(s): " + ", ".join(f"`{route['route']}`" for route in concrete[:6]) + ".")
    if analysis.frontend_signals:
        lines.append("")
        lines.append("Signals:")
        lines.extend(f"- {signal}" for signal in analysis.frontend_signals[:14])
    if not lines:
        return "No strong frontend signals detected."
    return "\n".join(lines)


def _workflow_map(analysis: RepoAnalysis) -> str:
    if not analysis.workflow_summaries:
        return "No `agents/*/workflow.py` modules were detected."
    lines = ["| Workflow | Contract classes | Public functions | Summary |", "|---|---|---|---|"]
    for workflow in analysis.workflow_summaries[:16]:
        contracts = ", ".join(f"`{name}`" for name in workflow["contracts"]) or ""
        functions = ", ".join(f"`{name}()`" for name in workflow["functions"]) or ""
        summary = workflow["doc"].replace("|", "\\|")
        if not summary and workflow["imports"]:
            summary = "Uses " + ", ".join(f"`{name}`" for name in workflow["imports"][:3])
        lines.append(f"| `{workflow['workflow']}` | {contracts} | {functions} | {summary} |")
    return "\n".join(lines)


def _likely_user_journeys(analysis: RepoAnalysis) -> str:
    journeys = []
    routes = {route["route"] for route in analysis.api_routes}
    ui_routes = {route["route"] for route in analysis.frontend_routes}
    api_methods = {call["name"] for call in analysis.frontend_api_calls}
    if "/clients" in ui_routes and "/api/clients" in routes:
        journeys.append("Client overview: React `/clients` route reads `/api/clients`, then drills into `/clients/:slug` and `/api/clients/{slug}`.")
    if any("/artifacts" in route for route in routes):
        journeys.append("Artifact review/edit loop: client detail UI can list artifacts, read semantic-layer files, and write artifact file edits through the API.")
    if any("/workflows/" in route for route in routes):
        journeys.append("Workflow launch loop: client route can approve stages, launch named workflows, and poll workflow status.")
    if {"knowledgeSearch", "artifactContent", "updateArtifactFile"} & api_methods:
        journeys.append("Knowledge workspace loop: typed frontend API methods support search, artifact reading, and edited artifact persistence.")
    if analysis.business_artifacts:
        journeys.append("Business context loop: profiles, requirements, KBs, evidence packs, constraints, and artifact indexes form the operating record for each client.")
    if analysis.data_signals:
        journeys.append("Governance loop: semantic-layer assets and constraints are checked by governance/validation code before artifacts should be treated as decision-grade.")
    if not journeys:
        return "No end-to-end journeys could be inferred from static route/artifact signals."
    return "\n".join(f"- {journey}" for journey in journeys)


def _engagement_path(analysis: RepoAnalysis) -> str:
    steps = [
        "Start with the business record: read the relevant `clients/{slug}/profile.yaml`, requirements, KB, evidence pack, and artifact index together.",
        "Open the UI path next: use frontend routes to identify what an operator can actually inspect or launch.",
        "Trace one API call from the UI into `web/api/main.py`, then into the tool/agent/pipeline that produces the artifact.",
        "Run the smallest local checks that cover the touched area before trusting generated output.",
        "Write down which artifact wins when profile, requirements, KB, evidence, and constraints disagree.",
    ]
    if analysis.commands:
        command_names = ", ".join(f"`{command['command']}`" for command in analysis.commands[:4])
        steps.append(f"Candidate commands to validate first: {command_names}.")
    return "\n".join(f"{index}. {step}" for index, step in enumerate(steps, start=1))


def _hard_questions(analysis: RepoAnalysis) -> str:
    questions = [
        "What painful business workflow does this repo make dramatically faster, and where is that proven in client artifacts?",
        "Which single user path matters most: backend automation, Studio UI, analyst KB generation, semantic-layer validation, or something else?",
        "What would break trust fastest for a client: wrong metric logic, stale evidence, bad UI state, slow agent output, or warehouse access failure?",
        "Which generated artifacts are decision-grade, and which are still drafts that need human review?",
        "What is the shortest demo path from raw client context to a useful business outcome?",
    ]
    if not analysis.api_routes:
        questions.append("If the app has a service layer, why are API routes not obvious from static scan?")
    if not analysis.frontend_routes and analysis.frontend_signals:
        questions.append("Is the frontend a true routed app or a single workspace surface, and does that match how users work?")
    if analysis.business_artifacts:
        questions.append("Which client artifact is the source of truth when profile, KB, requirements, and evidence disagree?")
    if analysis.commands:
        questions.append("Which detected command is the actual release gate, not just a local convenience command?")
    return "\n".join(f"- {question}" for question in questions)


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
        "Run the most relevant detected setup/test commands and record exact pass/fail output.",
        "Confirm which backend service, frontend app, and business workflow are the primary contributor path.",
        "Map one end-to-end flow from UI/API entrypoint to data/business artifact.",
        "Choose one business artifact as the source of truth and document conflict-resolution rules.",
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
    package_json_paths = [manifest["path"] for manifest in analysis.manifests if manifest["path"].endswith("package.json")]
    for package_path in package_json_paths[:4]:
        parent = package_path.rsplit("/", 1)[0] if "/" in package_path else ""
        installer = "npm install"
        if "pnpm" in analysis.package_managers:
            installer = "pnpm install"
        elif "yarn" in analysis.package_managers:
            installer = "yarn install"
        command = f"cd {parent} && {installer}" if parent else installer
        lines.append(f"- Install JavaScript dependencies: `{command}`")
    if "python/pyproject" in analysis.package_managers:
        lines.append("- Install Python package locally: `python -m pip install -e .`")
    requirement_paths = [manifest["path"] for manifest in analysis.manifests if manifest["path"].endswith("requirements.txt")]
    for req_path in requirement_paths[:4]:
        lines.append(f"- Install Python requirements: `python -m pip install -r {req_path}`")
    if "go" in analysis.package_managers:
        lines.append("- Download Go modules: `go mod download`")
    if analysis.env_signals:
        lines.append(f"- Copy the environment example and fill local values: `{analysis.env_signals[0]}`")
    else:
        lines.append("- Ask for required environment variables; no `.env.example` was detected.")
    if analysis.commands:
        lines.append("")
        lines.append("Verification candidates:")
        for command in analysis.commands[:8]:
            lines.append(f"- `{command['command']}` ({command['source']})")
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
