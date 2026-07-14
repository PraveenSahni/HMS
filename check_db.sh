#!/bin/bash
sudo -u postgres psql gnuhealth -c "SELECT id, code, name FROM party_party WHERE code LIKE 'IST%' ORDER BY id LIMIT 20;"
