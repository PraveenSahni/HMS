#!/usr/bin/env python3
from proteus import config, Model
config.set_trytond(database="gnuhealth", user="admin", config_file="/opt/gnuhealth/his-50/etc/trytond.conf")
HP = Model.get("gnuhealth.healthprofessional")
print("fields:", list(HP._fields.keys()))
