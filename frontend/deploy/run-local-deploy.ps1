$ErrorActionPreference = "Stop"
$log = "c:\HMS\frontend\deploy-scp.log"
"" | Set-Content $log
function L($m) { Add-Content $log $m; Write-Host $m }

L "START $(Get-Date -Format o)"
$tar = "c:\HMS\frontend\dist-deploy.tgz"
if (Test-Path $tar) { Remove-Item $tar -Force }
if (-not (Test-Path "c:\HMS\frontend\dist\index.html")) { throw "dist missing" }

tar -czf $tar -C c:\HMS\frontend\dist .
L "TAR_SIZE=$((Get-Item $tar).Length)"

gcloud compute scp --project=isthealth --zone=me-central1-a $tar "gnuhealth-his-01:/tmp/frontend-dist.tgz"
if ($LASTEXITCODE -ne 0) { throw "scp dist failed: $LASTEXITCODE" }
L "SCP_DIST_OK"

gcloud compute scp --project=isthealth --zone=me-central1-a "c:\HMS\frontend\deploy\deploy-frontend-only.sh" "gnuhealth-his-01:/tmp/deploy-frontend-only.sh"
if ($LASTEXITCODE -ne 0) { throw "scp script failed: $LASTEXITCODE" }
L "SCP_SCRIPT_OK"

gcloud compute ssh gnuhealth-his-01 --project=isthealth --zone=me-central1-a --command="bash /tmp/deploy-frontend-only.sh"
if ($LASTEXITCODE -ne 0) { throw "remote deploy failed: $LASTEXITCODE" }
L "SSH_EXIT=0"
L "END $(Get-Date -Format o)"
