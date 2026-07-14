#!/bin/bash
sudo -u postgres psql gnuhealth -c "SELECT id, code, name, active FROM party_party WHERE code LIKE 'IST-ST%' ORDER BY code;"
