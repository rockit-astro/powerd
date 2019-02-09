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

"""Configuration for the RASA's power daemon"""

# pylint: disable=too-few-public-methods

from warwick.observatory.common import IP, daemons
from warwick.observatory.power import (
    SNMPDevice,
    APCPDUSocketParameter,
    APCUPSStatusParameter,
    APCUPSBatteryRemainingParameter,
    APCUPSBatteryHealthyParameter,
    APCUPSOutputLoadParameter,
    APCUPSSocketGroupParameter,
    ETH002Device,
    ETH002SwitchParameter)

# Timeout in seconds for remote queries
SNMP_TIMEOUT = 2
HTTP_TIMEOUT = 5

UPS_IP = '10.2.6.40'
UPS_PARAMETERS = [
    APCUPSStatusParameter('ups_status'),
    APCUPSBatteryRemainingParameter('ups_battery_remaining'),
    APCUPSBatteryHealthyParameter('ups_battery_healthy'),
    APCUPSOutputLoadParameter('ups_load'),
    APCUPSSocketGroupParameter('dome', 2),
]

RACK_PDU_IP = '10.2.6.41'
RACK_PDU_PORTS = [
    APCPDUSocketParameter('nuc', 1),
    APCPDUSocketParameter('light', 2),
    APCPDUSocketParameter('telescope', 3),
    APCPDUSocketParameter('poe_network', 4),
    APCPDUSocketParameter('monitor', 8),
]

DEHUMIDIFIER_IP = '10.2.6.48'
DEHUMIDIFIER_PORTS = [
    ETH002SwitchParameter('dehumidifier', 0),
]

class RASAConfig:
    """Configuration for the RASA's power daemon"""
    daemon = daemons.rasa_power
    log_name = 'rasa_powerd'
    control_ips = [IP.RASAMain]

    @classmethod
    def get_devices(cls, power_daemon):
        """Returns a list of devices wrapped by the power daemon"""
        return [
            SNMPDevice(cls.log_name, UPS_IP, UPS_PARAMETERS, SNMP_TIMEOUT),
            SNMPDevice(cls.log_name, RACK_PDU_IP, RACK_PDU_PORTS, SNMP_TIMEOUT),
            ETH002Device(cls.log_name, DEHUMIDIFIER_IP, DEHUMIDIFIER_PORTS, HTTP_TIMEOUT)
        ]

    @classmethod
    def print_status(cls, data, format_switch, format_ups):
        """Prints a human-readable status summary to stdout"""
        print('        Computer: ' + format_switch(data['nuc']))
        print('       Telescope: ' + format_switch(data['telescope']))
        print('      Dome Light: ' + format_switch(data['light']))
        print('    Dehumidifier: ' + format_switch(data['dehumidifier']))
        print('            Dome: ' + format_switch(data['dome']))
        print('     PoE Network: ' + format_switch(data['poe_network']))
        print('    Rack Monitor: ' + format_switch(data['monitor']))
        print('             UPS: ' + format_ups(data['ups_status'],
                                                data['ups_battery_remaining'],
                                                data['ups_battery_healthy'],
                                                data['ups_load']))
