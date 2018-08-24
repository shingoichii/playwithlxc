#! /usr/bin/env python3

import pylxd

client = pylxd.Client()
for c in client.containers.all():
    name = c.name
    print(name)
    for a in c.state().network['eth0']['addresses']:
        if a['family'] == 'inet':
            print(a['address'])
