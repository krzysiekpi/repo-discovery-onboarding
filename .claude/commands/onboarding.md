Do NOT run python -m agents.*

# /onboarding

Generate a role-based onboarding guide for a local target repo.
The guide should be useful for analysts, frontend developers, backend
developers, data/governance engineers, and project managers. It should explain
how to enter the repo through business artifacts, UI/API/workflow contracts,
verification commands, and first contribution paths.
It should use the detected repo domains / vertical slices from discovery-style
evidence rather than a fixed taxonomy, and include must-read files, first
30-minutes / first-day / first-week guidance, starter tasks, and avoid-week-1
areas.

## Usage

```text
/onboarding /absolute/path/to/repo
```

Optional:

```text
/onboarding /absolute/path/to/repo --out ./reports/custom-name
/onboarding /absolute/path/to/repo --role ceo
/onboarding /absolute/path/to/repo --role analyst
/onboarding /absolute/path/to/repo --role frontend
/onboarding /absolute/path/to/repo --role backend
/onboarding /absolute/path/to/repo --role data-governance
/onboarding /absolute/path/to/repo --role project-manager
/onboarding /absolute/path/to/repo --role frontend --update
```

Role output files:
- default / `--role all` -> `onboarding.md`
- focused roles -> `onboarding_{role}.md`

`--update` refreshes command-owned content and preserves the block between
`<!-- MANUAL_NOTES:START -->` and `<!-- MANUAL_NOTES:END -->`.

## Step 0 - Resolve Paths

Use this Bash block to resolve paths and run the local CLI.

```bash
set -euo pipefail

COMMAND_REPO_ROOT="$(pwd)"
TARGET_REPO="$(printf '%s\n' "$ARGUMENTS" | awk '{print $1}')"
CUSTOM_OUT="$(printf '%s\n' "$ARGUMENTS" | sed -n 's/.*--out[[:space:]]\+\([^[:space:]]\+\).*/\1/p')"
ROLE="$(printf '%s\n' "$ARGUMENTS" | sed -n 's/.*--role[[:space:]]\+\([^[:space:]]\+\).*/\1/p')"
printf '%s\n' "$ARGUMENTS" | grep -q -- "--update" && UPDATE_FLAG="--update" || UPDATE_FLAG=""
[ -z "$ROLE" ] && ROLE="all"

if [ -z "$TARGET_REPO" ]; then
  echo "Usage: /onboarding /absolute/path/to/repo [--out ./reports/name]"
  exit 2
fi

if [ ! -d "$TARGET_REPO" ]; then
  echo "Target repo does not exist: $TARGET_REPO"
  exit 2
fi

TARGET_NAME="$(basename "$TARGET_REPO")"
if [ -n "$CUSTOM_OUT" ]; then
  OUTPUT_DIR="$CUSTOM_OUT"
else
  OUTPUT_DIR="$COMMAND_REPO_ROOT/reports/$TARGET_NAME"
fi

printf 'COMMAND_REPO_ROOT=%s\nTARGET_REPO=%s\nOUTPUT_DIR=%s\n' "$COMMAND_REPO_ROOT" "$TARGET_REPO" "$OUTPUT_DIR"

PYTHONPATH="$COMMAND_REPO_ROOT/src" python3 -m repo_onboarding onboarding \
  --repo "$TARGET_REPO" \
  --out "$OUTPUT_DIR" \
  --role "$ROLE" \
  $UPDATE_FLAG

if [ "$ROLE" = "all" ]; then
  ONBOARDING_FILE="$OUTPUT_DIR/onboarding.md"
else
  ONBOARDING_FILE="$OUTPUT_DIR/onboarding_${ROLE}.md"
fi
printf 'ONBOARDING_GUIDE=%s\n' "$ONBOARDING_FILE"
```

## Step 1 - Return Result

Read the generated guide path:

```text
reports/{repo-name}/onboarding.md
```

Final response must include:

- path to `onboarding.md`
- role tracks included
- selected role if `--role` was passed
- whether `--update` preserved manual notes
- detected domains and must-read files
- local setup and verification commands detected
- the most important source-of-truth or business-risk note from the guide
