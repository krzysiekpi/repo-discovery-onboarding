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
        "## 1. Executive Summary",
        "",
        _executive_summary(analysis),
        "",
        "## 2. Discovery Confidence",
        "",
        _discovery_confidence(analysis),
        "",
        "## 3. Snapshot",
        "",
        _snapshot(analysis),
        "",
        "## 4. Product and Documentation Context",
        "",
        _business_context(analysis),
        "",
        "## 5. Technology Signals",
        "",
        _language_table(analysis),
        "",
        "## 6. Repository Shape",
        "",
        _repo_shape(analysis),
        "",
        "## 7. Area Map",
        "",
        _area_map(analysis),
        "",
        "## 8. Detected Domains",
        "",
        _detected_domains_section(analysis),
        "",
        "## 9. Current Understanding",
        "",
        _current_understanding(analysis),
        "",
        "## 10. Domain Artifacts and Operating Model",
        "",
        _business_artifacts(analysis),
        "",
        "## 11. Source-of-Truth Analysis",
        "",
        _source_of_truth_analysis(analysis),
        "",
        "## 12. Backend and Services",
        "",
        _area_section(analysis.backend_signals, analysis.entrypoints),
        "",
        "## 13. API and UI Surface",
        "",
        _surface_area(analysis),
        "",
        "## 14. Frontend-to-API Contract",
        "",
        _frontend_api_contract(analysis),
        "",
        "## 15. Frontend and User Experience",
        "",
        _frontend_experience(analysis),
        "",
        "## 16. Automation and Workflow Map",
        "",
        _workflow_map(analysis),
        "",
        "## 17. Data, Domain Model, and Governance",
        "",
        _area_section(analysis.data_signals, []),
        "",
        "## 18. Likely User Journeys",
        "",
        _likely_user_journeys(analysis),
        "",
        "## 19. Inferred Commands",
        "",
        _commands(analysis),
        "",
        "## 20. Tests, CI, and Operations",
        "",
        _ops(analysis),
        "",
        "## 21. Recommended Validation Path",
        "",
        _validation_path(analysis),
        "",
        "## 22. Hard Questions",
        "",
        _hard_questions(analysis),
        "",
        "## 23. Risks and Open Questions",
        "",
        _risks(analysis),
        "",
        "## 24. Suggested Next Steps",
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
        api_paths = sorted({route["path"] for route in analysis.api_routes})
        primary = api_paths[0] if api_paths else "backend route files"
        lines.append(f"- API surface: {len(analysis.api_routes)} detected route(s), starting in `{primary}`.")
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
    lines.append("Avoid: changing domain logic without checking the matching tests, docs, and persisted model/schema.")
    return "\n".join(lines)


def _frontend_track(analysis: RepoAnalysis) -> str:
    lines = ["### Frontend Developer", "", "Purpose: make the user-facing UI easier to inspect, navigate, and verify."]
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
    lines.append("Avoid: adding UI states that hide loading, error, auth, or persistence status.")
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
        "- Start with the route files listed in Section 10 for API behavior.",
        "- Trace handlers into services, models, persistence, and external integrations before changing response shape.",
        "- Keep authentication, authorization, validation, and error behavior intact when changing writes.",
    ])
    lines.append("")
    lines.append("Avoid: duplicating business logic in route handlers when a service/model layer already owns it.")
    return "\n".join(lines)


def _data_governance_track(analysis: RepoAnalysis) -> str:
    lines = ["### Data / Governance Engineer", "", "Purpose: make persisted data, schemas, domain rules, and generated outputs trustworthy."]
    relevant = [signal for signal in analysis.data_signals if "semantic_layer" in signal or "constraints" in signal or "governance" in signal or "alembic" in signal or "migration" in signal]
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
        "- Run the migration, schema, backend, or pytest checks that cover the changed contract.",
    ])
    lines.append("")
    lines.append("Avoid: treating prose docs as authoritative when schema/model/test behavior says something different.")
    return "\n".join(lines)


def _project_manager_track(analysis: RepoAnalysis) -> str:
    lines = ["### Project Manager / Product Owner", "", "Purpose: keep the work tied to a client outcome, acceptance evidence, and an explicit source of truth."]
    lines.append("")
    lines.append("What to inspect:")
    lines.extend([
        "- Section 11 source-of-truth pressure: where docs, API code, models, and tests can disagree.",
        "- Section 9 core user journeys: which workflow the team is actually improving.",
        "- Section 15 quality bar: what must be true before work is considered done.",
    ])
    lines.append("")
    lines.append("Do first:")
    lines.extend([
        "- Pick the user journey and the artifact that proves it worked.",
        "- Define acceptance as a file, route, command, or validation result, not just a status update.",
        "- Ask which source is decision-grade and who owns corrections after behavior changes.",
    ])
    lines.append("")
    lines.append("Avoid: planning around generic repo progress without naming the user journey or product behavior that changes.")
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
        "Product/domain: improve one docs/requirements inconsistency and document the precedence used.",
        "Frontend: improve one route/page state, then run frontend tests/typecheck.",
        "Backend: add or tighten one API response path without bypassing existing service helpers.",
        "Data/governance: add one validation fixture or constraint rule and prove it with tests.",
        "Project manager: convert one vague roadmap item into an artifact-backed acceptance checklist.",
    ]
    return "\n".join(f"- {path}" for path in paths)


def _avoid_week_one(analysis: RepoAnalysis) -> str:
    items = [
        "Do not edit generated or persisted domain artifacts unless validation expectations are explicit.",
        "Do not change artifact write behavior without preserving path traversal checks, backups, and edit logs.",
        "Do not treat prose docs as authoritative when code, schemas, tests, or migrations conflict.",
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


def _executive_summary(analysis: RepoAnalysis) -> str:
    lines = []
    if analysis.readme_summary:
        lines.append("Product/context from README:")
        lines.extend(f"- {item}" for item in analysis.readme_summary[:4])
        lines.append("")

    stack = ", ".join(item["language"] for item in analysis.languages[:4]) or "unknown"
    areas = ", ".join(f"`{profile['name']}/`" for profile in analysis.directory_profiles[:6]) or "not enough directory signal"
    lines.extend([
        f"- Primary stack signals: {stack}.",
        f"- Main repo areas: {areas}.",
    ])
    if analysis.api_routes:
        lines.append(f"- Backend/API surface: {len(analysis.api_routes)} route(s) detected.")
    if analysis.frontend_routes:
        concrete = [route for route in analysis.frontend_routes if route["route"] != "*"]
        lines.append(f"- Frontend surface: {len(concrete)} concrete route(s) detected.")
    if analysis.commands:
        command_preview = ", ".join(f"`{command['command']}`" for command in analysis.commands[:4])
        lines.append(f"- Verification candidates: {command_preview}.")
    if analysis.risks:
        lines.append(f"- Main risk to confirm: {analysis.risks[0]}")
    return "\n".join(lines)


def _discovery_confidence(analysis: RepoAnalysis) -> str:
    score = 0
    evidence = []
    gaps = []
    checks = [
        (bool(analysis.readme_summary or analysis.doc_headings), 15, "README/docs parsed", "README/docs context is thin"),
        (bool(analysis.languages), 10, "language mix detected", "language mix unavailable"),
        (bool(analysis.manifests), 15, "package/build manifests detected", "no package/build manifests detected"),
        (bool(analysis.commands), 15, "runnable commands inferred", "no commands inferred"),
        (bool(analysis.test_signals), 10, "tests detected", "no test files detected"),
        (bool(analysis.ci_signals), 10, "CI detected", "no CI detected"),
        (bool(analysis.api_routes or analysis.entrypoints), 10, "backend entrypoints/routes detected", "backend entrypoints unclear"),
        (bool(analysis.frontend_routes or analysis.frontend_signals), 10, "frontend surface detected", "frontend surface unclear"),
        (bool(analysis.env_signals), 5, "environment example detected", "no env example detected"),
    ]
    for passed, points, good, gap in checks:
        if passed:
            score += points
            evidence.append(good)
        else:
            gaps.append(gap)

    rating = "High" if score >= 80 else "Medium" if score >= 55 else "Low"
    lines = [
        f"- Score: {score}/100 ({rating})",
        f"- Evidence: {', '.join(evidence[:8])}.",
    ]
    if gaps:
        lines.append(f"- Remaining uncertainty: {', '.join(gaps[:5])}.")
    else:
        lines.append("- Remaining uncertainty: low from static scan; still confirm real setup commands with the maintainer.")
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
    if analysis.readme_summary:
        for item in analysis.readme_summary[:3]:
            lines.append(f"- Confirmed from README: {item}")
    elif analysis.business_artifacts:
        lines.append("- Confirmed: domain-specific docs or artifacts are stored in-repo.")
    else:
        lines.append("- Unknown: no strong product/domain context was detected.")
    if analysis.doc_headings:
        first = analysis.doc_headings[0]
        lines.append(f"- Confirmed: root documentation starts at `{first['path']}:{first['line']}` with `{first['heading']}`.")
    lines.append("- Unknown: exact production owner, deployment target, and release gate still need maintainer confirmation.")
    lines.append("")
    lines.append("### Repository Shape")
    if analysis.detected_domains:
        domains = ", ".join(f"`{domain['slug']}`" for domain in analysis.detected_domains[:8])
        lines.append(f"- Confirmed: meaningful repo slices include {domains}.")
    if analysis.api_routes and analysis.frontend_routes:
        lines.append("- Confirmed: this repo exposes both a backend API and a frontend UI surface.")
    if analysis.workflow_summaries:
        lines.append("- Confirmed: automation workflows or typed workflow wrappers are present.")
    lines.append("- Likely: safest onboarding path is to trace one user journey across frontend, API, backend, and persistence before changing code.")
    return "\n".join(lines)


def _business_context(analysis: RepoAnalysis) -> str:
    lines = []
    if analysis.readme_summary:
        lines.append("README summary:")
        lines.extend(f"- {item}" for item in analysis.readme_summary[:5])
    if analysis.client_domains:
        if lines:
            lines.append("")
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
        return "No domain-specific profile, stakeholder, requirements, metric, evidence, or operating artifacts were detected."
    lines = ["| Artifact | Kind | Extracted title/context |", "|---|---|---|"]
    for artifact in analysis.business_artifacts[:20]:
        title = artifact["title"].replace("|", "\\|") if artifact["title"] else ""
        lines.append(f"| `{artifact['path']}` | {artifact['kind']} | {title} |")
    return "\n".join(lines)


def _source_of_truth_analysis(analysis: RepoAnalysis) -> str:
    if not analysis.business_artifacts:
        return "No domain-specific artifacts were detected, so source-of-truth precedence cannot be inferred. For this repo, start with README/product docs, then package manifests, then app routes/API handlers."
    by_scope: dict[str, list[str]] = {}
    for artifact in analysis.business_artifacts:
        parts = artifact["path"].split("/")
        scope = parts[1] if len(parts) > 1 and parts[0] == "clients" else parts[0]
        by_scope.setdefault(scope, []).append(artifact["kind"])

    lines = ["| Scope | Artifact kinds present | Likely source-of-truth pressure |", "|---|---|---|"]
    for scope, kinds in sorted(by_scope.items())[:12]:
        counts = Counter(kinds)
        present = ", ".join(f"{kind} ({count})" for kind, count in counts.most_common())
        pressure = _source_truth_pressure(counts)
        lines.append(f"| `{scope}` | {present} | {pressure} |")
    lines.append("")
    lines.append("Recommended precedence when facts conflict: product/requirements docs for intent, API and route code for actual behavior, schemas/models/migrations for persisted state, tests/CI for verified behavior, README/setup docs for local operation.")
    return "\n".join(lines)


def _source_truth_pressure(counts: Counter[str]) -> str:
    if counts.get("product requirements"):
        return "Medium: product intent exists; verify implementation against routes, models, and tests."
    if counts.get("client profile") and counts.get("requirements") and counts.get("metric definition") and counts.get("evidence pack"):
        return "High: intent, implementation, and verification all exist; conflicts need explicit precedence."
    if counts.get("client profile") and counts.get("knowledge base"):
        return "Medium: profile and narrative exist; verify metrics/evidence before treating as decision-grade."
    if counts.get("requirements") and not counts.get("metric definition"):
        return "Backlog risk: requirements exist without obvious implementation artifact."
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
    route_text = " ".join(sorted(routes | ui_routes)).lower()
    route_pairs = sorted(routes | ui_routes)

    if any("auth" in route or "login" in route for route in route_pairs):
        journeys.append("Authentication flow: login/auth routes suggest the first critical journey is sign-in, token/session handling, and post-login routing.")
    if any("onboarding" in route for route in route_pairs):
        journeys.append("User onboarding flow: onboarding routes suggest a guided first-use path before the main product dashboard.")
    if any("dashboard" in route for route in route_pairs):
        journeys.append("Core product dashboard flow: dashboard routes likely represent the main authenticated user workspace.")
    if any("profile" in route for route in route_pairs):
        journeys.append("Profile management flow: profile routes suggest user setup, preferences, or saved entities are central product state.")
    if any(route.startswith("/admin") or "/users" in route for route in route_pairs):
        journeys.append("Admin operations flow: admin/user routes suggest maintainer workflows for user management, activation, blocking, merge, and configuration.")
    if any("history" in route or "response" in route for route in route_pairs):
        journeys.append("Result/history flow: response/history routes suggest users generate or inspect prior outputs over time.")

    if "/clients" in ui_routes and "/api/clients" in routes:
        journeys.append("Client overview: React `/clients` route reads `/api/clients`, then drills into `/clients/:slug` and `/api/clients/{slug}`.")
    if any("/artifacts" in route for route in routes):
        journeys.append("Artifact review/edit loop: UI/API routes can list, read, or persist generated files or domain artifacts.")
    if any("/workflows/" in route for route in routes):
        journeys.append("Workflow launch loop: client route can approve stages, launch named workflows, and poll workflow status.")
    if {"knowledgeSearch", "artifactContent", "updateArtifactFile"} & api_methods:
        journeys.append("Knowledge workspace loop: typed frontend API methods support search, artifact reading, and edited artifact persistence.")
    if analysis.business_artifacts:
        journeys.append("Domain-context loop: requirements, profiles, evidence, docs, and related artifacts form the operating record for product decisions.")
    if analysis.data_signals:
        journeys.append("Data/governance loop: data assets, migrations, or constraints should be validated before product behavior is treated as reliable.")
    if not journeys and ("api" in route_text or analysis.api_routes) and analysis.frontend_routes:
        journeys.append("UI-to-API flow: start from the primary frontend route, identify its data-loading calls, then trace into the matching backend handler.")
    if not journeys:
        return "No end-to-end journeys could be inferred from static route/artifact signals."
    return "\n".join(f"- {journey}" for journey in journeys)


def _validation_path(analysis: RepoAnalysis) -> str:
    steps = [
        "Start with the product record: read README, product docs, package manifests, and any requirements/PRD files together.",
        "Open the UI path next: use frontend routes to identify what a real user can inspect or change.",
        "Trace one API call from the UI into the backend route handler, then into models/services/persistence.",
        "Run the smallest local checks that cover the touched area before trusting generated output.",
        "Write down which source wins when README, product docs, route code, schema/model code, and tests disagree.",
    ]
    if analysis.commands:
        command_names = ", ".join(f"`{command['command']}`" for command in analysis.commands[:4])
        steps.append(f"Candidate commands to validate first: {command_names}.")
    return "\n".join(f"{index}. {step}" for index, step in enumerate(steps, start=1))


def _hard_questions(analysis: RepoAnalysis) -> str:
    questions = [
        "What painful user or business workflow does this repo make faster or better, and where is that visible in product docs or routes?",
        "Which single user path matters most for a first contributor: onboarding, dashboard use, auth, profile management, admin operations, or something else?",
        "What would break user trust fastest: auth/session bugs, wrong generated output, stale persisted state, bad UI state, slow backend calls, or weak data validation?",
        "Which docs describe intended behavior, and which tests prove actual behavior?",
        "What is the shortest demo path from fresh clone to a useful product outcome?",
    ]
    if not analysis.api_routes:
        questions.append("If the app has a service layer, why are API routes not obvious from static scan?")
    if not analysis.frontend_routes and analysis.frontend_signals:
        questions.append("Is the frontend a true routed app or a single workspace surface, and does that match how users work?")
    if analysis.business_artifacts:
        questions.append("Which artifact is the source of truth when product docs, requirements, API behavior, and tests disagree?")
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
        "Confirm which backend service, frontend app, and product workflow are the primary contributor path.",
        "Map one end-to-end flow from UI route to API handler to model/service/persistence.",
        "Choose the source of truth for product behavior and document conflict-resolution rules.",
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
