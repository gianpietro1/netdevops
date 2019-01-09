#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Import the required libraries
from ncclient import manager
import sys

# Define a NETCONF filter based on a YANG model
config = """
    <config>
     <policy-manager xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-infra-policymgr-cfg">
      <class-maps>
        <class-map>
          <name>VOICE</name>
          <type>qos</type>
          <class-map-mode-match-any></class-map-mode-match-any>
          <match>
            <mpls-experimental-topmost>5</mpls-experimental-topmost>
          </match>
        </class-map>
      </class-maps>
      <policy-maps>
        <policy-map>
          <name>BACKBONE-QOS</name>
          <type>qos</type>
          <policy-map-rule>
            <class-name>VOICE</class-name>
            <class-type>qos</class-type>
            <police>
              <rate>
                <value>1</value>
                <units>gbps</units>
              </rate>
            </police>
            <priority-level>1</priority-level>
          </policy-map-rule>
        </policy-map>
      </policy-maps>
     </policy-manager>
</config>

"""

hosts = [ 
   {'name':'R1','ip': '192.168.0.1'},
   {'name':'R2','ip': '192.168.0.2'},
   {'name':'R3','ip': '192.168.0.3'},
   {'name':'R4','ip': '192.168.0.4'},
]

for host in hosts:
    # Definimos y abrimos la conexión
    m = manager.connect(host=host['ip'],
                        username='ws',
                        password='ws',
                        hostkey_verify=False,look_for_keys=False)
    # Use the NETCONF "edit-config" method to set configuration in the device
    response = m.edit_config(target='candidate', config=config)

    # Commit the configuration
    commit = m.commit()
    print(commit)
    m.close_session()

