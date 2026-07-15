#!/usr/bin/env bash
# Deploy IST Health accounting uploader to gnuhealth-his-01 and run it.
set -euo pipefail

PROJECT="${PROJECT:-isthealth}"
ZONE="${ZONE:-me-central1-a}"
VM="${VM:-gnuhealth-his-01}"
REMOTE_DIR="${REMOTE_DIR:-/opt/gnuhealth/synthetic-data/accounting}"
MODE="${1:-dry-run}"  # dry-run | execute

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

echo "=== Deploy accounting scripts to $VM:$REMOTE_DIR (mode=$MODE) ==="
gcloud compute ssh "$VM" --project="$PROJECT" --zone="$ZONE" --command="mkdir -p $REMOTE_DIR"

gcloud compute scp --project="$PROJECT" --zone="$ZONE" \
  "$ROOT/scripts/accounting/assess_accounting.py" \
  "$ROOT/scripts/accounting/upload_ist_health_accounting.py" \
  "$VM:$REMOTE_DIR/"

CMD="export GNUHEALTH_TRYTOND_CONF=/opt/gnuhealth/his-50/etc/trytond.conf
cd $REMOTE_DIR
/opt/gnuhealth/his-50/venv/bin/python assess_accounting.py --database isthealth --json > assess_before.json
"
if [[ "$MODE" == "execute" ]]; then
  CMD+="/opt/gnuhealth/his-50/venv/bin/python upload_ist_health_accounting.py --execute --json-out upload_report.json -v
"
else
  CMD+="/opt/gnuhealth/his-50/venv/bin/python upload_ist_health_accounting.py --dry-run --json-out upload_report_dry.json -v
"
fi
CMD+="/opt/gnuhealth/his-50/venv/bin/python assess_accounting.py --database isthealth --json > assess_after.json
echo DONE
"

gcloud compute ssh "$VM" --project="$PROJECT" --zone="$ZONE" --command="$CMD"
echo "Reports on VM: $REMOTE_DIR/assess_*.json upload_report*.json"
