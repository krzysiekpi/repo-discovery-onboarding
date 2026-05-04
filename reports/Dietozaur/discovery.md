# Repository Discovery Report - Dietozaur

Generated: 2026-05-04
Repository path: `/Users/krzysiekpilat/Documents/GitHub/Dietozaur`

## 1. Executive Summary

Product/context from README:
- README title: 🦕 Dietozaur
- API do personalizowanej oceny żywności z wykorzystaniem LLM. Uwzględnia profil zdrowotny użytkownika (wyniki badań, choroby, dane demograficzne) oraz rozpoznaje produkty ze zdjęć etykiet i menu.
- Dietozaur to aplikacja do personalizowanej oceny żywności, która pomaga użytkownikom podejmować świadome decyzje żywieniowe. System wykorzystuje Large Language Models (LLM) do analizy produktów i menu, uwzględniając...

- Primary stack signals: TypeScript, Python, Markdown, JSON.
- Main repo areas: `PRD/`, `docs/`, `mockup/`, `packages/`, `scripts/`.
- Backend/API surface: 32 route(s) detected.
- Frontend surface: 16 concrete route(s) detected.
- Verification candidates: `npm run build`, `npm run typecheck`, `cd packages/admin && npm run build`, `cd packages/admin && npm run dev`.
- Main risk to confirm: No GitHub Actions workflows were detected.

## 2. Discovery Confidence

- Score: 90/100 (High)
- Evidence: README/docs parsed, language mix detected, package/build manifests detected, runnable commands inferred, tests detected, backend entrypoints/routes detected, frontend surface detected, environment example detected.
- Remaining uncertainty: no CI detected.

## 3. Snapshot

- Files scanned: 288
- Current branch: `main`
- Latest commit: `59a1a188 sh names fixes`
- Origin remote: `git@github.com:jamarpl21/Dietozaur.git`
- Package managers / build systems: npm, npm lockfile, pip, python/pyproject

## 4. Product and Documentation Context

README summary:
- README title: 🦕 Dietozaur
- API do personalizowanej oceny żywności z wykorzystaniem LLM. Uwzględnia profil zdrowotny użytkownika (wyniki badań, choroby, dane demograficzne) oraz rozpoznaje produkty ze zdjęć etykiet i menu.
- Dietozaur to aplikacja do personalizowanej oceny żywności, która pomaga użytkownikom podejmować świadome decyzje żywieniowe. System wykorzystuje Large Language Models (LLM) do analizy produktów i menu, uwzględniając...

Documentation map:
- `README.md:1` - 🦕 Dietozaur
- `README.md:5` - 📋 Spis treści
- `README.md:16` - 🎯 O projekcie
- `README.md:20` - Główne funkcjonalności
- `README.md:28` - 🏗️ Struktura monorepo
- `README.md:59` - 💻 Wymagania systemowe
- `README.md:61` - Backend
- `README.md:66` - Docker (opcjonalnie)
- `README.md:70` - Przyszłe wymagania (Etap 2+)
- `README.md:74` - 🚀 Szybki start
- `README.md:76` - 1️⃣ Klonowanie repozytorium
- `README.md:83` - 2️⃣ Backend (FastAPI) - Development

Business usage signals:
- `docs/AGENTS.md` - business usage or domain context
- `docs/CLAUDE.md` - business usage or domain context
- `docs/DEPLOYMENT.md` - business usage or domain context
- `PRD/Dietozaur.md` - business usage or domain context

## 5. Technology Signals

| Language | Files | Lines |
|---|---:|---:|
| TypeScript | 145 | 10418 |
| Python | 68 | 11849 |
| Markdown | 20 | 7191 |
| JSON | 19 | 26071 |
| Shell | 9 | 718 |
| JavaScript | 5 | 795 |
| HTML | 3 | 1188 |
| CSS | 3 | 2411 |
| TOML | 1 | 47 |

## 6. Repository Shape

Top-level directories:
- `PRD/`
- `docs/`
- `mockup/`
- `packages/`
- `scripts/`

Key files:
- readme: `README.md`, `mockup/README.md`, `packages/backend/README.md`, `packages/backend/scripts/README.md`, `packages/backend/scripts/README_SCRIPTS.md`, `packages/backend/tests/fixtures/README.md`, `packages/shared/README.md`, `packages/webapp/README.md`
- package: `package.json`, `packages/admin/package.json`, `packages/backend/pyproject.toml`, `packages/backend/requirements.txt`, `packages/shared/package.json`, `packages/webapp/package.json`
- docker: `packages/backend/Dockerfile`
- config: `.env.example`, `packages/admin/postcss.config.js`, `packages/admin/tailwind.config.js`, `packages/backend/src/common/config.py`, `packages/webapp/postcss.config.js`, `packages/webapp/tailwind.config.js`

Manifests and build files:
- `package-lock.json` - npm lockfile
- `package.json` - npm package
- `packages/admin/package-lock.json` - npm lockfile
- `packages/admin/package.json` - npm package
- `packages/backend/Dockerfile` - docker image
- `packages/backend/pyproject.toml` - python project
- `packages/backend/requirements.txt` - python requirements
- `packages/shared/package.json` - npm package
- `packages/webapp/package-lock.json` - npm lockfile
- `packages/webapp/package.json` - npm package

Dependency manifests:
- `package.json`: none listed
- `packages/admin/package.json`: @sentry/react, @sentry/vite-plugin, @tanstack/react-query, @types/node, @types/react, @types/react-dom, @vitejs/plugin-react, autoprefixer, axios, class-variance-authority, clsx, date-fns, ... (21 total)
- `packages/backend/pyproject.toml`: fastapi>=0.104.0, sqlalchemy>=2.0.0, alembic>=1.12.0, pydantic>=2.0.0, pydantic-settings>=2.0.0, loguru>=0.7.0, pillow>=10.0.0
- `packages/backend/requirements.txt`: fastapi>=0.104.0, sqlalchemy>=2.0.0, alembic>=1.12.0, pydantic>=2.0.0, pydantic-settings>=2.0.0, loguru>=0.7.0, pillow>=10.0.0, python-jose[cryptography]>=3.3.0, httpx>=0.25.0, python-multipart>=0.0.6, json-repair>=0.25.0, uvicorn>=0.24.0, ... (18 total)
- `packages/shared/package.json`: @tanstack/react-query, @types/react, axios, react, tsup, typescript
- `packages/webapp/package.json`: @dietozaur/shared, @playwright/test, @sentry/react, @sentry/vite-plugin, @tanstack/react-query, @testing-library/jest-dom, @testing-library/react, @testing-library/user-event, @types/node, @types/react, @types/react-dom, @vitejs/plugin-react, ... (37 total)

## 7. Area Map

| Area | Files | Likely purpose | Languages | Notable files |
|---|---:|---|---|---|
| `PRD/` | 1 | product requirements and planning docs | Markdown | `PRD/Dietozaur.md` |
| `docs/` | 10 | architecture, setup, audit, and project documentation | Markdown | `docs/AGENTS.md`, `docs/CLAUDE.md`, `docs/DEFINITION_OF_DONE.md` |
| `mockup/` | 5 | static mockups or product prototypes | HTML, CSS, Markdown | `mockup/README.md` |
| `packages/` | 262 | monorepo packages or services | TypeScript, Python, JSON | `packages/admin/package.json`, `packages/backend/README.md`, `packages/backend/pyproject.toml` |
| `scripts/` | 1 | one-off or operational command-line scripts | Shell |  |

## 8. Detected Domains

| Domain slug | Status | Why this is a separate slice | First read | Evidence |
|---|---|---|---|---|
| `prd` | Likely | product requirements and planning docs | `PRD/Dietozaur.md` | `PRD/Dietozaur.md` |
| `docs` | Confirmed | architecture, setup, audit, and project documentation | `docs/AGENTS.md` | `docs/AGENTS.md`, `docs/CLAUDE.md`, `docs/DEFINITION_OF_DONE.md` |
| `mockup` | Confirmed | static mockups or product prototypes | `mockup/README.md` | `mockup/README.md` |
| `packages` | Confirmed | monorepo packages or services | `packages/admin/package.json` | `packages/admin/package.json`, `packages/backend/README.md`, `packages/backend/pyproject.toml` |

## 9. Current Understanding

### Product / Business

- Confirmed from README: README title: 🦕 Dietozaur
- Confirmed from README: API do personalizowanej oceny żywności z wykorzystaniem LLM. Uwzględnia profil zdrowotny użytkownika (wyniki badań, choroby, dane demograficzne) oraz rozpoznaje produkty ze zdjęć etykiet i menu.
- Confirmed from README: Dietozaur to aplikacja do personalizowanej oceny żywności, która pomaga użytkownikom podejmować świadome decyzje żywieniowe. System wykorzystuje Large Language Models (LLM) do analizy produktów i menu, uwzględniając...
- Confirmed: root documentation starts at `README.md:1` with `🦕 Dietozaur`.
- Unknown: exact production owner, deployment target, and release gate still need maintainer confirmation.

### Repository Shape
- Confirmed: meaningful repo slices include `prd`, `docs`, `mockup`, `packages`.
- Confirmed: this repo exposes both a backend API and a frontend UI surface.
- Likely: safest onboarding path is to trace one user journey across frontend, API, backend, and persistence before changing code.

## 10. Domain Artifacts and Operating Model

| Artifact | Kind | Extracted title/context |
|---|---|---|
| `PRD/Dietozaur.md` | product requirements | Dietozaur |

## 11. Source-of-Truth Analysis

| Scope | Artifact kinds present | Likely source-of-truth pressure |
|---|---|---|
| `PRD` | product requirements (1) | Medium: product intent exists; verify implementation against routes, models, and tests. |

Recommended precedence when facts conflict: product/requirements docs for intent, API and route code for actual behavior, schemas/models/migrations for persisted state, tests/CI for verified behavior, README/setup docs for local operation.

## 12. Backend and Services

Likely entrypoints:
- `packages/admin/src/App.tsx`
- `packages/admin/src/main.tsx`
- `packages/backend/src/main.py`
- `packages/shared/package.json [main: dist/index.js]`
- `packages/shared/src/index.ts`
- `packages/webapp/src/App.tsx`
- `packages/webapp/src/i18n/index.ts`
- `packages/webapp/src/main.tsx`

Signals:
- `packages/backend/alembic/env.py` - integration or service dependency signal
- `packages/backend/alembic/versions/001_create_users_and_subscriptions_tables.py` - integration or service dependency signal
- `packages/backend/alembic/versions/002_create_refresh_tokens_table.py` - integration or service dependency signal

## 13. API and UI Surface

Detected API routes:
| Method | Route | Source |
|---|---|---|
| GET | `/admin/users` | `packages/backend/src/api/admin.py:122` -> `list_users()`; calls: select, func.count, query.where, count_query.where, User.email.ilike |
| GET | `/admin/users/{user_id}` | `packages/backend/src/api/admin.py:167` -> `get_user_detail()`; calls: _get_user_or_404, logger.info, _build_user_detail |
| PATCH | `/admin/users/{user_id}` | `packages/backend/src/api/admin.py:182` -> `update_user()`; calls: _get_user_or_404, db.commit, db.refresh, logger.info, _build_user_detail |
| PATCH | `/admin/users/{user_id}/subscription` | `packages/backend/src/api/admin.py:207` -> `update_subscription()`; calls: _get_user_or_404, SubscriptionStatus, db.commit, db.refresh, logger.info |
| DELETE | `/admin/users/{user_id}` | `packages/backend/src/api/admin.py:235` -> `delete_user()`; calls: _get_user_or_404, db.delete, db.commit, logger.info |
| POST | `/admin/users/{user_id}/block` | `packages/backend/src/api/admin.py:262` -> `block_user()`; calls: _get_user_or_404, db.commit, db.refresh, logger.info, _build_user_detail |
| POST | `/admin/users/{user_id}/unblock` | `packages/backend/src/api/admin.py:282` -> `unblock_user()`; calls: _get_user_or_404, db.commit, db.refresh, logger.info, _build_user_detail |
| GET | `/admin/config` | `packages/backend/src/api/admin.py:302` -> `get_config()`; calls: app_config_service.get_config, AdminConfigResponse, app_config_service.apply_config_to_runtime |
| PATCH | `/admin/config` | `packages/backend/src/api/admin.py:330` -> `update_config()`; calls: app_config_service.get_or_create_config, logger.info, db.flush, app_config_service.apply_config_to_runtime, AdminConfigResponse |
| GET | `/admin/models` | `packages/backend/src/api/admin.py:365` -> `get_available_models()`; calls: AdminAvailableModelsResponse |
| PATCH | `/admin/users/{user_id}/llm-model` | `packages/backend/src/api/admin.py:389` -> `update_user_llm_model()`; calls: _get_user_or_404, db.commit, db.refresh, logger.info, _build_user_detail |
| POST | `/admin/users/{target_id}/merge/{source_id}` | `packages/backend/src/api/admin.py:410` -> `merge_users()`; calls: _get_user_or_404, db.flush, db.delete, db.commit, db.refresh |
| POST | `/admin/users/create` | `packages/backend/src/api/admin.py:463` -> `create_user()`; calls: db.execute, where, select, existing.scalar_one_or_none, User |
| POST | `/admin/users/{user_id}/activate` | `packages/backend/src/api/admin.py:500` -> `activate_user()`; calls: _get_user_or_404, _generate_login_url, logger.info, AdminActivateResponse |
| POST | `/auth/request-magic-link` | `packages/backend/src/api/auth.py:88` -> `request_magic_link()`; calls: auth_service.generate_magic_link_token, auth_service.record_request, logger.info, StatusResponse, auth_service.check_rate_limit |
| POST | `/auth/verify-magic-link` | `packages/backend/src/api/auth.py:157` -> `verify_magic_link()`; calls: auth_service.verify_magic_link_token, auth_service.create_access_token, _set_refresh_cookie, AuthResponse, auth_service.create_or_get_user |
| POST | `/auth/refresh` | `packages/backend/src/api/auth.py:199` -> `refresh_tokens()`; calls: _set_refresh_cookie, logger.info, TokenRefreshResponse, auth_service.validate_and_rotate_refresh_token, logger.warning |
| POST | `/auth/logout` | `packages/backend/src/api/auth.py:238` -> `logout()`; calls: auth_service.get_user_id_from_refresh_token, logger.info, auth_service.revoke_all_user_tokens, _delete_refresh_cookie, StatusResponse |
| POST | `/auth/apple/callback` | `packages/backend/src/api/auth.py:260` -> `apple_callback()`; calls: auth_service.create_access_token, _set_refresh_cookie, AuthResponse, verify_apple_id_token, auth_service.create_or_get_user |
| POST | `/auth/google/callback` | `packages/backend/src/api/auth.py:302` -> `google_callback()`; calls: auth_service.create_access_token, _set_refresh_cookie, AuthResponse, verify_google_id_token, auth_service.create_or_get_user |

Detected frontend routes:
| Route | UI component | Source |
|---|---|---|
| `/login` | `LoginPage` | `packages/admin/src/App.tsx:85` |
| `/auth/verify` | `LoginPage` | `packages/admin/src/App.tsx:86` |
| `/users` | `ProtectedRoute` | `packages/admin/src/App.tsx:88` |
| `/users/:userId` | `ProtectedRoute` | `packages/admin/src/App.tsx:98` |
| `/config` | `ProtectedRoute` | `packages/admin/src/App.tsx:108` |
| `*` | `Navigate` | `packages/admin/src/App.tsx:117` |
| `/` | `SplashPage` | `packages/webapp/src/App.tsx:103` |
| `/onboarding` | `OnboardingPage` | `packages/webapp/src/App.tsx:104` |
| `/login` | `LoginPage` | `packages/webapp/src/App.tsx:105` |
| `/auth/verify` | `LoginPage` | `packages/webapp/src/App.tsx:106` |
| `/profile-setup` | `ProtectedRoute` | `packages/webapp/src/App.tsx:109` |
| `/dashboard` | `ProtectedRoute` | `packages/webapp/src/App.tsx:118` |
| `/response` | `ProtectedRoute` | `packages/webapp/src/App.tsx:130` |
| `/profiles` | `ProtectedRoute` | `packages/webapp/src/App.tsx:142` |
| `/profiles/:id` | `ProtectedRoute` | `packages/webapp/src/App.tsx:154` |
| `/history` | `ProtectedRoute` | `packages/webapp/src/App.tsx:166` |
| `/settings` | `ProtectedRoute` | `packages/webapp/src/App.tsx:178` |
| `*` | `Navigate` | `packages/webapp/src/App.tsx:190` |

## 14. Frontend-to-API Contract

No typed frontend API client calls were detected.

## 15. Frontend and User Experience

Primary UI appears to expose 16 concrete route(s): `/login`, `/auth/verify`, `/users`, `/users/:userId`, `/config`, `/`.

Signals:
- `packages/admin/src/components/layout/AdminLayout.tsx` - frontend application path
- `packages/admin/src/components/ui/Badge.tsx` - frontend application path
- `packages/admin/src/components/ui/Button.tsx` - frontend application path
- `packages/admin/src/components/ui/Card.tsx` - frontend application path
- `packages/admin/src/components/ui/Input.tsx` - frontend application path
- `packages/admin/src/components/ui/Spinner.tsx` - frontend application path
- `packages/admin/src/pages/ConfigPage.tsx` - frontend application path
- `packages/admin/src/pages/LoginPage.tsx` - frontend application path
- `packages/admin/src/pages/UserDetailPage.tsx` - frontend application path
- `packages/admin/src/pages/UsersPage.tsx` - frontend application path
- `packages/webapp/src/components/auth/ProfileGate.tsx` - frontend application path
- `packages/webapp/src/components/BulkImportDialog.tsx` - frontend application path
- `packages/webapp/src/components/layout/BottomNav.tsx` - frontend application path
- `packages/webapp/src/components/layout/MainLayout.tsx` - frontend application path

## 16. Automation and Workflow Map

No `agents/*/workflow.py` modules were detected.

## 17. Data, Domain Model, and Governance

No strong signals detected in this area.

## 18. Likely User Journeys

- Authentication flow: login/auth routes suggest the first critical journey is sign-in, token/session handling, and post-login routing.
- User onboarding flow: onboarding routes suggest a guided first-use path before the main product dashboard.
- Core product dashboard flow: dashboard routes likely represent the main authenticated user workspace.
- Profile management flow: profile routes suggest user setup, preferences, or saved entities are central product state.
- Admin operations flow: admin/user routes suggest maintainer workflows for user management, activation, blocking, merge, and configuration.
- Result/history flow: response/history routes suggest users generate or inspect prior outputs over time.
- Domain-context loop: requirements, profiles, evidence, docs, and related artifacts form the operating record for product decisions.

## 19. Inferred Commands

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

## 20. Tests, CI, and Operations

Test files detected:
- `packages/backend/scripts/test_api.py`
- `packages/backend/scripts/test_menu_image.py`
- `packages/backend/scripts/test_requests.py`
- `packages/backend/tests/__init__.py`
- `packages/backend/tests/conftest.py`
- `packages/backend/tests/fixtures/README.md`
- `packages/backend/tests/fixtures/images/base64_sample.txt`
- `packages/backend/tests/integration/__init__.py`
- `packages/backend/tests/integration/test_e2e.py`
- `packages/backend/tests/test_auth.py`
- `packages/backend/tests/test_health.py`
- `packages/backend/tests/test_llm.py`
- No GitHub Actions workflows detected.

Environment examples:
- `.env.example`

## 21. Recommended Validation Path

1. Start with the product record: read README, product docs, package manifests, and any requirements/PRD files together.
2. Open the UI path next: use frontend routes to identify what a real user can inspect or change.
3. Trace one API call from the UI into the backend route handler, then into models/services/persistence.
4. Run the smallest local checks that cover the touched area before trusting generated output.
5. Write down which source wins when README, product docs, route code, schema/model code, and tests disagree.
6. Candidate commands to validate first: `npm run build`, `npm run typecheck`, `cd packages/admin && npm run build`, `cd packages/admin && npm run dev`.

## 22. Hard Questions

- What painful user or business workflow does this repo make faster or better, and where is that visible in product docs or routes?
- Which single user path matters most for a first contributor: onboarding, dashboard use, auth, profile management, admin operations, or something else?
- What would break user trust fastest: auth/session bugs, wrong generated output, stale persisted state, bad UI state, slow backend calls, or weak data validation?
- Which docs describe intended behavior, and which tests prove actual behavior?
- What is the shortest demo path from fresh clone to a useful product outcome?
- Which artifact is the source of truth when product docs, requirements, API behavior, and tests disagree?
- Which detected command is the actual release gate, not just a local convenience command?

## 23. Risks and Open Questions

- No GitHub Actions workflows were detected.
- 1 TODO/FIXME/HACK markers detected in scanned files.

Sample TODO/FIXME/HACK markers:
- `packages/backend/README.md:274` - - **Metrics**: TODO (Prometheus w przyszłości)

## 24. Suggested Next Steps

- Run the most relevant detected setup/test commands and record exact pass/fail output.
- Confirm which backend service, frontend app, and product workflow are the primary contributor path.
- Map one end-to-end flow from UI route to API handler to model/service/persistence.
- Choose the source of truth for product behavior and document conflict-resolution rules.
- Add a minimal CI workflow once the test command is confirmed.
