#!/usr/bin/env python3
from proteus import config, Model

config.set_trytond(
    database="gnuhealth",
    user="admin",
    config_file="/opt/gnuhealth/his-50/etc/trytond.conf",
)

Party = Model.get("party.party")
code = "IST-ST-DOC-0001"
recs = Party.find([("code", "=", code)], limit=1)
print(f"find code={code!r} -> {[r.id for r in recs]}")
recs2 = Party.find([("code", "like", "IST-ST-%")], limit=10)
print(f"like IST-ST-% -> {[(r.id, r.code) for r in recs2]}")
