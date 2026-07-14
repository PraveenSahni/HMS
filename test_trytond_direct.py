#!/usr/bin/env python3
"""Quick test: Proteus set_trytond direct connection."""
from proteus import config, Model

config.set_trytond(
    database="gnuhealth",
    user="admin",
    config_file="/opt/gnuhealth/his-50/etc/trytond.conf",
)
User = Model.get("res.user")
users = User.find([("login", "=", "admin")])
print("Connected as admin, user id:", users[0].id if users else "NOT FOUND")

Party = Model.get("party.party")
count = len(Party.find([]))
print("Existing parties:", count)
