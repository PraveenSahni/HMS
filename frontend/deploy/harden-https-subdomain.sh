#!/usr/bin/env bash
# Harden trytond (localhost-only) + prepare nginx for subdomain + attempt Let's Encrypt.
# Target host: health.irisstar.tech (override with SITE_HOST=...)
# Do NOT use OS HOSTNAME env; use SITE_HOST (default health.irisstar.tech).
set -euo pipefail

SITE_HOST="${SITE_HOST:-health.irisstar.tech}"
PUBLIC_IP="${PUBLIC_IP:-34.18.116.146}"
CONF_TRYTON="/opt/gnuhealth/his-50/etc/trytond.conf"
NGINX_SITE="/etc/nginx/sites-available/gnuhealth"
SSL_DIR="/etc/nginx/ssl/ist-health"
ACME_ROOT="/var/www/letsencrypt"
LE_LIVE="/etc/letsencrypt/live/${SITE_HOST}"

echo "==> Site host: $SITE_HOST  IP: $PUBLIC_IP"

echo "==> 1. Bind trytond to 127.0.0.1:8000"
if grep -qE '^listen\s*=' "$CONF_TRYTON"; then
  sudo sed -i 's|^listen\s*=.*|listen = 127.0.0.1:8000|' "$CONF_TRYTON"
else
  # Ensure [web] has listen
  if grep -q '^\[web\]' "$CONF_TRYTON"; then
    sudo sed -i '/^\[web\]/a listen = 127.0.0.1:8000' "$CONF_TRYTON"
  else
    printf '\n[web]\nlisten = 127.0.0.1:8000\n' | sudo tee -a "$CONF_TRYTON" >/dev/null
  fi
fi
grep -A5 '^\[web\]' "$CONF_TRYTON" | head -10

echo "==> Restart trytond"
sudo systemctl restart trytond
sleep 4
sudo systemctl is-active trytond
sudo ss -tlnp | grep ':8000' || true
# Must be localhost only
if sudo ss -tlnp | grep -E '0\.0\.0\.0:8000|:::8000'; then
  echo "ERROR: trytond still listening on public interfaces" >&2
  sudo ss -tlnp | grep 8000 || true
  exit 1
fi
curl -s -o /dev/null -w "local_trytond=%{http_code}\n" http://127.0.0.1:8000/ || true

echo "==> 2. Detect existing Let's Encrypt cert"
USE_LE=0
if [[ -f "$LE_LIVE/fullchain.pem" && -f "$LE_LIVE/privkey.pem" ]]; then
  USE_LE=1
  echo "    Found LE cert at $LE_LIVE"
else
  echo "    No LE cert yet — using self-signed until DNS + certbot succeed"
  sudo mkdir -p "$SSL_DIR"
  if [[ ! -f "$SSL_DIR/fullchain.pem" || ! -f "$SSL_DIR/privkey.pem" ]]; then
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
CN = $SITE_HOST
[v3_req]
subjectAltName = @alt_names
basicConstraints = CA:FALSE
keyUsage = digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth
[alt_names]
DNS.1 = $SITE_HOST
IP.1 = $PUBLIC_IP
DNS.2 = localhost
EOF
    sudo openssl req -x509 -nodes -newkey rsa:2048 -days 825 \
      -keyout "$SSL_DIR/privkey.pem" \
      -out "$SSL_DIR/fullchain.pem" \
      -config "$TMPCFG"
    rm -f "$TMPCFG"
    sudo chmod 640 "$SSL_DIR/privkey.pem"
    sudo chmod 644 "$SSL_DIR/fullchain.pem"
    sudo chown root:www-data "$SSL_DIR/privkey.pem" "$SSL_DIR/fullchain.pem" 2>/dev/null || true
  fi
fi

sudo mkdir -p "$ACME_ROOT/.well-known/acme-challenge"
sudo chown -R www-data:www-data "$ACME_ROOT" 2>/dev/null || true

if [[ "$USE_LE" -eq 1 ]]; then
  CERT_PATH="$LE_LIVE/fullchain.pem"
  KEY_PATH="$LE_LIVE/privkey.pem"
  HSTS_LINE='    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;'
  HTTP_BODY=$(cat <<'EOF'
    # ACME http-01
    location ^~ /.well-known/acme-challenge/ {
        root /var/www/letsencrypt;
        default_type "text/plain";
    }
    location / {
        return 301 https://$host$request_uri;
    }
EOF
)
else
  CERT_PATH="$SSL_DIR/fullchain.pem"
  KEY_PATH="$SSL_DIR/privkey.pem"
  HSTS_LINE='    # HSTS off until Let'\''s Encrypt succeeds'
  HTTP_BODY=$(cat <<'EOF'
    # ACME http-01 (ready for certbot)
    location ^~ /.well-known/acme-challenge/ {
        root /var/www/letsencrypt;
        default_type "text/plain";
    }

    # Dual-serve on :80 until LE + HSTS redirect (IP still usable)
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
    location /sao/ {
        proxy_pass http://127.0.0.1:8000/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 300s;
    }
    location /legal/ { try_files $uri $uri/ =404; }
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
EOF
)
fi

echo "==> 3. Write nginx config (server_name=$SITE_HOST)"
sudo tee "$NGINX_SITE" >/dev/null << NGINX
# IST Health — hardened + subdomain-ready
# Primary host: ${SITE_HOST}
# Generated by harden-https-subdomain.sh

server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name ${SITE_HOST} ${PUBLIC_IP} _;
    client_max_body_size 50m;

    root /var/www/ist-health/frontend/dist;
    index index.html;

${HTTP_BODY}
}

server {
    listen 443 ssl default_server;
    listen [::]:443 ssl default_server;
    server_name ${SITE_HOST} ${PUBLIC_IP} _;
    client_max_body_size 50m;

    ssl_certificate     ${CERT_PATH};
    ssl_certificate_key ${KEY_PATH};
    ssl_protocols       TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers off;
    ssl_session_cache   shared:SSL:10m;
    ssl_session_timeout 1d;

${HSTS_LINE}

    root /var/www/ist-health/frontend/dist;
    index index.html;

    location /api/tryton/ {
        proxy_pass http://127.0.0.1:8000/;
        proxy_http_version 1.1;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_read_timeout 120s;
    }

    location /gnuhealth/ {
        proxy_pass http://127.0.0.1:8000/gnuhealth/;
        proxy_http_version 1.1;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_read_timeout 300s;
    }

    location /sao/ {
        proxy_pass http://127.0.0.1:8000/;
        proxy_http_version 1.1;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_read_timeout 300s;
    }

    location /legal/ { try_files \$uri \$uri/ =404; }
    location /styles/ {
        try_files \$uri =404;
        add_header Cache-Control "public, max-age=86400";
    }
    location /assets/ {
        try_files \$uri =404;
        add_header Cache-Control "public, max-age=86400";
    }
    location / {
        try_files \$uri \$uri/ /index.html;
    }
}
NGINX

sudo nginx -t
sudo systemctl reload nginx

echo "==> 4. Verify /sao/ and API via nginx (localhost)"
curl -s -o /dev/null -w "sao=%{http_code}\n" http://127.0.0.1/sao/
curl -s -X POST http://127.0.0.1/api/tryton/ \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"common.db.list","params":[]}' | head -c 200
echo
curl -sk -o /dev/null -w "https_root=%{http_code}\n" "https://127.0.0.1/" -H "Host: ${SITE_HOST}"

echo "==> 5. Install certbot if needed"
if ! command -v certbot >/dev/null 2>&1; then
  sudo apt-get update -qq
  sudo apt-get install -y certbot python3-certbot-nginx
fi

echo "==> 6. DNS check for $SITE_HOST → $PUBLIC_IP"
RESOLVED="$(getent ahostsv4 "$SITE_HOST" 2>/dev/null | awk '{print $1; exit}' || true)"
echo "    Resolved: ${RESOLVED:-<none>}"
LE_STATUS="waiting_on_dns"
if [[ "$RESOLVED" == "$PUBLIC_IP" ]]; then
  echo "==> DNS OK — attempting certbot --nginx -d $SITE_HOST"
  if sudo certbot --nginx -d "$SITE_HOST" --non-interactive --agree-tos \
      --register-unsafely-without-email --redirect; then
    LE_STATUS="success"
    # Ensure HSTS after certbot
    if ! grep -q 'Strict-Transport-Security' "$NGINX_SITE"; then
      sudo sed -i '/ssl_session_timeout/a\    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;' "$NGINX_SITE"
      sudo nginx -t && sudo systemctl reload nginx
    fi
  else
    LE_STATUS="certbot_failed"
    echo "WARNING: certbot failed even though DNS resolved. Nginx left ready." >&2
  fi
else
  echo "WARNING: DNS for $SITE_HOST does not point to $PUBLIC_IP (got '${RESOLVED:-none}')."
  echo "         Skipping certbot. Create this A record, wait for propagation, then run:"
  echo "           sudo certbot --nginx -d $SITE_HOST --redirect"
  echo "         Then enable HSTS if not already present."
fi

echo "==> 7. Summary"
echo "SITE_HOST=$SITE_HOST"
echo "LE_STATUS=$LE_STATUS"
echo "TRYTOND_BIND=$(sudo ss -tlnp | grep 8000 || echo none)"
echo "SAO_PROXY=http(s)://$SITE_HOST/sao/ (and via IP until DNS ready)"
cat << EOF

DNS step (required for trusted HTTPS):
  Type: A
  Name: health   (or FQDN $SITE_HOST)
  Value: $PUBLIC_IP
  TTL: 300 (or default)

After DNS propagates on this VM:
  sudo certbot --nginx -d $SITE_HOST --redirect
  sudo nginx -t && sudo systemctl reload nginx
EOF
