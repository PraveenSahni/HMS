#!/bin/bash
# Run on VM (gnuhealth-his-01) after: gcloud compute ssh gnuhealth-his-01 --project=isthealth --zone=me-central1-a

HIS=/opt/gnuhealth/his-50
CONF=$HIS/etc/trytond.conf

echo "=== 1. Is trytond listening on all interfaces? ==="
sudo ss -tlnp | grep 8000 || echo "NOT listening on 8000 - start server via ghcontrol"

echo ""
echo "=== 2. Local firewall (ufw) ==="
sudo ufw status 2>/dev/null || echo "ufw not installed"

echo ""
echo "=== 3. trytond.conf [web] section ==="
grep -A5 '\[web\]' "$CONF"

echo ""
echo "=== 4. SAO web client ==="
if grep -q '^root' "$CONF" 2>/dev/null; then
  ROOT=$(grep '^root' "$CONF" | awk '{print $3}')
  echo "root = $ROOT"
  [ -d "$ROOT/index.html" ] || [ -f "$ROOT/index.html" ] && echo "SAO index: OK" || echo "SAO index: MISSING"
else
  echo "NO 'root' in trytond.conf - SAO web client NOT configured (causes 405 in browser)"
fi

echo ""
echo "=== 5. Test local HTTP ==="
curl -s -o /dev/null -w "GET / -> HTTP %{http_code}\n" http://127.0.0.1:8000/ || echo "curl failed"

echo ""
echo "=== DONE ==="
echo "If external browser times out but local curl works:"
echo "  - GCP firewall must allow tcp:8000 to this VM"
echo "  - Run from Cloud Shell (not on VM):"
echo "    gcloud compute firewall-rules create allow-gnuhealth-8000 --project=isthealth --direction=INGRESS --priority=1000 --network=default --action=ALLOW --rules=tcp:8000 --source-ranges=0.0.0.0/0 --target-tags=gnuhealth-server"
echo "    gcloud compute instances add-tags gnuhealth-his-01 --project=isthealth --zone=me-central1-a --tags=gnuhealth-server"
