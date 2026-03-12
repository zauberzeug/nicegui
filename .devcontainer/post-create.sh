#!/bin/bash
set -e

# Fix ownership of .config/gh (Docker volume mounts it as root)
sudo chown vscode:vscode /home/vscode/.config
sudo chown -R vscode:vscode /home/vscode/.config/gh

uv sync
uv run pre-commit install

# Authenticate with GitHub CLI if not already logged in
gh auth status >/dev/null 2>&1 || gh auth login -h github.com -p https -w || true
