#!/usr/bin/env bash
set -eu

sudo rm -rf /tmp/frontend-dist-new
sudo mkdir -p /tmp/frontend-dist-new
sudo tar -xzf /tmp/frontend-dist.tgz -C /tmp/frontend-dist-new
sudo mkdir -p /var/www/ist-health/frontend/dist
sudo find /var/www/ist-health/frontend/dist -mindepth 1 -delete
sudo cp -a /tmp/frontend-dist-new/. /var/www/ist-health/frontend/dist/

SAO_ROOT=/opt/gnuhealth/his-50/sao
if [ -f /opt/gnuhealth/his-50/trytond.conf ]; then
  CONF_ROOT=$(grep -E '^\s*root\s*=' /opt/gnuhealth/his-50/trytond.conf | head -1 | cut -d= -f2- | tr -d '[:space:]' || true)
  if [ -n "${CONF_ROOT:-}" ] && [ -d "$CONF_ROOT" ]; then
    SAO_ROOT="$CONF_ROOT"
  fi
fi
echo "SAO_ROOT=$SAO_ROOT"

sudo cp /tmp/sao-custom.css "$SAO_ROOT/custom.css"
sudo cp /tmp/sao-custom.js "$SAO_ROOT/custom.js"
sudo chown gnuhealth:gnuhealth "$SAO_ROOT/custom.css" "$SAO_ROOT/custom.js" 2>/dev/null || true

echo "=== frontend assets ==="
ls -la /var/www/ist-health/frontend/dist/assets/ | head -20
grep -oE 'assets/[^"]+' /var/www/ist-health/frontend/dist/index.html || true

echo "=== custom.css embedded hide ==="
grep -n 'ist-embedded' "$SAO_ROOT/custom.css" | head -20

echo "=== sizes ==="
wc -c "$SAO_ROOT/custom.css" "$SAO_ROOT/custom.js"
echo "DEPLOY_OK"