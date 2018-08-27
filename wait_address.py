#! /usr/bin/env python3
# wait for assignment of an IP address to the container

import pylxd
import time
import sys

if len(sys.argv) < 2:
    exit(1)

container_name = sys.argv[1]

client = pylxd.Client()

# the following should work, but it generates an error (https://github.com/lxc/pylxd/issues/301)
#c = client.containers.get(container_name)
# inefficient workaround below instead
for c in client.containers.all():
    if c.name == container_name:
        break

container_address = ""
while container_address == "":
    time.sleep(1)
    for a in c.state().network['eth0']['addresses']:
        #print(a['family'])
        if a['family'] == 'inet':
            container_address = a['address']
            break

return container_address



 