#!/usr/bin/env bash
# Deploy synthetic data engine to GNU Health VM and run it
set -e

PROJECT=isthealth
ZONE=me-central1-a
VM=gnuhealth-his-01
REMOTE_DIR=/opt/gnuhealth/synthetic-data

echo "=== Deploying to $VM ==="
gcloud compute ssh "$VM" --project="$PROJECT" --zone="$ZONE" --command="mkdir -p $REMOTE_DIR"

# Copy files
gcloud compute scp --project="$PROJECT" --zone="$ZONE" \
  config.yaml requirements.txt run_synthetic_data.py \
  "$VM:$REMOTE_DIR/"

gcloud compute scp --project="$PROJECT" --zone="$ZONE" --recurse \
  synthetic_data \
  "$VM:$REMOTE_DIR/"

echo "=== Installing Python deps on VM ==="
gcloud compute ssh "$VM" --project="$PROJECT" --zone="$ZONE" --command="
  cd $REMOTE_DIR
  /opt/gnuhealth/his-50/venv/bin/pip install -q -r requirements.txt
"

echo "=== Dry-run connection test ==="
gcloud compute ssh "$VM" --project="$PROJECT" --zone="$ZONE" --command="
  cd $REMOTE_DIR
  /opt/gnuhealth/his-50/venv/bin/python run_synthetic_data.py --dry-run
"

echo ""
echo "=== To generate data, run: ==="
echo "gcloud compute ssh $VM --project=$PROJECT --zone=$ZONE --command=\"cd $REMOTE_DIR && /opt/gnuhealth/his-50/venv/bin/python run_synthetic_data.py\""
echo ""
read -r -p "Run full synthetic data generation now? [y/N] " answer
if [[ "$answer" =~ ^[Yy]$ ]]; then
  gcloud compute ssh "$VM" --project="$PROJECT" --zone="$ZONE" --command="
    cd $REMOTE_DIR
    nohup /opt/gnuhealth/his-50/venv/bin/python run_synthetic_data.py > synthetic_run.log 2>&1 &
    echo 'Started in background. Tail log with:'
    echo '  tail -f $REMOTE_DIR/synthetic_run.log'
  "
fi
