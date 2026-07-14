#!/bin/bash
set -e
mkdir -p /tmp/frontend-dist-new
sudo rsync -a --delete /tmp/frontend-dist-new/ /var/www/ist-health/frontend/dist/
echo "=== deployed assets ==="
ls -la /var/www/ist-health/frontend/dist/
ls /var/www/ist-health/frontend/dist/assets/
echo "=== index refs ==="
grep -oE 'assets/[^"]+' /var/www/ist-health/frontend/dist/index.html
