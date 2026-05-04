Do NOT run python -m agents.*

# /repo-onboarding

Generate both repository discovery and developer onboarding artifacts for a local target repo.

## Usage

```text
/repo-onboarding /absolute/path/to/repo
```

Optional:

```text
/repo-onboarding /absolute/path/to/repo --out ./reports/custom-name
/repo-onboarding /absolute/path/to/repo --role ceo
/repo-onboarding /absolute/path/to/repo --role frontend
```

## Step 0 - Resolve Paths

Use this Bash block to resolve paths and run the local CLI.

```bash
set -euo pipefail

COMMAND_REPO_ROOT="$(pwd)"
TARGET_REPO="$(printf '%s\n' "$ARGUMENTS" | awk '{print $1}')"
CUSTOM_OUT="$(printf '%s\n' "$ARGUMENTS" | sed -n 's/.*--out[[:space:]]\+\([^[:space:]]\+\).*/\1/p')"
ROLE="$(printf '%s\n' "$ARGUMENTS" | sed -n 's/.*--role[[:space:]]\+\([^[:space:]]\+\).*/\1/p')"
[ -z "$ROLE" ] && ROLE="all"

if [ -z "$TARGET_REPO" ]; then
  echo "Usage: /repo-onboarding /absolute/path/to/repo [--out ./reports/name]"
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

PYTHONPATH="$COMMAND_REPO_ROOT/src" python3 -m repo_onboarding all \
  --repo "$TARGET_REPO" \
  --out "$OUTPUT_DIR" \
  --role "$ROLE"

if [ "$ROLE" = "all" ]; then
  ONBOARDING_FILE="$OUTPUT_DIR/onboarding.md"
else
  ONBOARDING_FILE="$OUTPUT_DIR/onboarding_${ROLE}.md"
fi
printf 'DISCOVERY_REPORT=%s\nONBOARDING_GUIDE=%s\n' "$OUTPUT_DIR/discovery.md" "$ONBOARDING_FILE"
```

## Step 1 - Return Result

Read the generated artifact paths:

```text
reports/{repo-name}/discovery.md
reports/{repo-name}/onboarding.md
```

Final response must include:

- path to `discovery.md`
- path to `onboarding.md`
- short summary of detected stack, tests/CI, and setup risks
