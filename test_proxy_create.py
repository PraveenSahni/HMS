#!/usr/bin/env python3
from proteus import config, Model

config.set_trytond(
    database="gnuhealth",
    user="admin",
    config_file="/opt/gnuhealth/his-50/etc/trytond.conf",
)

Inst = Model.get("gnuhealth.institution")
Party = Model.get("party.party")

# Ensure party is institution
parties = Party.find([("code", "=", "IST-CO")], limit=1)
p = parties[0]
p.is_institution = True
p.save()
print("Party id:", p.id, "is_institution:", p.is_institution)

existing = Inst.find([("code", "=", "IST")], limit=1)
if existing:
    print("Already exists:", existing[0].id)
else:
    vals = {
        "party": p.id,
        "code": "IST",
        "institution_type": "clinic",
        "public_level": "private",
        "extra_info": "Test",
    }
    result = Inst._proxy.create([vals], {})
    print("proxy.create result:", result)
