#!/usr/bin/env bash
set -euo pipefail

if [ $# -gt 0 ]; then
  exec "$@"
fi

cd /app/tag-governance-app
exec npm run dev -- --host 0.0.0.0 --port "${VITE_PORT:-5173}"
