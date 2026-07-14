#!/usr/bin/env python3
from proteus import config, Model

config.set_trytond(
    database="gnuhealth",
    user="admin",
    config_file="/opt/gnuhealth/his-50/etc/trytond.conf",
)

Inst = Model.get("gnuhealth.institution")
Party = Model.get("party.party")

# Clean test - search by code only
existing = Inst.find([("code", "=", "IST")], limit=1)
print("Existing by code:", [r.id for r in existing])

if not existing:
    p = Party(name="IST Technologies LLC", code="IST-CO")
    p.save()
    print("Party id:", p.id)
    inst = Inst(party=p, code="IST", extra_info="Multi-specialty Clinic — Doha, Qatar")
    inst.save()
    print("Created institution id:", inst.id)
else:
    print("Institution already exists:", existing[0].id)
