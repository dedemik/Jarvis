#!/bin/sh
set -eu

PROJECT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$PROJECT_DIR"

if ! command -v python3 >/dev/null 2>&1; then
    printf '%s\n' "Hata: Python 3 bulunamadı. Python 3.10 veya üzerini yükle." >&2
    exit 1
fi

if ! python3 -c 'import sys; raise SystemExit(sys.version_info < (3, 10))'; then
    printf '%s\n' "Hata: Jarvis için Python 3.10 veya üzeri gerekiyor." >&2
    exit 1
fi

if [ ! -x .venv/bin/python ]; then
    python3 -m venv .venv
fi

.venv/bin/python -m pip install -r requirements.txt
printf '%s\n' "Kurulum tamamlandı. Jarvis'i başlatmak için ./run.sh çalıştır."
