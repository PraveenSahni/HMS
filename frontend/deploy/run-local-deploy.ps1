$ErrorActionPreference = "Stop"
$log = "c:\HMS\frontend\deploy-scp.log"
"" | Set-Content $log
function L($m) { Add-Content $log $m; Write-Host $m }

L "START $(Get-Date -Format o)"
$tar = "c:\HMS\frontend\dist-deploy.tgz"
if (Test-Path $tar) { Remove-Item $tar -Force }
if (-not (Test-Path "c:\HMS\frontend\dist\index.html")) { throw "dist missing — run npm run build first" }

tar -czf $tar -C c:\HMS\frontend\dist .
L "TAR_SIZE=$((Get-Item $tar).Length)"

$saoCss = "c:\HMS\frontend\deploy\sao-custom.css"
$saoJs = "c:\HMS\frontend\deploy\sao-custom.js"
$deploySh = "c:\HMS\frontend\deploy\deploy-workspace-simple.sh"
if (-not (Test-Path $saoCss)) { throw "missing $saoCss" }
if (-not (Test-Path $saoJs)) { throw "missing $saoJs" }
if (-not (Test-Path $deploySh)) { throw "missing $deploySh" }

gcloud compute scp --project=isthealth --zone=me-central1-a $tar "gnuhealth-his-01:/tmp/frontend-dist.tgz"
if ($LASTEXITCODE -ne 0) { throw "scp dist failed: $LASTEXITCODE" }
L "SCP_DIST_OK"

gcloud compute scp --project=isthealth --zone=me-central1-a $saoCss "gnuhealth-his-01:/tmp/sao-custom.css"
if ($LASTEXITCODE -ne 0) { throw "scp sao-custom.css failed: $LASTEXITCODE" }
L "SCP_SAO_CSS_OK"

gcloud compute scp --project=isthealth --zone=me-central1-a $saoJs "gnuhealth-his-01:/tmp/sao-custom.js"
if ($LASTEXITCODE -ne 0) { throw "scp sao-custom.js failed: $LASTEXITCODE" }
L "SCP_SAO_JS_OK"

gcloud compute scp --project=isthealth --zone=me-central1-a $deploySh "gnuhealth-his-01:/tmp/deploy-workspace-simple.sh"
if ($LASTEXITCODE -ne 0) { throw "scp deploy script failed: $LASTEXITCODE" }
L "SCP_SCRIPT_OK"

gcloud compute ssh gnuhealth-his-01 --project=isthealth --zone=me-central1-a --command="bash /tmp/deploy-workspace-simple.sh"
if ($LASTEXITCODE -ne 0) { throw "remote deploy failed: $LASTEXITCODE" }
L "SSH_EXIT=0"
L "END $(Get-Date -Format o)"
