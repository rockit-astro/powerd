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

"""APC-specific parameters for SNMPDevice"""

# pylint: disable=too-few-public-methods
# pylint: disable=no-self-use

from . import Parameter

class ParameterType:
    """Defines the way that an OID parameter should be handled"""
    Bool, ReadOnlyBool, Int, ReadOnlyInt, ReadOnlyGauge = range(5)

class APCParameter(Parameter):
    """Data structure encapsulating a PDU/UPS parameter"""
    def __init__(self, name, oid_type, oid):
        Parameter.__init__(self, name)
        self._oid_type = oid_type
        self.get_oid = oid

        self.set_oid = None
        if oid_type in [ParameterType.Int, ParameterType.Bool]:
            self.set_oid = oid

    def format_set_value(self, value):
        """Format a python value to a string to send via SNMP"""
        if self._oid_type == ParameterType.Bool:
            return '1' if value else '2'
        return str(value)

    def parse_snmp_output(self, output):
        """Convert a snmp output string for this parameter into a python value"""
        parts = output.split(' ')

        if self._oid_type == ParameterType.ReadOnlyGauge and parts[-2] != 'Gauge32:':
            raise Exception('Unabled to parse Gauge32 from SNMP output: ' + output)
        elif self._oid_type != ParameterType.ReadOnlyGauge and parts[-2] != 'INTEGER:':
            raise Exception('Unabled to parse integer from SNMP output: ' + output)

        if self._oid_type == ParameterType.Bool or self._oid_type == ParameterType.ReadOnlyBool:
            return int(parts[-1]) == 1

        return int(parts[-1])

class APCPDUSocket(APCParameter):
    """Parameter representing a specific PDU socket"""
    def __init__(self, name, socket):
        oid = '.1.3.6.1.4.1.318.1.1.12.3.3.1.1.4.' + str(socket)
        APCParameter.__init__(self, name, ParameterType.Bool, oid)

class APCUPSStatus(APCParameter):
    """Parameter representing the read-only UPS status enum"""
    def __init__(self, name):
        oid = '.1.3.6.1.4.1.318.1.1.1.4.1.1.0'
        APCParameter.__init__(self, name, ParameterType.ReadOnlyInt, oid)

class APCUPSBatteryRemaining(APCParameter):
    """Parameter representing the read-only UPS battery remaining gauge"""
    def __init__(self, name):
        oid = '.1.3.6.1.4.1.318.1.1.1.2.2.1.0'
        APCParameter.__init__(self, name, ParameterType.ReadOnlyGauge, oid)

class APCUPSBatteryHealthy(APCParameter):
    """Parameter representing the read-only UPS battery health flag"""
    def __init__(self, name):
        oid = '.1.3.6.1.4.1.318.1.1.1.2.2.4.0'
        APCParameter.__init__(self, name, ParameterType.ReadOnlyBool, oid)

class APCUPSOutputLoad(APCParameter):
    """Parameter representing the read-only UPS load gauge"""
    def __init__(self, name):
        oid = '.1.3.6.1.4.1.318.1.1.1.4.2.3.0'
        APCParameter.__init__(self, name, ParameterType.ReadOnlyGauge, oid)
