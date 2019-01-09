#!/usr/bin/env python

from netmiko import ConnectHandler

ip_list = ['192.168.0.1','192.168.0.2','192.168.0.3','192.168.0.4']

for host in ip_list:
  cisco_ios_xrv = {'device_type': 'cisco_xr', 'ip': host, 'username': 'ws', 'password': 'ws'}
  net_connect = ConnectHandler(**cisco_ios_xrv)
  output = net_connect.send_command('show interface brief')
  print(output)

  interfaces = net_connect.send_command('show interfaces',use_textfsm=True)

  change_mtu_list = []

  for interface in interfaces:
      hardwareType = interface['hardware_type']
      mtu_number = int(interface['mtu'])
      new_mtu = '9000'
      if hardwareType == 'GigabitEthernet' and mtu_number <= 1514:
        change_mtu_list.extend(['interface ' + interface['interface'], 'mtu ' + new_mtu])

  if change_mtu_list:
    change_mtu_list.append('commit')
    output = net_connect.send_config_set(change_mtu_list)
    print(output)
