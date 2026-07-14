#!/usr/bin/env python3
from proteus import config, Model

config.set_trytond(
    database="gnuhealth",
    user="admin",
    config_file="/opt/gnuhealth/his-50/etc/trytond.conf",
)

Inst = Model.get("gnuhealth.institution")
code, name = "IST", "IST Technologies LLC"

for label, domain in [
    ("simple code", [("code", "=", code)]),
    ("simple name", [("name", "=", name)]),
    ("or tuples", ["|", ("code", "=", code), ("name", "=", name)]),
    ("or lists", ["|", ["code", "=", code], ["name", "=", name]]),
]:
    try:
        recs = Inst.find(domain, limit=1)
        print(f"{label}: OK -> {[r.id for r in recs]}")
    except Exception as e:
        print(f"{label}: FAIL -> {type(e).__name__}: {e}")
