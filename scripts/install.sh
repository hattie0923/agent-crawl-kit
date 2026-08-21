#!/usr/bin/env bash
set -euo pipefail

REPO_URL="${AGENT_CRAWL_REPO_URL:-https://github.com/hattie0923/agent-crawl-kit.git}"
REPO_REF="${AGENT_CRAWL_REF:-main}"
INSTALL_DIR="${AGENT_CRAWL_INSTALL_DIR:-$HOME/.agent-crawl-kit}"
SKILL_DIR="${AGENT_CRAWL_SKILL_DIR:-}"
AGENT_TARGET="${AGENT_CRAWL_AGENT:-}"
PYTHON_BIN="${PYTHON_BIN:-python3}"

usage() {
  cat <<'EOF'
Agent Crawl Kit installer

Usage:
  scripts/install.sh [options]

Options:
  --repo-url URL       Git repository URL. Defaults to the company repo.
  --ref REF            Branch, tag, or commit to install. Defaults to main.
  --install-dir DIR    Install directory. Defaults to ~/.agent-crawl-kit.
  --skill-dir DIR      Optional agent skill directory. Copies agent-crawl/SKILL.md there.
  --agent NAME         Optional agent target: auto, trae, claude, cursor, generic, none.
  --help              Show this help.

Environment:
  AGENT_CRAWL_REPO_URL
  AGENT_CRAWL_REF
  AGENT_CRAWL_INSTALL_DIR
  AGENT_CRAWL_SKILL_DIR
  AGENT_CRAWL_AGENT
  PYTHON_BIN
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo-url)
      REPO_URL="$2"
      shift 2
      ;;
    --ref)
      REPO_REF="$2"
      shift 2
      ;;
    --install-dir)
      INSTALL_DIR="$2"
      shift 2
      ;;
    --skill-dir)
      SKILL_DIR="$2"
      shift 2
      ;;
    --agent)
      AGENT_TARGET="$2"
      shift 2
      ;;
    --help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

require_command() {
  local command_name="$1"
  if ! command -v "$command_name" >/dev/null 2>&1; then
    echo "Missing required command: $command_name" >&2
    exit 1
  fi
}

require_command git
require_command "$PYTHON_BIN"

agent_skill_dir() {
  local agent_name="$1"
  case "$agent_name" in
    trae)
      echo "$HOME/.trae/skills"
      ;;
    claude)
      echo "$HOME/.claude/skills"
      ;;
    cursor)
      echo "$HOME/.cursor/skills"
      ;;
    generic)
      echo "$HOME/.agents/skills"
      ;;
    none|"")
      echo ""
      ;;
    *)
      echo "Unknown agent target: $agent_name" >&2
      echo "Supported targets: auto, trae, claude, cursor, generic, none" >&2
      exit 2
      ;;
  esac
}

detect_skill_dir() {
  local candidates=(
    "$HOME/.trae/skills"
    "$HOME/.claude/skills"
    "$HOME/.cursor/skills"
    "$HOME/.agents/skills"
  )
  local candidate
  for candidate in "${candidates[@]}"; do
    if [[ -d "$candidate" ]]; then
      echo "$candidate"
      return 0
    fi
  done
  echo "$HOME/.agents/skills"
}

if [[ -z "$SKILL_DIR" && -n "$AGENT_TARGET" && "$AGENT_TARGET" != "none" ]]; then
  if [[ "$AGENT_TARGET" == "auto" ]]; then
    SKILL_DIR="$(detect_skill_dir)"
  else
    SKILL_DIR="$(agent_skill_dir "$AGENT_TARGET")"
  fi
fi

if [[ -d "$INSTALL_DIR/.git" ]]; then
  echo "Updating Agent Crawl Kit in $INSTALL_DIR"
  git -C "$INSTALL_DIR" fetch --tags origin
elif [[ -e "$INSTALL_DIR" ]]; then
  echo "Install directory exists but is not a git repository: $INSTALL_DIR" >&2
  exit 1
else
  echo "Cloning Agent Crawl Kit into $INSTALL_DIR"
  git clone "$REPO_URL" "$INSTALL_DIR"
fi

cd "$INSTALL_DIR"
git checkout "$REPO_REF"
if [[ "$REPO_REF" == "main" ]]; then
  git pull --ff-only origin main
fi

if [[ ! -d .venv ]]; then
  "$PYTHON_BIN" -m venv .venv
fi

# shellcheck disable=SC1091
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e .

if [[ -n "$SKILL_DIR" ]]; then
  mkdir -p "$SKILL_DIR/agent-crawl"
  cp "$INSTALL_DIR/skills/agent-crawl/SKILL.md" "$SKILL_DIR/agent-crawl/SKILL.md"
  echo "Installed skill to $SKILL_DIR/agent-crawl/SKILL.md"
else
  echo "Skill install skipped. Set --agent auto, --skill-dir, AGENT_CRAWL_AGENT, or AGENT_CRAWL_SKILL_DIR to install it."
fi

echo
echo "Install complete."
echo "Run:"
echo "  source \"$INSTALL_DIR/.venv/bin/activate\""
echo "  agent-crawl doctor --format markdown"
echo
agent-crawl doctor --format markdown
