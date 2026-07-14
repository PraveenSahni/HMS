#!/bin/bash
grep -r -i password /opt/gnuhealth/his-50/*.sh /opt/gnuhealth/his-50/start* /home/*/.bash_history 2>/dev/null | head -20
grep -r -i password /opt/gnuhealth/ 2>/dev/null | grep -v venv | grep -v '.pyc' | head -20
cat /opt/gnuhealth/his-50/start_gnuhealth 2>/dev/null
ls -la /opt/gnuhealth/his-50/
