#!/bin/bash
set -e
echo "=== Installing GNU Health dependencies on Debian ==="
sudo DEBIAN_FRONTEND=noninteractive apt-get update -y
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y git curl wget build-essential python3 python3-pip python3-venv python3-dev libxml2-dev libxslt1-dev libssl-dev libffi-dev libpq-dev libjpeg-dev zlib1g-dev postgresql postgresql-contrib nginx libldap2-dev libsasl2-dev
sudo systemctl enable postgresql
sudo systemctl start postgresql
DB_PASS="$(openssl rand -base64 24 | tr -d '/+=' | cut -c1-24)"
sudo -u postgres psql -tc "SELECT 1 FROM pg_roles WHERE rolname='gnuhealth'" | grep -q 1 || sudo -u postgres psql -c "CREATE USER gnuhealth WITH PASSWORD '${DB_PASS}';"
sudo -u postgres psql -tc "SELECT 1 FROM pg_database WHERE datname='gnuhealth'" | grep -q 1 || sudo -u postgres psql -c "CREATE DATABASE gnuhealth OWNER gnuhealth;"
sudo -u postgres psql -c "ALTER USER gnuhealth CREATEDB;"
sudo mkdir -p /opt/gnuhealth
sudo chown "$USER":"$USER" /opt/gnuhealth
python3 -m venv /home/$USER/ghvenv
source /home/$USER/ghvenv/bin/activate
pip install --upgrade pip
pip install gnuhealth-control
echo "DB_USER=gnuhealth" | sudo tee /root/gnuhealth-db.env >/dev/null
echo "DB_PASS=${DB_PASS}" | sudo tee -a /root/gnuhealth-db.env >/dev/null
echo "DB_NAME=gnuhealth" | sudo tee -a /root/gnuhealth-db.env >/dev/null
sudo chmod 600 /root/gnuhealth-db.env
echo "=== Dependencies installed successfully ==="
echo "PostgreSQL credentials saved in /root/gnuhealth-db.env"
echo "Next: source ~/ghvenv/bin/activate && ghcontrol"
