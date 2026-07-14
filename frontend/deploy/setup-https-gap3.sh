#!/usr/bin/env bash
# Gap 3: HTTPS / production hardening for IST Health (self-signed on public IP)
set -euo pipefail

IP=34.18.116.146
SSL_DIR=/etc/nginx/ssl/ist-health
CONF=/etc/nginx/sites-available/gnuhealth
UNIT=/etc/systemd/system/trytond.service

echo "==> Creating SSL directory: $SSL_DIR"
mkdir -p "$SSL_DIR"

if [ ! -f "$SSL_DIR/fullchain.pem" ] || [ ! -f "$SSL_DIR/privkey.pem" ]; then
  echo "==> Generating self-signed cert for $IP (825 days)"
  # Use openssl.cnf SAN for older openssl without -addext reliability
  TMPCFG=$(mktemp)
  cat > "$TMPCFG" << EOF
[req]
default_bits = 2048
prompt = no
default_md = sha256
distinguished_name = dn
x509_extensions = v3_req

[dn]
C = AE
ST = Dubai
L = Dubai
O = IST Health
OU = HIS
CN = $IP

[v3_req]
subjectAltName = @alt_names
basicConstraints = CA:FALSE
keyUsage = digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth

[alt_names]
IP.1 = $IP
DNS.1 = localhost
EOF
  openssl req -x509 -nodes -newkey rsa:2048 -days 825 \
    -keyout "$SSL_DIR/privkey.pem" \
    -out "$SSL_DIR/fullchain.pem" \
    -config "$TMPCFG"
  rm -f "$TMPCFG"
  chmod 640 "$SSL_DIR/privkey.pem"
  chmod 644 "$SSL_DIR/fullchain.pem"
  if getent group www-data >/dev/null; then
    chown root:www-data "$SSL_DIR/privkey.pem" "$SSL_DIR/fullchain.pem"
  else
    chown root:root "$SSL_DIR/privkey.pem" "$SSL_DIR/fullchain.pem"
  fi
else
  echo "==> Cert already exists, keeping"
fi

ls -la "$SSL_DIR"
openssl x509 -in "$SSL_DIR/fullchain.pem" -noout -subject -dates -ext subjectAltName 2>/dev/null || \
  openssl x509 -in "$SSL_DIR/fullchain.pem" -noout -subject -dates

echo "==> Writing nginx config (HTTP + HTTPS dual listen; HSTS off)"
cat > "$CONF" << 'NGINX'
# IST Health — production nginx (React SPA + Tryton proxy + legacy SAO)
# HTTP :80 and HTTPS :443 (self-signed until custom domain + Let's Encrypt)
# Gap 3 — HTTPS hardening

server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name _;
    client_max_body_size 50m;

    root /var/www/ist-health/frontend/dist;
    index index.html;

    # Optional: after HTTPS verified, redirect HTTP→HTTPS by replacing this
    # server body with: return 301 https://$host$request_uri;

    location /api/tryton/ {
        proxy_pass http://127.0.0.1:8000/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 120s;
    }

    location /gnuhealth/ {
        proxy_pass http://127.0.0.1:8000/gnuhealth/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 300s;
    }

    location /legal/ {
        try_files $uri $uri/ =404;
    }

    location /styles/ {
        try_files $uri =404;
        add_header Cache-Control "public, max-age=86400";
    }

    location /assets/ {
        try_files $uri =404;
        add_header Cache-Control "public, max-age=86400";
    }

    location / {
        try_files $uri $uri/ /index.html;
    }
}

server {
    listen 443 ssl default_server;
    listen [::]:443 ssl default_server;
    server_name _;
    client_max_body_size 50m;

    ssl_certificate     /etc/nginx/ssl/ist-health/fullchain.pem;
    ssl_certificate_key /etc/nginx/ssl/ist-health/privkey.pem;
    ssl_protocols       TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers off;
    ssl_session_cache   shared:SSL:10m;
    ssl_session_timeout 1d;

    # HSTS OFF for self-signed (avoids sticky HTTPS with untrusted cert)
    # Enable after Let's Encrypt on a real domain:
    # add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    root /var/www/ist-health/frontend/dist;
    index index.html;

    location /api/tryton/ {
        proxy_pass http://127.0.0.1:8000/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 120s;
    }

    location /gnuhealth/ {
        proxy_pass http://127.0.0.1:8000/gnuhealth/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 300s;
    }

    location /legal/ {
        try_files $uri $uri/ =404;
    }

    location /styles/ {
        try_files $uri =404;
        add_header Cache-Control "public, max-age=86400";
    }

    location /assets/ {
        try_files $uri =404;
        add_header Cache-Control "public, max-age=86400";
    }

    location / {
        try_files $uri $uri/ /index.html;
    }
}
NGINX

ln -sf /etc/nginx/sites-available/gnuhealth /etc/nginx/sites-enabled/gnuhealth
rm -f /etc/nginx/sites-enabled/default

echo "==> Testing nginx"
/usr/sbin/nginx -t
systemctl reload nginx
echo "==> nginx reloaded OK"

echo "==> Installing trytond systemd unit"
cat > "$UNIT" << 'UNIT'
[Unit]
Description=GNU Health / Tryton Server (trytond)
After=network.target postgresql.service
Wants=postgresql.service

[Service]
Type=simple
User=sahni_ps
Group=sahni_ps
WorkingDirectory=/opt/gnuhealth/his-50
ExecStart=/opt/gnuhealth/his-50/start_gnuhealth
Restart=on-failure
RestartSec=5
KillMode=mixed
TimeoutStopSec=30
# Inherit PATH for ghis_env / venv
Environment=HOME=/home/sahni_ps
StandardOutput=append:/opt/gnuhealth/his-50/log/trytond-systemd.log
StandardError=append:/opt/gnuhealth/his-50/log/trytond-systemd.err.log

[Install]
WantedBy=multi-user.target
UNIT

# Stop nohup instance before enabling systemd (avoid port conflict)
echo "==> Stopping nohup trytond (if any)"
pkill -f '/opt/gnuhealth/his-50/venv/bin/trytond' || true
sleep 2

systemctl daemon-reload
systemctl enable trytond.service
systemctl restart trytond.service
sleep 3
systemctl --no-pager --full status trytond.service || true

echo "==> Listening ports"
ss -tlnp | grep -E ':80|:443|:8000' || true

echo "==> Local HTTPS smoke test"
curl -sk -o /dev/null -w "https_local_http_code=%{http_code}\n" https://127.0.0.1/ || true
curl -s -o /dev/null -w "http_local_http_code=%{http_code}\n" http://127.0.0.1/ || true

echo "==> Gap 3 setup complete"
