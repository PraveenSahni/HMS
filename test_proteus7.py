#!/usr/bin/env python3
"""Test Proteus 7 connection methods."""
from proteus import config, Model

PW = "IstHealth@2026!Admin"

# Method 1: set_trytond (direct connection to trytond)
try:
    config.set_trytond(
        database="gnuhealth",
        user="admin",
        password=PW,
        config_file="/opt/gnuhealth/his-50/etc/trytond.conf",
    )
    User = Model.get("res.user")
    users = User.find([("login", "=", "admin")])
    print("set_trytond OK:", users[0].id if users else "no user")
except Exception as e:
    print("set_trytond FAILED:", type(e).__name__, e)

# Method 2: set_xmlrpc
try:
    config.set_xmlrpc(
        "http://127.0.0.1:8000/",
        db="gnuhealth",
        user="admin",
        password=PW,
    )
    User = Model.get("res.user")
    users = User.find([("login", "=", "admin")])
    print("set_xmlrpc OK:", users[0].id if users else "no user")
except Exception as e:
    print("set_xmlrpc FAILED:", type(e).__name__, e)

# Method 3: set_xmlrpc_session
try:
    config.set_xmlrpc_session(
        "http://127.0.0.1:8000/",
        db="gnuhealth",
        user="admin",
        password=PW,
    )
    User = Model.get("res.user")
    users = User.find([("login", "=", "admin")])
    print("set_xmlrpc_session OK:", users[0].id if users else "no user")
except Exception as e:
    print("set_xmlrpc_session FAILED:", type(e).__name__, e)
