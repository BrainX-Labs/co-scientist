#!/bin/bash
set -e

# 1. Copy .env.example to .env if .env doesn't exist
if [ ! -f .env ]; then
  cp .env.example .env
fi

# 2. Install Pi Agent CLI & Extensions
curl -fsSL https://pi.dev/install.sh | sh
export PATH="$HOME/.pi/bin:$PATH"
pi install npm:pi-mcp-extension --approve
pi install npm:pi-web-access --approve

# 3. Install LiteLLM Proxy, paper search, and Lean LSP MCP runner
pip install 'litellm[proxy]' paper-search-mcp uv

# 4. Install Lean 4 Theorem Prover via Elan
curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh -s -- -y
export PATH="$HOME/.elan/bin:$PATH"

# 5. Initialize Lean Workspace with Mathlib
lake new lean4_workspace math || true
lake -C lean4_workspace build

echo "Setup complete! All tools, provers, and agent dependencies installed."
