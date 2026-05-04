# Repo Discovery Onboarding

Small CLI for testing a repository discovery and developer onboarding flow against any local codebase.

It is intentionally static and lightweight:

- reads a local repo path passed with `--repo`
- detects languages, dependency manifests, package scripts, docs, tests, CI, env examples, TODO markers, and setup risks
- writes two markdown artifacts: `discovery.md` and `onboarding.md`
- does not require API keys, warehouse access, or data-platform-specific folders
- skips common build/cache folders such as `.git`, `node_modules`, `.venv`, `dist`, and `target`

## Install

```bash
git clone https://github.com/krzysiekpi/repo-discovery-onboarding.git
cd repo-discovery-onboarding

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Run Against Another Repo

Pass the path to the repo you want to inspect:

```bash
repo-onboarding all \
  --repo /path/to/friends-startup-repo \
  --out ./reports/friends-startup-repo
```

Outputs:

```text
reports/friends-startup-repo/discovery.md
reports/friends-startup-repo/onboarding.md
```

You can also run one artifact at a time:

```bash
repo-onboarding discovery --repo /path/to/repo --out ./reports/repo
repo-onboarding onboarding --repo /path/to/repo --out ./reports/repo
```

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
```

The commands write markdown files under:

```text
reports/{repo-name}/discovery.md
reports/{repo-name}/onboarding.md
```

## No Install Alternative

From this repo root:

```bash
PYTHONPATH=src python3 -m repo_onboarding all --repo /path/to/repo --out ./reports/repo
```

## What To Share With A Friend

Ask them to run:

```bash
git clone https://github.com/krzysiekpi/repo-discovery-onboarding.git
cd repo-discovery-onboarding
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
repo-onboarding all --repo /absolute/path/to/their/repo --out ./reports/their-repo
```

Then they can send back:

- `reports/their-repo/discovery.md`
- `reports/their-repo/onboarding.md`

## Development

```bash
python -m pip install -e ".[dev]"
pytest -q
```

## Current Scope

This is a developer-repo test harness, not the full analytics platform. It does not copy client workflow state, warehouse connectors, semantic-layer checks, Studio UI, or LLM agents from the original repo.
