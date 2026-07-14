#!/bin/bash
echo "=== processes ==="
pgrep -af 'activate_modules|retry_failed|trytond-admin' | grep -v 'bash -c' || echo none
echo "=== activate tail ==="
tail -30 /tmp/module_activate.log
echo "=== retry tail ==="
tail -20 /tmp/module_retry.log 2>/dev/null || echo '(no retry yet)'
echo "=== activated health ==="
sudo -u postgres psql -d gnuhealth -c "SELECT name, state FROM ir_module WHERE name LIKE 'health%' ORDER BY state, name;"
echo "=== trytond ==="
pgrep -af '/venv/bin/trytond' | grep -v admin | grep -v 'bash -c' || echo 'trytond not running'
