#!/bin/bash
echo "=== Config ==="
grep -E 'patients:|staff:|appointment_months:' /opt/gnuhealth/synthetic-data/config.yaml

echo ""
echo "=== Process ==="
ps aux | grep run_synthetic | grep -v grep || echo "No run_synthetic process (run completed)"

echo ""
echo "=== DB counts ==="
sudo -u postgres psql gnuhealth -c "
SELECT 'party_patients' AS metric, COUNT(*) FROM party_party WHERE code LIKE 'IST-P-%'
UNION ALL SELECT 'party_staff', COUNT(*) FROM party_party WHERE code LIKE 'IST-ST-%'
UNION ALL SELECT 'gnuhealth_patient', COUNT(*) FROM gnuhealth_patient
UNION ALL SELECT 'health_professional', COUNT(*) FROM gnuhealth_healthprofessional
UNION ALL SELECT 'appointments', COUNT(*) FROM gnuhealth_appointment
UNION ALL SELECT 'institution', COUNT(*) FROM gnuhealth_institution
UNION ALL SELECT 'product_meds', COUNT(*) FROM product_template WHERE code LIKE 'IST-MED-%';
"
