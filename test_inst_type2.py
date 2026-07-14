#!/usr/bin/env python3
from proteus import config, Model

config.set_trytond(
    database="gnuhealth",
    user="admin",
    config_file="/opt/gnuhealth/his-50/etc/trytond.conf",
)

Inst = Model.get("gnuhealth.institution")
Party = Model.get("party.party")

# Use existing party from failed test
parties = Party.find([("code", "=", "IST-CO")], limit=1)
print("Party:", parties[0].id if parties else "none")

# Query DB for institution_type column type
from trytond.transaction import Transaction
from trytond.pool import Pool
pool = Pool("gnuhealth")
InstModel = pool.get("gnuhealth.institution")
field = InstModel._fields.get("institution_type")
print("Field type:", type(field).__name__)
if hasattr(field, "selection"):
    print("Selection:", field.selection)

existing = Inst.find([("code", "=", "IST")], limit=1)
if existing:
    print("Institution exists:", existing[0].id)
else:
    p = parties[0] if parties else None
    if not p:
        p = Party(name="IST Technologies LLC", code="IST-CO2")
        p.save()
    
    # Get selection values from field
    sel = field.selection if hasattr(field, "selection") else []
    if callable(sel):
        with Transaction().start("gnuhealth", 1):
            sel = sel()
    print("Trying selections:", sel[:10] if sel else "none")
    
    for itype in (sel or [None]):
        val = itype[0] if isinstance(itype, (list, tuple)) else itype
        try:
            inst = Inst(party=p, code="IST", institution_type=val)
            inst.save()
            print("SUCCESS id=", inst.id, "type=", val)
            break
        except Exception as e:
            print(f"FAIL type={val}: {type(e).__name__}: {str(e)[:100]}")
