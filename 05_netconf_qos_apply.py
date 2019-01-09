#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Import the required libraries
from ncclient import manager
import sys

# Define a NETCONF filter based on a YANG model
config = """
    <config>
     <interface-configurations xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg">
      <interface-configuration>
        <interface-name>{interface}</interface-name>
        <active>act</active>
          <qos xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-qos-ma-cfg">
            <output>
              <service-policy>
                <service-policy-name>BACKBONE-QOS</service-policy-name>
              </service-policy>
            </output>
          </qos>
      </interface-configuration>
     </interface-configurations>
    </config>

"""

hosts = [ 
   {'name':'R1','ip': '192.168.0.1'},
   {'name':'R2','ip': '192.168.0.2'},
   {'name':'R3','ip': '192.168.0.3'},
   {'name':'R4','ip': '192.168.0.4'},
]

interface_list = ['GigabitEthernet0/0/0/0','GigabitEthernet0/0/0/1','GigabitEthernet0/0/0/2']

for host in hosts:
    # Definimos y abrimos la conexión
    m = manager.connect(host=host['ip'],
                        username='ws',
                        password='ws',
                        hostkey_verify=False,look_for_keys=False)

    for interface in interface_list:
      # Use the NETCONF "edit-config" method to set configuration in the device
      response = m.edit_config(target='candidate', config=config.format(interface=interface))

      # Commit the configuration
      m.commit()
    
    m.close_session()

