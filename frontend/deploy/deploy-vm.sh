#!/usr/bin/env bash
# IST Health frontend — build and deploy to VM (run on server or via ssh)
set -euo pipefail

APP_DIR="${APP_DIR:-/var/www/ist-health/frontend}"
REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

echo "==> Sync design assets"
powershell.exe -File "$REPO_ROOT/frontend/scripts/sync-design.ps1" 2>/dev/null || \
  cp -r "$REPO_ROOT/design/styles/"* "$REPO_ROOT/frontend/src/styles/" && \
  mkdir -p "$REPO_ROOT/frontend/public/styles" && \
  cp -r "$REPO_ROOT/design/styles/"* "$REPO_ROOT/frontend/public/styles/"

cd "$REPO_ROOT/frontend"
echo "==> npm install"
npm ci
echo "==> npm run build"
npm run build

echo "==> Deploy dist to $APP_DIR"
sudo mkdir -p "$APP_DIR"
sudo rsync -av --delete dist/ "$APP_DIR/dist/"
sudo rsync -av public/styles/ "$APP_DIR/dist/styles/"
sudo rsync -av public/legal/ "$APP_DIR/dist/legal/"

echo "==> Done. Configure nginx with deploy/nginx-ist-health.conf"
echo "    Ensure VITE_USE_PROXY=true in production build (.env.production)"
