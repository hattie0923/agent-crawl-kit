#!/usr/bin/env bash
set -euo pipefail

REPO_URL="${AGENT_CRAWL_REPO_URL:-https://github.com/hattie0923/agent-crawl-kit.git}"
INSTALL_DIR="${AGENT_CRAWL_INSTALL_DIR:-$HOME/.agent-crawl-kit}"
SKILL_DIR="${AGENT_CRAWL_SKILL_DIR:-}"
PYTHON_BIN="${PYTHON_BIN:-python3}"

usage() {
  cat <<'EOF'
Agent Crawl Kit installer

Usage:
  scripts/install.sh [options]

Options:
  --repo-url URL       Git repository URL. Defaults to the company repo.
  --install-dir DIR    Install directory. Defaults to ~/.agent-crawl-kit.
  --skill-dir DIR      Optional agent skill directory. Copies agent-crawl/SKILL.md there.
  --help              Show this help.

Environment:
  AGENT_CRAWL_REPO_URL
  AGENT_CRAWL_INSTALL_DIR
  AGENT_CRAWL_SKILL_DIR
  PYTHON_BIN
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo-url)
      REPO_URL="$2"
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

if [[ -d "$INSTALL_DIR/.git" ]]; then
  echo "Updating Agent Crawl Kit in $INSTALL_DIR"
  git -C "$INSTALL_DIR" pull --ff-only
elif [[ -e "$INSTALL_DIR" ]]; then
  echo "Install directory exists but is not a git repository: $INSTALL_DIR" >&2
  exit 1
else
  echo "Cloning Agent Crawl Kit into $INSTALL_DIR"
  git clone "$REPO_URL" "$INSTALL_DIR"
fi

cd "$INSTALL_DIR"

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
  echo "Skill install skipped. Set --skill-dir or AGENT_CRAWL_SKILL_DIR to install it."
fi

echo
echo "Install complete."
echo "Run:"
echo "  source \"$INSTALL_DIR/.venv/bin/activate\""
echo "  agent-crawl doctor --format markdown"
echo
agent-crawl doctor --format markdown

