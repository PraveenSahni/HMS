#!/bin/bash
echo "=== activate log ==="
tail -25 /tmp/module_activate.log
echo "=== retry log ==="
tail -15 /tmp/module_retry.log 2>/dev/null || echo '(retry waiting)'
echo "=== processes ==="
pgrep -af 'activate_modules|retry_failed|trytond-admin' | grep -v 'bash -c' || echo none
echo "=== counts ==="
sudo -u postgres psql -d gnuhealth -c "SELECT state, count(1) FROM ir_module GROUP BY state ORDER BY 1;"
sudo -u postgres psql -d gnuhealth -c "SELECT name FROM ir_module WHERE state='activated' AND name LIKE 'health%' ORDER BY 1;"
