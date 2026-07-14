#!/bin/bash
# Paste entire script on VM: bash fix-gnuhealth-access.sh
set -e
HIS=/opt/gnuhealth/his-50
CONF=$HIS/etc/trytond.conf
SAO=$HIS/sao

echo "========== DIAGNOSTIC =========="
echo "--- Processes ---"
ps aux | grep -E '[t]rytond|[g]nuhealth' || echo "trytond NOT running"
echo "--- Ports ---"
sudo ss -tlnp | grep -E ':8000|:80 ' || true
echo "--- trytond.conf [web] ---"
grep -A10 '\[web\]' "$CONF" || true
echo "--- SAO ---"
[ -f "$SAO/index.html" ] && echo "SAO index.html OK" || echo "SAO index.html MISSING at $SAO"
curl -s -o /dev/null -w "Local GET /8000 -> HTTP %{http_code}\n" http://127.0.0.1:8000/ || echo "curl failed"
echo "--- External IP ---"
EXT_IP=$(curl -s -H "Metadata-Flavor: Google" http://metadata.google.internal/computeMetadata/v1/instance/networkInterfaces/0/accessConfigs/0/external-ip)
echo "$EXT_IP"
echo "--- VM tags ---"
curl -s -H "Metadata-Flavor: Google" http://metadata.google.internal/computeMetadata/v1/instance/tags
echo ""

echo "========== FIX 1: Ensure SAO root in trytond.conf =========="
if [ ! -f "$SAO/index.html" ]; then
  echo "Installing SAO..."
  sudo apt-get update -qq
  sudo apt-get install -y nodejs npm curl
  mkdir -p "$SAO"
  cd /tmp
  curl -fsSL -o tryton-sao.tgz "http://downloads.tryton.org/7.0/tryton-sao-last.tgz"
  tar -xzf tryton-sao.tgz --strip-components=1 -C "$SAO"
  cd "$SAO"
  npm install --production --legacy-peer-deps
fi

# Ensure listen on all interfaces and root set
sudo sed -i 's|^listen = .*|listen = 0.0.0.0:8000|' "$CONF"
if grep -q '^root' "$CONF"; then
  sudo sed -i "s|^root = .*|root = $SAO|" "$CONF"
else
  sudo sed -i "/^\[web\]/a root = $SAO" "$CONF"
fi
echo "Updated config:"
grep -A8 '\[web\]' "$CONF"

echo ""
echo "========== FIX 2: Nginx reverse proxy on port 80 =========="
sudo tee /etc/nginx/sites-available/gnuhealth >/dev/null <<NGINX
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name _;
    client_max_body_size 50m;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_read_timeout 300s;
    }
}
NGINX
sudo ln -sf /etc/nginx/sites-available/gnuhealth /etc/nginx/sites-enabled/gnuhealth
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t && sudo systemctl reload nginx
echo "Nginx proxy: OK"

echo ""
echo "========== FIX 3: Restart trytond =========="
pkill -f trytond 2>/dev/null || true
sleep 2
cd "$HIS"
nohup ./start_gnuhealth > /tmp/trytond.log 2>&1 &
sleep 5
ps aux | grep '[t]rytond' && echo "trytond started" || echo "trytond FAILED - check /tmp/trytond.log"

echo ""
echo "========== FINAL TEST =========="
curl -s -o /dev/null -w "Local :8000 -> HTTP %{http_code}\n" http://127.0.0.1:8000/
curl -s -o /dev/null -w "Local :80   -> HTTP %{http_code}\n" http://127.0.0.1:80/
curl -s http://127.0.0.1:80/ | head -2

echo ""
echo "=========================================="
echo "Try these URLs in your browser:"
echo "  http://${EXT_IP}"
echo "  http://${EXT_IP}:8000"
echo ""
echo "Login: admin / your password"
echo "=========================================="
echo ""
echo "If :80 works but :8000 times out, firewall blocks 8000 only."
echo "Run in Cloud Shell (one line):"
echo "gcloud compute firewall-rules create allow-gnuhealth-8000 --project=isthealth --direction=INGRESS --priority=1000 --network=default --action=ALLOW --rules=tcp:8000 --source-ranges=0.0.0.0/0 2>/dev/null || gcloud compute firewall-rules update allow-gnuhealth-8000 --project=isthealth --allow=tcp:8000 --source-ranges=0.0.0.0/0"
