#!/bin/bash
echo "=== trytond-admin process ==="
ps -o pid,etime,pcpu,pmem,cmd -p 32302 2>/dev/null || echo 'pid gone'
echo "=== postgres activity ==="
sudo -u postgres psql -d gnuhealth -c "SELECT pid, state, wait_event_type, left(query,120) AS q FROM pg_stat_activity WHERE datname='gnuhealth' ORDER BY state;"
echo "=== log size / mtime ==="
ls -la /tmp/module_activate.log
wc -l /tmp/module_activate.log
echo "=== last log lines ==="
tail -5 /tmp/module_activate.log
# check if orthanc or something blocking - look at strace briefly? skip
echo "=== open files count ==="
ls /proc/32302/fd 2>/dev/null | wc -l
