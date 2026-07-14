#!/bin/bash
# Install Tryton 7 SAO web client for GNU Health 5 - run on VM as sahni_ps

set -e
HIS=/opt/gnuhealth/his-50
SAO_DIR=$HIS/sao
CONF=$HIS/etc/trytond.conf

echo "=== Installing SAO web client (Tryton 7.x) ==="
sudo apt-get update -qq
sudo apt-get install -y nodejs npm curl

mkdir -p "$SAO_DIR"
cd /tmp
curl -fsSL -o tryton-sao.tgz "http://downloads.tryton.org/7.0/tryton-sao-last.tgz"
tar -xzf tryton-sao.tgz --strip-components=1 -C "$SAO_DIR"

cd "$SAO_DIR"
npm install --production --legacy-peer-deps

# Add root to trytond.conf if missing
if ! grep -q '^root' "$CONF"; then
  sudo sed -i "/^\[web\]/a root = $SAO_DIR" "$CONF"
else
  sudo sed -i "s|^root = .*|root = $SAO_DIR|" "$CONF"
fi

echo ""
echo "=== Updated [web] section ==="
grep -A6 '\[web\]' "$CONF"

echo ""
echo "=== Restart GNU Health server ==="
echo "Run: ghcontrol -> Stop Server -> Start GNU Health HIS"
echo "Or: pkill trytond; cd $HIS && ./start_gnuhealth &"
echo ""
echo "Then open: http://34.18.116.146:8000"
