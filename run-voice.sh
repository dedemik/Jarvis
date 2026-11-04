#!/bin/sh
set -eu

PROJECT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PYTHON="$PROJECT_DIR/.venv/bin/python"

if [ ! -x "$PYTHON" ]; then
    printf '%s\n' "Sanal ortam bulunamadı. Önce ./install.sh çalıştır." >&2
    exit 1
fi

exec "$PYTHON" -m jarvis.voice_cli