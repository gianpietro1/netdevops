#!/usr/bin/env python3

from netmiko import ConnectHandler

ip_list = ['192.168.0.1','192.168.0.2','192.168.0.3','192.168.0.4']

for host in ip_list:
  cisco_ios_xrv = {'device_type': 'cisco_xr', 'ip': host, 'username': 'ws', 'password': 'ws'}
  net_connect = ConnectHandler(**cisco_ios_xrv)

  config = ['xml agent tty iteration off','netconf-yang agent ssh','ssh server netconf vrf default','commit']

  output = net_connect.send_config_set(config)
  print(output)
