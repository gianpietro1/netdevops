#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import the required libraries
from napalm import get_network_driver
import sys

# Define the driver that will be used
driver = get_network_driver('iosxr')

hosts = [ 
   {'name':'R1','ip': '192.168.0.1'},
   {'name':'R2','ip': '192.168.0.2'},
   {'name':'R3','ip': '192.168.0.3'},
   {'name':'R4','ip': '192.168.0.4'},
]

for host in hosts:
    # Definimos y abrimos la conexión
    device = driver(hostname=host['ip'],
                    username='ws',
                    password='ws',
                   )
    device.open()

    print('Aplicando rollback en el equipo %s' % host['name'])
    device.rollback()

    device.close()

