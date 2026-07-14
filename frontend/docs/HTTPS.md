# HTTPS / TLS — IST Health

## Status

| Item | Value |
|------|--------|
| Public IP | `34.18.116.146` |
| Primary hostname | **`health.irisstar.tech`** |
| Certificate | Self-signed until DNS A record + Let's Encrypt |
| HTTP | `http://34.18.116.146/` (temporary; dual-serve until LE) |
| HTTPS (IP) | `https://34.18.116.146/` (browser warns — self-signed) |
| HTTPS (host) | `https://health.irisstar.tech/` after DNS + certbot |
| HSTS | **Off** until Let's Encrypt succeeds |
| trytond | Bound to **`127.0.0.1:8000` only** (not public) |
| SAO | Prefer `https://health.irisstar.tech/sao/` (nginx proxy) |
| GCP firewall | `allow-gnuhealth-8000` should be deleted/restricted after `/sao/` verified |

Let’s Encrypt does **not** issue certificates for bare IPs. A DNS hostname is required for a trusted padlock.

## DNS (required for trusted HTTPS)

Create this record at **GoDaddy** (DNS for `irisstar.tech` is `ns41`/`ns42.domaincontrol.com`):

| Field | Value |
|-------|--------|
| Type | **A** |
| Name / host | **`health`** (FQDN `health.irisstar.tech`) |
| Value / points to | **`34.18.116.146`** |
| TTL | 300 (or provider default) |

Verify propagation:

```bash
nslookup health.irisstar.tech 8.8.8.8
# Expect: Address: 34.18.116.146
```

## Issue / renew Let's Encrypt (on the VM)

After the A record resolves to `34.18.116.146`:

```bash
gcloud compute ssh gnuhealth-his-01 --project=isthealth --zone=me-central1-a

sudo apt-get update && sudo apt-get install -y certbot python3-certbot-nginx
sudo certbot --nginx -d health.irisstar.tech --redirect
sudo nginx -t && sudo systemctl reload nginx
```

Certbot updates nginx `ssl_certificate` paths under `/etc/letsencrypt/live/health.irisstar.tech/`.

Then ensure HSTS is on in the `:443` block:

```nginx
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
```

Or re-run the helper (skips bind if already localhost, runs certbot when DNS is ready):

```bash
sudo SITE_HOST=health.irisstar.tech bash /path/to/harden-https-subdomain.sh
```

Renewal: `certbot renew` (systemd timer from the package).

## Final URLs (after DNS + LE)

| Purpose | URL |
|---------|-----|
| Login | https://health.irisstar.tech/login |
| App | https://health.irisstar.tech/ |
| Tryton API | https://health.irisstar.tech/api/tryton/ |
| SAO | https://health.irisstar.tech/sao/ |

Until DNS exists, use the IP temporarily (`http://34.18.116.146/`). Port **8000 must not** be reachable from the public internet.

## Nginx layout

- Live site: `/etc/nginx/sites-available/gnuhealth`
- Repo copies: `frontend/deploy/nginx-ist-health.conf`, `nginx-ist-health-vm.conf`
- Harden + LE helper: `frontend/deploy/harden-https-subdomain.sh`
- SPA root: `/var/www/ist-health/frontend/dist/`
- Proxy: `/api/tryton/` → `http://127.0.0.1:8000/`
- SAO: `/sao/` → `http://127.0.0.1:8000/`
- ACME webroot: `/var/www/letsencrypt/.well-known/acme-challenge/`

React JSON-RPC uses relative `/api/tryton/` when the proxy is enabled — **no mixed content** on HTTPS.

## trytond systemd

| Unit | `trytond.service` |
|------|-------------------|
| Start | `/opt/gnuhealth/his-50/start_gnuhealth` |
| Listen | `127.0.0.1:8000` in `/opt/gnuhealth/his-50/etc/trytond.conf` `[web]` |
| User | `sahni_ps` |
| Logs | `/opt/gnuhealth/his-50/log/trytond-systemd.log` |

```bash
sudo systemctl status trytond
sudo systemctl restart trytond
```

## Verify

```bash
# From your PC — :8000 must FAIL after harden
curl --connect-timeout 5 http://34.18.116.146:8000/   # expect timeout / connection refused

# SAO + app via nginx
curl -s -o /dev/null -w "%{http_code}\n" http://34.18.116.146/sao/
curl -s -o /dev/null -w "%{http_code}\n" http://34.18.116.146/login

# After DNS + LE
curl -s -o /dev/null -w "%{http_code}\n" https://health.irisstar.tech/login
curl -s -X POST https://health.irisstar.tech/api/tryton/ \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"common.db.list","params":[]}'
```

## Close public :8000 (GCP)

After confirming `/sao/` works for operators:

```bash
gcloud compute firewall-rules delete allow-gnuhealth-8000 --project=isthealth --quiet
# Or restrict sourceRanges instead of 0.0.0.0/0
```
