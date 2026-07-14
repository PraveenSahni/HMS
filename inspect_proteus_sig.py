#!/usr/bin/env python3
import inspect
from proteus import config
for name in ['set_trytond', 'set_xmlrpc', 'set_xmlrpc_session', 'get_config']:
    fn = getattr(config, name, None)
    if fn:
        print(name, inspect.signature(fn))
        print(inspect.getdoc(fn) or '')
        print('---')
