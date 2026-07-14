#!/usr/bin/env python3
from proteus import config, Model

config.set_trytond(
    database="gnuhealth",
    user="admin",
    config_file="/opt/gnuhealth/his-50/etc/trytond.conf",
)

Inst = Model.get("gnuhealth.institution")
rec = Inst()
# Check institution_type field descriptor
from proteus import FieldDescriptor
for fname in ["institution_type", "party", "code", "extra_info"]:
    desc = Inst._fields.get(fname)
    print(fname, "->", type(desc).__name__, getattr(desc, "selection", None))

# Try common selection values
Party = Model.get("party.party")
existing = Inst.find([("code", "=", "IST")], limit=1)
if not existing:
    p = Party(name="IST Technologies LLC", code="IST-CO")
    p.save()
    for itype in ["Hospital", "hospital", "Clinic", "clinic", "primary_care", "other"]:
        try:
            inst = Inst(party=p, code="IST", institution_type=itype, extra_info="Test")
            inst.save()
            print("SUCCESS with institution_type=", itype, "id=", inst.id)
            break
        except Exception as e:
            print(f"FAIL {itype}: {type(e).__name__}: {str(e)[:80]}")
else:
    print("Exists:", existing[0].id)
