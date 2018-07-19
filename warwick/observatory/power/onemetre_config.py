#!/usr/bin/env python3
#
# This file is part of powerd.
#
# powerd is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# powerd is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with powerd.  If not, see <http://www.gnu.org/licenses/>.

"""Configuration for the W1m's power daemon"""

# pylint: disable=too-few-public-methods

from warwick.observatory.common import IP, daemons
from warwick.observatory.power import (
    DehumidifierSwitchDevice,
    DehumidifierParameter,
    SNMPDevice,
    APCPDUSocketParameter,
    APCUPSStatusParameter,
    APCUPSBatteryRemainingParameter,
    APCUPSBatteryHealthyParameter,
    APCUPSOutputLoadParameter,
    NetgearPoESocketParameter)

SWITCHABLE_PARAMETERS = (DehumidifierParameter, APCPDUSocketParameter, NetgearPoESocketParameter)

# Machines that are allowed to issue power commands
CONTROL_IPS = [IP.OneMetreDome, IP.OneMetreTCS]

# Timeout in seconds for SNMP commands
SNMP_TIMEOUT = 2

RACK_PDU_IP = '10.2.6.212'
RACK_PDU_PORTS = [
    APCPDUSocketParameter('rack_nuc', 1),
    APCPDUSocketParameter('telescope_12v', 2),
    APCPDUSocketParameter('telescope_80v', 3),
    APCPDUSocketParameter('vaisala', 4),
    APCPDUSocketParameter('monitor', 6),
    APCPDUSocketParameter('light', 8)
]

TEL_PDU_IP = '10.2.6.213'
TEL_PDU_PORTS = [
    APCPDUSocketParameter('red_camera', 1),
    APCPDUSocketParameter('blue_camera', 2),
    APCPDUSocketParameter('telescope_nuc', 3),
    APCPDUSocketParameter('red_focus_motor', 7),
    APCPDUSocketParameter('red_focus_controller', 8)
]

MAIN_UPS_IP = '10.2.6.210'
MAIN_UPS_PARAMETERS = [
    APCUPSStatusParameter('main_ups_status'),
    APCUPSBatteryRemainingParameter('main_ups_battery_remaining'),
    APCUPSBatteryHealthyParameter('main_ups_battery_healthy'),
    APCUPSOutputLoadParameter('main_ups_load'),
]

DOME_UPS_IP = '10.2.6.211'
DOME_UPS_PARAMETERS = [
    APCUPSStatusParameter('dome_ups_status'),
    APCUPSBatteryRemainingParameter('dome_ups_battery_remaining'),
    APCUPSBatteryHealthyParameter('dome_ups_battery_healthy'),
    APCUPSOutputLoadParameter('dome_ups_load'),
]

RACK_SWITCH_IP = '10.2.6.214'
RACK_SWITCH_PARAMETERS = [
    NetgearPoESocketParameter('telescope_network', 1),
    NetgearPoESocketParameter('webcam', 3),
    NetgearPoESocketParameter('roomalert', 5),
    NetgearPoESocketParameter('microphone', 7),
]

DEHUMIDIFIER_SERIAL_PORT = '/dev/dehumidifier'

class OneMetreConfig:
    """Configuration for the W1m's power daemon"""
    daemon = daemons.onemetre_power
    log_name = 'powerd'
    control_ips = [IP.OneMetreDome, IP.OneMetreTCS]

    @classmethod
    def get_devices(cls, power_daemon):
        """Returns a list of devices wrapped by the power daemon"""
        return [
            SNMPDevice(cls.log_name, RACK_PDU_IP, RACK_PDU_PORTS, SNMP_TIMEOUT),
            SNMPDevice(cls.log_name, TEL_PDU_IP, TEL_PDU_PORTS, SNMP_TIMEOUT),
            SNMPDevice(cls.log_name, MAIN_UPS_IP, MAIN_UPS_PARAMETERS, SNMP_TIMEOUT),
            SNMPDevice(cls.log_name, DOME_UPS_IP, DOME_UPS_PARAMETERS, SNMP_TIMEOUT),
            SNMPDevice(cls.log_name, RACK_SWITCH_IP, RACK_SWITCH_PARAMETERS, SNMP_TIMEOUT),
            DehumidifierSwitchDevice(cls.log_name, DEHUMIDIFIER_SERIAL_PORT,
                                     DehumidifierParameter('dehumidifier'), power_daemon),
        ]

    @classmethod
    def print_status(cls, data, format_switch, format_ups):
        """Prints a human-readable status summary to stdout"""
        print('   Tel. Computer: ' + format_switch(data['telescope_nuc']))
        print('    Tel. Network: ' + format_switch(data['telescope_network']))
        print('Tel. Controllers: ' + format_switch(data['telescope_12v']))
        print('     Tel. Motors: ' + format_switch(data['telescope_80v']))
        print('     Blue Camera: ' + format_switch(data['blue_camera']))
        print('      Red Camera: ' + format_switch(data['red_camera']))
        print('  Red Foc. Motor: ' + format_switch(data['red_focus_motor']))
        print(' Red Foc. Ctrler: ' + format_switch(data['red_focus_controller']))
        print('   Rack Computer: ' + format_switch(data['rack_nuc']))
        print('    Rack Monitor: ' + format_switch(data['monitor']))
        print('     Dome Webcam: ' + format_switch(data['webcam']))
        print(' Dome Microphone: ' + format_switch(data['microphone']))
        print('      Dome Light: ' + format_switch(data['light']))
        print('      Room Alert: ' + format_switch(data['roomalert']))
        print(' Weather Station: ' + format_switch(data['vaisala']))
        print('    Dehumidifier: ' + format_switch(data['dehumidifier']))
        print('        Main UPS: ' + format_ups(data['main_ups_status'],
                                                data['main_ups_battery_remaining'],
                                                data['main_ups_battery_healthy'],
                                                data['main_ups_load']))
        print('        Dome UPS: ' + format_ups(data['dome_ups_status'],
                                                data['dome_ups_battery_remaining'],
                                                data['dome_ups_battery_healthy'],
                                                data['dome_ups_load']))
