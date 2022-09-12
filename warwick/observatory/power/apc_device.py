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

"""APC-specific parameters for SNMPDevice"""

from .constants import SwitchStatus, APCUPSStatus, SwitchableParameter
from .snmp_device import SNMPParameter, IntegerSNMPParameter


class APCPDUSocketParameter(IntegerSNMPParameter, SwitchableParameter):
    """Parameter representing a specific PDU socket"""
    def __init__(self, name, socket):
        oid = '.1.3.6.1.4.1.318.1.1.12.3.3.1.1.4.' + str(socket)
        IntegerSNMPParameter.__init__(self, name, oid, oid, SwitchStatus.Unknown)

    def format_set_value(self, value):
        """Format a python value to a string to send via SNMP"""
        return '1' if value == SwitchStatus.On else '2'

    def parse_snmpget_output(self, output):
        """Convert a snmpget output string for this parameter into a python value"""
        return SwitchStatus.On if IntegerSNMPParameter.parse_snmpget_output(self, output) == 1 else SwitchStatus.Off


class APCUPSSocketGroupParameter(IntegerSNMPParameter, SwitchableParameter):
    """Parameter representing a specific UPS socket group"""
    def __init__(self, name, socket):
        oid = '.1.3.6.1.4.1.318.1.1.1.12.3.2.1.3.' + str(socket)
        IntegerSNMPParameter.__init__(self, name, oid, oid, SwitchStatus.Unknown)

    def format_set_value(self, value):
        """Format a python value to a string to send via SNMP"""
        return '1' if value == SwitchStatus.On else '2'

    def parse_snmpget_output(self, output):
        """Convert a snmpget output string for this parameter into a python value"""
        return SwitchStatus.On if IntegerSNMPParameter.parse_snmpget_output(self, output) == 1 else SwitchStatus.Off


class APCUPSStatusParameter(IntegerSNMPParameter):
    """Parameter representing the read-only UPS status enum"""
    def __init__(self, name):
        oid = '.1.3.6.1.4.1.318.1.1.1.4.1.1.0'
        IntegerSNMPParameter.__init__(self, name, oid, None, APCUPSStatus.Unknown)


class APCUPSBatteryHealthyParameter(IntegerSNMPParameter):
    """Parameter representing the read-only UPS battery health flag"""
    def __init__(self, name):
        IntegerSNMPParameter.__init__(self, name, '.1.3.6.1.4.1.318.1.1.1.2.2.4.0', None, False)

    def parse_snmpget_output(self, output):
        """Convert a snmpget output string for this parameter into a python value"""
        return IntegerSNMPParameter.parse_snmpget_output(self, output) == 1


class APCATSInputSourceParameter(IntegerSNMPParameter):
    """Parameter representing the read-only ATS source scalar"""
    def __init__(self, name):
        IntegerSNMPParameter.__init__(self, name, '.1.3.6.1.4.1.318.1.1.8.5.1.2.0', None, 0)


class APCGaugeParameter(SNMPParameter):
    """Data structure encapsulating a readonly UPS Gauge parameter"""
    def __init__(self, name, oid):
        SNMPParameter.__init__(self, name, oid, None, 0)

    def parse_snmpget_output(self, output):
        """Convert a snmpget output string for this parameter into a python value"""
        parts = output.split(' ')
        if parts[-2] != 'Gauge32:':
            raise Exception('Unabled to parse Gauge32 from SNMP output: ' + output)

        return int(parts[-1])

    def parse_snmpset_output(self, output):
        """Convert a snmpset output string for this parameter into a python value"""
        return self.parse_snmpget_output(output)


class APCUPSBatteryRemainingParameter(APCGaugeParameter):
    """Parameter representing the read-only UPS battery remaining gauge"""
    def __init__(self, name):
        APCGaugeParameter.__init__(self, name, '.1.3.6.1.4.1.318.1.1.1.2.2.1.0')


class APCUPSOutputLoadParameter(APCGaugeParameter):
    """Parameter representing the read-only UPS load gauge"""
    def __init__(self, name):
        APCGaugeParameter.__init__(self, name, '.1.3.6.1.4.1.318.1.1.1.4.2.3.0')
