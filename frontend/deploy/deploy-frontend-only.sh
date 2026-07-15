#!/usr/bin/env bash
set -eu

sudo rm -rf /tmp/frontend-dist-new
sudo mkdir -p /tmp/frontend-dist-new
sudo tar -xzf /tmp/frontend-dist.tgz -C /tmp/frontend-dist-new
sudo mkdir -p /var/www/ist-health/frontend/dist
sudo find /var/www/ist-health/frontend/dist -mindepth 1 -delete
sudo cp -a /tmp/frontend-dist-new/. /var/www/ist-health/frontend/dist/

echo "=== frontend assets ==="
ls -la /var/www/ist-health/frontend/dist/assets/ | head -20
grep -oE 'assets/[^"]+' /var/www/ist-health/frontend/dist/index.html || true
echo DEPLOY_OK