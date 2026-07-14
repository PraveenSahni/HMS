# GNU Health Module Dependency Map (Planning)

**Source:** Official features list + IST `activate_modules.sh` batching.  
**Note:** Exact Tryton `depends` graphs should be verified from installed `tryton.cfg` on the VM. This map is a **planning** view, not a dump of `ir.module.dependency`.

```mermaid
flowchart TB
  subgraph core [Core]
    health[health]
  end
  subgraph clinical [Clinical extensions]
    lab[health_lab]
    img[health_imaging]
    inp[health_inpatient]
    nurs[health_nursing]
    surg[health_surgery]
    icu[health_icu]
    ped[health_pediatrics]
    gyn[health_gyneco]
  end
  subgraph services [Services and stock]
    svc[health_services]
    svclab[health_services_lab]
    svcimg[health_services_imaging]
    stock[health_stock]
    stocki[health_stock_inpatient]
    stocks[health_stock_surgery]
  end
  subgraph tryton [Tryton enterprise]
    account[account / invoice]
    tstock[stock / stock_lot]
  end
  subgraph coding [Coding]
    icd10[health_icd10]
    icd11[health_icd11]
  end
  health --> lab
  health --> img
  health --> inp
  health --> nurs
  health --> surg
  health --> icu
  health --> ped
  health --> gyn
  health --> svc
  health --> stock
  health --> icd10
  health --> icd11
  lab --> svclab
  img --> svcimg
  svc --> svclab
  svc --> svcimg
  inp --> stocki
  surg --> stocks
  stock --> tstock
  svc --> account
```

## Activation order (IST script)

1. Tryton: `account`, `account_product`, `account_invoice`, `stock`, `stock_lot`  
2. Clinical core batch (see discovery doc)  
3. Remaining `health_*` not yet activated  

## Custom modules

None in `C:\HMS`. Future UAE/QA connectors should be **separate** Tryton modules or an external integration service — do not fork core `health` without a governance decision.
