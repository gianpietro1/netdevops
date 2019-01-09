#!/usr/bin/env python
# Import the required libraries
from napalm import get_network_driver
import sys

# Define the driver that will be used
driver = get_network_driver('iosxr')

# Define the connection parameters
device = driver(hostname=sys.argv[1], username='ws', password='ws')

# Open the connection
print('Opening ...')
device.open()

# Rollback the configuration
print('Running Rollback ...')
device.rollback()

# Close the connection
device.close()
