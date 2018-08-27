#! /usr/bin/env python3
# wait for a container to get ready

import sys
import time
import pylxd

if len(sys.argv) < 2:
    exit(1)

container_name = sys.argv[1]

client = pylxd.Client()
while True:
    for c in client.containers.all():
        if c.name == container_name:
            sys.exit(0)
    time.sleep(1)
