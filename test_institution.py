#!/usr/bin/env python3
from proteus import config, Model

config.set_trytond(
    database="gnuhealth",
    user="admin",
    config_file="/opt/gnuhealth/his-50/etc/trytond.conf",
)

Inst = Model.get("gnuhealth.institution")
rec = Inst()
print("Institution fields:", [f for f in dir(rec) if not f.startswith("_")][:30])
# Try to get _fields
try:
    print("Model info:", Inst._fields.keys() if hasattr(Inst, "_fields") else "no _fields")
except Exception as e:
    print("fields error:", e)

# List existing
recs = Inst.find([], limit=5)
print("Existing count:", len(recs))
for r in recs:
    print(" id=", r.id, "code=", getattr(r, "code", "?"))
