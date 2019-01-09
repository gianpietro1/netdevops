#!/usr/bin/env python
# Import the required libraries
from napalm import get_network_driver
import jinja2
import sys

# Define the driver that will be used
driver = get_network_driver('iosxr')

# Preparemos Jinja2 para poder cargar 
# nuestra plantilla desde el sistema de archivos local
templateLoader = jinja2.FileSystemLoader(searchpath="./")
templateEnv = jinja2.Environment(loader=templateLoader)
template = templateEnv.get_template(str(”nombre_del_archivo”))

# Las variables pueden venir desde un archivo, 
# por ahora definámoslas aquí mismo
## Variables R1
R1_LO0 = "1.1.1.1"
R1_GE0 = "10.10.10.1"
R1_GE1 = "10.10.10.13"
R1_GE2 = "10.10.10.9"
## Variables R2
R2_LO0 = "2.2.2.2"
R2_GE0 = "10.10.10.5"
R2_GE1 = "10.10.10.2"
## Variables R3
R3_LO0 = "3.3.3.3"
R3_GE0 = "10.10.10.14"
R3_GE1 = "10.10.10.18"
## Variables R4
R4_LO0 = "4.4.4.4"
R4_GE0 = "10.10.10.17"
R4_GE1 = "10.10.10.6"
R4_GE2 = "10.10.10.10"

# Carguemos las configuraciones respectivas 
# desde la plantilla Jinja2, aquí es donde le 
# pasamos las variables a la plantilla genérica 
# (podríamos hacerlo en un loop también!)
R1conf = template.render(IP_LO0=R1_LO0,IP_GE0=R1_GE0,IP_GE1=R1_GE1,IP_GE2=R1_GE2,RR="yes")
R2conf = template.render(IP_LO0=R2_LO0,IP_GE0=R2_GE0,IP_GE1=R2_GE1)
R3conf = template.render(IP_LO0=R3_LO0,IP_GE0=R3_GE0,IP_GE1=R3_GE1)
R4conf = template.render(IP_LO0=R4_LO0,IP_GE0=R4_GE0,IP_GE1=R4_GE1,IP_GE2=R4_GE2)

hosts = [ 
   {'name':'R1','ip': '192.168.0.1', 'config': R1conf},
   {'name':'R2','ip': '192.168.0.2', 'config': R2conf},
   {'name':'R2','ip': '192.168.0.3', 'config': R3conf},
   {'name':'R2','ip': '192.168.0.4', 'config': R4conf},
]

for host in hosts:
    # Definimos y abrimos la conexión
    device = driver(hostname=host['ip'],
                    username='ws',
                    password='ws',
                    optional_args={'port': host['port']})
    device.open()

    print('Cargando configuración en el equipo %s' % host['name'])
    device.load_merge_candidate(config=host['config'])
    config_changes = device.compare_config()

    # Hay cambios a aplicar?
    if config_changes:
        print('Cambios a aplicar...')
        print(config_changes)
    else:
        print('No hay cambios a aplicar')
    device.close()

