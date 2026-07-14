#!/usr/bin/env python3
from proteus import config, Model
from trytond.transaction import Transaction
from trytond.pool import Pool

config.set_trytond(
    database="gnuhealth",
    user="admin",
    config_file="/opt/gnuhealth/his-50/etc/trytond.conf",
)

Inst = Model.get("gnuhealth.institution")
Party = Model.get("party.party")

pool = Pool("gnuhealth")
InstModel = pool.get("gnuhealth.institution")
pub_field = InstModel._fields["public_level"]
with Transaction().start("gnuhealth", 1):
    pub_sel = pub_field.selection
    if callable(pub_sel):
        pub_sel = pub_sel()
print("public_level options:", pub_sel)

existing = Inst.find([("code", "=", "IST")], limit=1)
if existing:
    print("Already exists id=", existing[0].id)
else:
    parties = Party.find([("code", "=", "IST-CO")], limit=1)
    p = parties[0]
    pub = pub_sel[1][0] if len(pub_sel) > 1 else pub_sel[0][0]
    inst = Inst(
        party=p,
        code="IST",
        institution_type="clinic",
        public_level=pub,
        extra_info="Multi-specialty Clinic — Doha, Qatar",
    )
    inst.save()
    print("Created institution id=", inst.id, "public_level=", pub)
