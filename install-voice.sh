#!/bin/sh
set -eu

PROJECT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$PROJECT_DIR"

if [ ! -x .venv/bin/python ]; then
    ./install.sh
fi

if command -v pacman >/dev/null 2>&1; then
    missing_packages=""
    if ! pacman -Q portaudio >/dev/null 2>&1; then
        missing_packages="$missing_packages portaudio"
    fi
    if ! pacman -Q espeak-ng >/dev/null 2>&1; then
        missing_packages="$missing_packages espeak-ng"
    fi
    if [ -n "$missing_packages" ]; then
        printf '%s\n' "Eksik sistem paketleri:$missing_packages" >&2
        printf '%s\n' "Kurmak için: sudo pacman -S --needed$missing_packages" >&2
        exit 1
    fi
fi

.venv/bin/python -m pip install -r requirements-voice.txt
printf '%s\n' "Ses paketleri kuruldu. Başlatmak için ./run-voice.sh çalıştır."