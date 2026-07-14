#!/usr/bin/env python3
from proteus import config, Model

config.set_trytond(
    database="gnuhealth",
    user="admin",
    config_file="/opt/gnuhealth/his-50/etc/trytond.conf",
)

Type = Model.get("gnuhealth.institution.type")
types = Type.find([], limit=20)
print("Institution types:")
for t in types:
    print(f"  id={t.id} code={getattr(t,'code','?')} name={getattr(t,'name','?')}")

Inst = Model.get("gnuhealth.institution")
Party = Model.get("party.party")

existing = Inst.find([("code", "=", "IST")], limit=1)
if existing:
    print("Already exists:", existing[0].id)
else:
    type_id = types[0].id if types else None
    print("Using type_id:", type_id)
    p = Party(name="IST Technologies LLC", code="IST-CO")
    p.save()
    vals = {"party": p.id, "code": "IST", "extra_info": "Multi-specialty Clinic"}
    if type_id:
        vals["institution_type"] = type_id
    inst = Inst(**vals)
    inst.save()
    print("Created institution id:", inst.id)
