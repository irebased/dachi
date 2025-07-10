#!/usr/bin/env bash
set -e

REPO_URL="https://github.com/yourusername/dachi.git"
REPO_NAME="dachi"
VENV_DIR="venv"

# 1. Clone the repo if not already present
echo "[dachi] Checking for repo..."
if [ ! -d "src" ]; then
  echo "[dachi] Cloning repository..."
  git clone "$REPO_URL" "$REPO_NAME"
  cd "$REPO_NAME"
fi

# 2. Create virtual environment if not present
echo "[dachi] Setting up virtual environment..."
if [ ! -d "$VENV_DIR" ]; then
  # Ensure we're using python3 -m venv (not conda)
  if command -v python3 &> /dev/null; then
    python3 -m venv "$VENV_DIR"
  else
    echo "[dachi] Error: python3 not found. Please install Python 3.8+ and try again."
    exit 1
  fi
fi

# 3. Activate virtual environment
echo "[dachi] Activating virtual environment..."
source "$VENV_DIR/bin/activate"
echo "[dachi] Virtual environment activated: $(which python)"

# 4. Upgrade pip and install project with dev dependencies
pip install --upgrade pip
pip install -e ".[dev]"

# 5. Install pre-commit hooks
pre-commit install

# 6. Add venv bin to PATH for this session
VENV_BIN="$(pwd)/$VENV_DIR/bin"
export PATH="$VENV_BIN:$PATH"
echo "[dachi] Added $VENV_BIN to PATH for this session."

# 7. Suggest adding venv bin to shell profile for persistence
SHELL_PROFILE=""
if [ -n "$ZSH_VERSION" ]; then
  SHELL_PROFILE="$HOME/.zshrc"
elif [ -n "$BASH_VERSION" ]; then
  SHELL_PROFILE="$HOME/.bashrc"
fi
if [ -n "$SHELL_PROFILE" ]; then
  echo "[dachi] To use the 'dachi' command in new terminals, add this to your $SHELL_PROFILE:"
  echo "export PATH=\"$VENV_BIN:\$PATH\""
fi

# 8. Show success message and usage
cat <<EOF

[dachi] Setup complete! 🎉

To use the CLI, try:
  dachi --help
  dachi vigenere encrypt --key "SECRET" --text "HELLO WORLD"

To activate your environment in the future:
  source $VENV_DIR/bin/activate

To run tests (safe for macOS Terminal):
  make test-safe    # No coverage, prevents terminal crashes
  pytest --no-cov   # Alternative safe command

To run tests with coverage (may crash terminal):
  make test-cov     # With coverage reporting

To run the CLI without activating the venv:
  $VENV_BIN/dachi vigenere encrypt --key "SECRET" --text "HELLO WORLD"

Note: Always activate the virtual environment before running tests or development commands:
  source $VENV_DIR/bin/activate

Terminal Safety: If your terminal crashes after running tests, use 'make test-safe' instead of 'make test'.

Happy hacking!
EOF