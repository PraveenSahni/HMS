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
print("before find:", [r.id for r in recs])

try:
    result = Party._proxy.create([{"name": "Dr. Test One", "code": code}], {})
    print("create OK:", result)
except Exception as e:
    print("create FAIL:", type(e).__name__, e)

recs = Party.find([("code", "=", code)], limit=1)
print("after find:", [r.id for r in recs])
