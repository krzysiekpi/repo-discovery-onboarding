# Onboarding Guide - Dietozaur

Generated: 2026-05-04
Role focus: CEO / Founder

## 1. Executive Orientation

This repository is primarily a `Dietozaur` workspace with these strongest static signals:
- Stack/build signals: npm, npm lockfile, pip, python/pyproject.
- API surface: 32 detected route(s), starting in `packages/backend/src/api/admin.py`.
- UI surface: 16 concrete React route(s): `/login`, `/auth/verify`, `/users`, `/users/:userId`, `/config`, `/`, `/onboarding`, `/login`.
- Product/domain record: requirements, docs, schemas, routes, and tests should be read together before trusting a behavior claim.

Onboarding goal for CEO / Founder: follow the focused track below, trace one relevant workflow, then make one small verified contribution.

## 2. First Day Plan

1. Read the root `README.md` and the generated discovery report for this repo.
2. Use the `CEO / Founder` track in Section 8; do not try to learn every folder first.
3. Trace one user journey from Section 9 through UI, API, services, data model, and tests.
4. Run the smallest local verification command for your role.
5. Write down the source-of-truth rule you used if docs, code, schemas, and tests disagree.

Root README anchors worth reading first:
- `README.md:1` - 🦕 Dietozaur
- `README.md:5` - 📋 Spis treści
- `README.md:16` - 🎯 O projekcie
- `README.md:20` - Główne funkcjonalności
- `README.md:28` - 🏗️ Struktura monorepo
- `README.md:59` - 💻 Wymagania systemowe
- `README.md:61` - Backend
- `README.md:66` - Docker (opcjonalnie)

## 3. Local Setup and Verification

Use these steps as a starting point; confirm project-specific secrets with the maintainer.
- Install JavaScript dependencies: `npm install`
- Install JavaScript dependencies: `cd packages/admin && npm install`
- Install JavaScript dependencies: `cd packages/shared && npm install`
- Install JavaScript dependencies: `cd packages/webapp && npm install`
- Install Python package locally: `python -m pip install -e .`
- Install Python requirements: `python -m pip install -r packages/backend/requirements.txt`
- Copy the environment example and fill local values: `.env.example`

Verification candidates:
- `npm run build` (package.json)
- `npm run typecheck` (package.json)
- `cd packages/admin && npm run build` (packages/admin/package.json)
- `cd packages/admin && npm run dev` (packages/admin/package.json)
- `cd packages/admin && npm run lint` (packages/admin/package.json)
- `cd packages/admin && npm run preview` (packages/admin/package.json)
- `cd packages/shared && npm run build` (packages/shared/package.json)
- `cd packages/shared && npm run typecheck` (packages/shared/package.json)

## 4. Architecture Map

| Area | Files | Likely purpose | Languages | Notable files |
|---|---:|---|---|---|
| `PRD/` | 1 | product requirements and planning docs | Markdown | `PRD/Dietozaur.md` |
| `docs/` | 10 | architecture, setup, audit, and project documentation | Markdown | `docs/AGENTS.md`, `docs/CLAUDE.md`, `docs/DEFINITION_OF_DONE.md` |
| `mockup/` | 5 | static mockups or product prototypes | HTML, CSS, Markdown | `mockup/README.md` |
| `packages/` | 262 | monorepo packages or services | TypeScript, Python, JSON | `packages/admin/package.json`, `packages/backend/README.md`, `packages/backend/pyproject.toml` |
| `scripts/` | 1 | one-off or operational command-line scripts | Shell |  |

## 5. Detected Repo Domains

| Domain slug | Status | Why this is a separate slice | First read | Evidence |
|---|---|---|---|---|
| `prd` | Likely | product requirements and planning docs | `PRD/Dietozaur.md` | `PRD/Dietozaur.md` |
| `docs` | Confirmed | architecture, setup, audit, and project documentation | `docs/AGENTS.md` | `docs/AGENTS.md`, `docs/CLAUDE.md`, `docs/DEFINITION_OF_DONE.md` |
| `mockup` | Confirmed | static mockups or product prototypes | `mockup/README.md` | `mockup/README.md` |
| `packages` | Confirmed | monorepo packages or services | `packages/admin/package.json` | `packages/admin/package.json`, `packages/backend/README.md`, `packages/backend/pyproject.toml` |

## 6. Must-Read Files

- `README.md`
- `PRD/Dietozaur.md`
- `docs/AGENTS.md`
- `mockup/README.md`
- `packages/admin/package.json`

## 7. Recommended Order of Learning

### First 30 minutes
- Read the root README and this onboarding guide's executive orientation.
- Pick one role track and one detected repo domain.
- Open the first-read file for that domain.

### First day
- Run local setup for the touched area.
- Trace one journey through UI/API/workflow/artifact boundaries.
- Identify the source-of-truth docs/code/tests for one product domain.

### First week
- Make one small contribution from Section 13.
- Run the narrowest relevant verification command.
- Write down any unknown ownership, source-of-truth, or release-gate questions.

## 8. Role Tracks

### CEO / Founder

Purpose: understand what the product does, where execution risk sits, and what demo path proves the repo is alive.

Product thesis from repo evidence:
- README title: 🦕 Dietozaur
- API do personalizowanej oceny żywności z wykorzystaniem LLM. Uwzględnia profil zdrowotny użytkownika (wyniki badań, choroby, dane demograficzne) oraz rozpoznaje produkty ze zdjęć etykiet i menu.
- Dietozaur to aplikacja do personalizowanej oceny żywności, która pomaga użytkownikom podejmować świadome decyzje żywieniowe. System wykorzystuje Large Language Models (LLM) do analizy produktów i menu, uwzględniając...

Read first:
- `README.md`
- `PRD/Dietozaur.md`
- `docs/AGENTS.md`
- `mockup/README.md`
- `packages/admin/package.json`

Evaluate first:
- Product promise: does README/PRD clearly state the user pain and expected outcome?
- Demo path: can someone go from login/onboarding to dashboard/result/history without maintainer help?
- Trust risk: what breaks confidence fastest: auth, LLM output quality, profile data, image/menu parsing, or admin controls?
- Delivery risk: which command is the real release gate, and why is CI missing or present?
- Ownership: who owns product intent when README/PRD, implemented routes, and tests disagree?

Do first:
- Ask the team to run the shortest demo and narrate which routes/API calls prove the main product loop.
- Pick one KPI for the next build slice: activation, successful analysis, saved profile, repeat use, or admin reliability.
- Turn one open question from the discovery report into a concrete acceptance check.

Avoid: judging progress by repo activity alone; insist on one product journey, one verification command, and one owner for source-of-truth conflicts.

## 9. Core User Journeys

- Authentication flow: login/auth routes suggest the first critical journey is sign-in, token/session handling, and post-login routing.
- User onboarding flow: onboarding routes suggest a guided first-use path before the main product dashboard.
- Core product dashboard flow: dashboard routes likely represent the main authenticated user workspace.
- Profile management flow: profile routes suggest user setup, preferences, or saved entities are central product state.
- Admin operations flow: admin/user routes suggest maintainer workflows for user management, activation, blocking, merge, and configuration.
- Result/history flow: response/history routes suggest users generate or inspect prior outputs over time.
- Domain-context loop: requirements, profiles, evidence, docs, and related artifacts form the operating record for product decisions.

## 10. API, UI, and Workflow Contracts


Backend handlers:
- GET `/admin/users` -> `list_users()`
- GET `/admin/users/{user_id}` -> `get_user_detail()`
- PATCH `/admin/users/{user_id}` -> `update_user()`
- PATCH `/admin/users/{user_id}/subscription` -> `update_subscription()`
- DELETE `/admin/users/{user_id}` -> `delete_user()`
- POST `/admin/users/{user_id}/block` -> `block_user()`
- POST `/admin/users/{user_id}/unblock` -> `unblock_user()`
- GET `/admin/config` -> `get_config()`
- PATCH `/admin/config` -> `update_config()`
- GET `/admin/models` -> `get_available_models()`
- PATCH `/admin/users/{user_id}/llm-model` -> `update_user_llm_model()`
- POST `/admin/users/{target_id}/merge/{source_id}` -> `merge_users()`

## 11. Business Source of Truth

| Scope | Artifact kinds present | Likely source-of-truth pressure |
|---|---|---|
| `PRD` | product requirements (1) | Medium: product intent exists; verify implementation against routes, models, and tests. |

Recommended precedence when facts conflict: product/requirements docs for intent, API and route code for actual behavior, schemas/models/migrations for persisted state, tests/CI for verified behavior, README/setup docs for local operation.

## 12. Common Commands

| Name | Command | Source | Details |
|---|---|---|---|
| build | `npm run build` | `package.json` | `npm run -w @dietozaur/shared build && npm run -w @dietozaur/webapp build && npm run -w @dietozaur/admin build` |
| typecheck | `npm run typecheck` | `package.json` | `npm run -w @dietozaur/shared typecheck && npm run -w @dietozaur/webapp build && npm run -w @dietozaur/admin build` |
| build | `cd packages/admin && npm run build` | `packages/admin/package.json` | `tsc -b && vite build` |
| dev | `cd packages/admin && npm run dev` | `packages/admin/package.json` | `vite` |
| lint | `cd packages/admin && npm run lint` | `packages/admin/package.json` | `eslint .` |
| preview | `cd packages/admin && npm run preview` | `packages/admin/package.json` | `vite preview` |
| build | `cd packages/shared && npm run build` | `packages/shared/package.json` | `tsup` |
| typecheck | `cd packages/shared && npm run typecheck` | `packages/shared/package.json` | `tsc --noEmit` |
| build | `cd packages/webapp && npm run build` | `packages/webapp/package.json` | `tsc -b && vite build` |
| dev | `cd packages/webapp && npm run dev` | `packages/webapp/package.json` | `vite` |
| lint | `cd packages/webapp && npm run lint` | `packages/webapp/package.json` | `eslint .` |
| preview | `cd packages/webapp && npm run preview` | `packages/webapp/package.json` | `vite preview` |
| test | `cd packages/webapp && npm run test` | `packages/webapp/package.json` | `vitest run` |
| test:all | `cd packages/webapp && npm run test:all` | `packages/webapp/package.json` | `vitest run && playwright test` |
| test:e2e | `cd packages/webapp && npm run test:e2e` | `packages/webapp/package.json` | `playwright test` |
| test:e2e:headed | `cd packages/webapp && npm run test:e2e:headed` | `packages/webapp/package.json` | `playwright test --headed` |
| test:e2e:ui | `cd packages/webapp && npm run test:e2e:ui` | `packages/webapp/package.json` | `playwright test --ui` |
| test:ui | `cd packages/webapp && npm run test:ui` | `packages/webapp/package.json` | `vitest --ui` |
| test:watch | `cd packages/webapp && npm run test:watch` | `packages/webapp/package.json` | `vitest` |
| pytest | `python -m pytest` | `tests/` | `inferred from Python tests` |

## 13. First Contribution Paths

- CEO/founder: turn one unclear product-risk question into an acceptance check for the next slice.
- Product/domain: improve one docs/requirements inconsistency and document the precedence used.
- Frontend: improve one route/page state, then run frontend tests/typecheck.
- Backend: add or tighten one API response path without bypassing existing service helpers.
- Data/governance: add one validation fixture or constraint rule and prove it with tests.
- Project manager: convert one vague roadmap item into an artifact-backed acceptance checklist.

## 14. Avoid in Week 1

- Do not edit generated or persisted domain artifacts unless validation expectations are explicit.
- Do not change artifact write behavior without preserving path traversal checks, backups, and edit logs.
- Do not treat prose docs as authoritative when code, schemas, tests, or migrations conflict.
- Do not start by refactoring shared utilities before tracing one concrete user journey.

## 15. Quality Bar

- Every change should name the role/user journey it improves.
- Every product-facing claim should point to README, PRD, requirements, route code, schemas/models, or tests.
- Generated or persisted outputs need visible loading/error/success status when shown or edited.
- API changes should preserve authentication, authorization, validation, and error semantics.
- UI changes should preserve typed API contracts and error visibility.
- Run the narrowest relevant command from Section 12 before opening a PR.

## 16. Maintainer Questions

- What command starts the app locally?
- What command is required before a PR is considered safe?
- Which external services are required for a full local run?
- Where is the product boundary between core app, workers, scripts, and infrastructure?
- Is CI intentionally absent, or should a basic workflow be added?

## Manual Notes

Notes below are preserved when rerunning with `--update`.

<!-- MANUAL_NOTES:START -->

<!-- MANUAL_NOTES:END -->
