# Repo Discovery Onboarding

Small CLI for testing a repository discovery and role-based onboarding flow against any local codebase.

It is intentionally static and local:

- reads a local repo path passed with `--repo`
- detects repo shape, dependency manifests, commands, API routes, frontend routes, frontend API clients, workflow contracts, business artifacts, source-of-truth pressure, tests, CI, env examples, TODO markers, and setup risks
- writes two markdown artifacts: `discovery.md` and `onboarding.md`
- does not require API keys, warehouse access, or data-platform-specific folders
- skips common build/cache folders such as `.git`, `node_modules`, `.venv`, `dist`, and `target`

The output is meant for beta testing with real repos. It should be accurate enough to start a useful conversation, but still needs maintainer review for repo-specific ownership, release gates, and production setup.

Requires Python 3.9 or newer.

## Install

Choose a folder where you keep GitHub projects, clone this tool, and install it in a local virtual environment:

```bash
mkdir -p ~/Documents/GitHub
cd ~/Documents/GitHub

git clone https://github.com/krzysiekpi/discovery-onboarding.git
cd discovery-onboarding

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Quick Start

Run this from inside `discovery-onboarding`.

Replace `/absolute/path/to/their/repo` with the repo you want to inspect. The path must point to a local folder that already exists on your machine.

```bash
repo-onboarding all \
  --repo /absolute/path/to/their/repo \
  --out ./reports/their-repo
```

Outputs:

```text
reports/their-repo/discovery.md
reports/their-repo/onboarding.md
```

Tip: on macOS/Linux, you can get the absolute path for the current folder with:

```bash
pwd
```

## Run Options

You can also run one artifact at a time:

```bash
repo-onboarding discovery --repo /path/to/repo --out ./reports/repo
repo-onboarding onboarding --repo /path/to/repo --out ./reports/repo
```

Generate a role-focused onboarding guide:

```bash
repo-onboarding onboarding \
  --repo /path/to/repo \
  --out ./reports/repo \
  --role frontend
```

Supported roles:

- `all` (default) -> `onboarding.md`
- `analyst` -> `onboarding_analyst.md`
- `frontend` -> `onboarding_frontend.md`
- `backend` -> `onboarding_backend.md`
- `data-governance` -> `onboarding_data-governance.md`
- `project-manager` -> `onboarding_project-manager.md`

Refresh an onboarding guide while preserving manual notes:

```bash
repo-onboarding onboarding \
  --repo /path/to/repo \
  --out ./reports/repo \
  --role frontend \
  --update
```

`--update` preserves text between:

```markdown
<!-- MANUAL_NOTES:START -->
...
<!-- MANUAL_NOTES:END -->
```

## What The Artifacts Contain

`discovery.md` is the horizontal source of truth:

- confirmed/likely/unknown current understanding
- detected repo domains / vertical slices from file evidence
- area map with likely purpose per folder
- backend API routes and handlers
- frontend routes and typed API client calls
- workflow contracts
- business artifacts and source-of-truth pressure
- likely user journeys, hard questions, risks, and next actions

`onboarding.md` is the role-based entry guide:

- executive orientation and first-day plan
- local setup and verification commands
- detected repo domains and must-read files
- first 30 minutes / first day / first week learning order
- role tracks for analyst, frontend developer, backend developer, data/governance engineer, and project manager
- API/UI/workflow contracts
- source-of-truth rules, first contribution paths, avoid-week-1 guidance, and quality bar

## Claude Code Slash Commands

This repo also includes project commands in `.claude/commands/`.

After cloning this repo, open Claude Code from the repo root and run:

```text
/repo-onboarding /absolute/path/to/friends-startup-repo
```

Or run one artifact at a time:

```text
/discovery /absolute/path/to/friends-startup-repo
/onboarding /absolute/path/to/friends-startup-repo
/onboarding /absolute/path/to/friends-startup-repo --role ceo
/onboarding /absolute/path/to/friends-startup-repo --role frontend
/onboarding /absolute/path/to/friends-startup-repo --role backend
```

The commands write markdown files under:

```text
reports/{repo-name}/discovery.md
reports/{repo-name}/onboarding.md
```

Optional custom output path:

```text
/repo-onboarding /absolute/path/to/friends-startup-repo --out ./reports/custom-name
/discovery /absolute/path/to/friends-startup-repo --out ./reports/custom-name
/onboarding /absolute/path/to/friends-startup-repo --out ./reports/custom-name
```

Focused onboarding and update mode:

```text
/onboarding /absolute/path/to/friends-startup-repo --role analyst
/onboarding /absolute/path/to/friends-startup-repo --role frontend --update
/repo-onboarding /absolute/path/to/friends-startup-repo --role backend
```

## No Install Alternative

From this repo root:

```bash
PYTHONPATH=src python3 -m repo_onboarding all --repo /path/to/repo --out ./reports/repo
```

## What To Share With A Friend

Ask them to run this full copy/paste flow:

```bash
mkdir -p ~/Documents/GitHub
cd ~/Documents/GitHub

git clone https://github.com/krzysiekpi/discovery-onboarding.git
cd discovery-onboarding

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"

repo-onboarding all --repo /absolute/path/to/their/repo --out ./reports/their-repo
```

If they want role-specific guides too:

```bash
repo-onboarding onboarding --repo /absolute/path/to/their/repo --out ./reports/their-repo --role analyst
repo-onboarding onboarding --repo /absolute/path/to/their/repo --out ./reports/their-repo --role frontend
repo-onboarding onboarding --repo /absolute/path/to/their/repo --out ./reports/their-repo --role backend
repo-onboarding onboarding --repo /absolute/path/to/their/repo --out ./reports/their-repo --role data-governance
repo-onboarding onboarding --repo /absolute/path/to/their/repo --out ./reports/their-repo --role project-manager
```

Then they can send back:

- `reports/their-repo/discovery.md`
- `reports/their-repo/onboarding.md`
- any role-specific files such as `reports/their-repo/onboarding_frontend.md`

Ask them to review:

- Are detected domains useful or noisy?
- Does discovery correctly identify the product/business workflow?
- Does onboarding tell each role where to start?
- Are setup and verification commands accurate?
- What source-of-truth or ownership question is missing?

## Development

```bash
python -m pip install -e ".[dev]"
.venv/bin/pytest -q
```

## Current Scope

This is a developer-repo test harness, not the full analytics platform. It does not copy client workflow state, warehouse connectors, semantic-layer checks, Studio UI, or LLM agents from the original repo.
