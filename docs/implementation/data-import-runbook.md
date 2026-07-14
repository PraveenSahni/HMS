# Data Import Runbook

## Preconditions

- Target environment classified (dev/test/uat/prod)
- Master data workbook validated
- Backup taken for shared environments
- For prod: CAB approval + `--allow-production`

## Commands

```bash
# Validate master data Excel
python scripts/implementation/validate_master_data.py templates/Healthcare_Implementation_Master_Data.xlsx

# Validate synthetic config
python scripts/synthetic_data/cli.py validate --config config/synthetic/uae_qatar_demo.yaml

# Dry-run import (no writes)
python scripts/synthetic_data/cli.py import_data --config config/synthetic/uae_qatar_demo.yaml --dry-run

# Generate synthetic dataset (local files / report)
python scripts/synthetic_data/cli.py generate_synthetic --config config/synthetic/uae_qatar_demo.yaml

# Import synthetic into GNU Health (non-prod)
python scripts/synthetic_data/cli.py import_synthetic --config config/synthetic/uae_qatar_demo.yaml

# Legacy engine (existing)
python run_synthetic_data.py --config config.yaml --dry-run
```

## Rollback

1. Stop imports.  
2. Restore PostgreSQL backup taken pre-import.  
3. Or delete by synthetic code prefix (`IST-P-*`, comments containing `IST synthetic`) — only if documented and tested.  
4. Record incident in import report under `docs/testing/`.

## Refuse production

CLI exits non-zero if `environment: production` (or server URL matches prod host) unless `--allow-production` is passed.
