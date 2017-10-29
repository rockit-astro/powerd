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

"""Wrapper for accessing a device via SNMP"""

# pylint: disable=broad-except
# pylint: disable=too-few-public-methods
# pylint: disable=no-self-use

import datetime
import subprocess
from warwick.observatory.common import log

class SNMPDevice:
    """Wrapper for querying an APC PDU or UPS via SNMP"""
    def __init__(self, ip, parameters, query_timeout):
        self._ip = ip
        self._query_timeout = query_timeout
        self.parameters = parameters
        self.parameters_by_name = {p.name: p for p in parameters}

    def status(self):
        """Return a dictionary of parameter values for this device"""
        # Query all OIDs at once for efficiency
        oids = [p.get_oid for p in self.parameters]
        args = ['/usr/bin/snmpget', '-v', '1', '-c', 'public', self._ip] + oids
        output = subprocess.check_output(args, universal_newlines=True, timeout=self._query_timeout)
        lines = output.strip().split('\n')

        # Return a dictionary of values keyed by parameter name
        return {k.name: k.parse_snmp_output(v) for k, v in zip(self.parameters, lines)}

    def get_parameter(self, parameter_name):
        """Returns the value of a named parameter"""
        if parameter_name not in self.parameters_by_name:
            return False

        parameter = self.parameters_by_name[parameter_name]
        args = ['/usr/bin/snmpget', '-v', '1', '-c', 'public', self._ip, parameter.get_oid]
        output = subprocess.check_output(args, universal_newlines=True, timeout=self._query_timeout)
        return parameter.parse_snmp_output(output)

    def set_parameter(self, parameter_name, value):
        """Sets the value of a named parameter"""
        if parameter_name not in self.parameters_by_name:
            return False

        parameter = self.parameters_by_name[parameter_name]

        # Read only parameter
        if not parameter.set_oid:
            return False

        try:
            args = ['/usr/bin/snmpset', '-v', '1', '-c', 'private', self._ip, parameter.set_oid,
                    'i', parameter.format_set_value(value)]

            output = subprocess.check_output(args, universal_newlines=True,
                                             timeout=self._query_timeout)
            return parameter.parse_snmp_output(output) == value
        except Exception as exception:
            print('{} ERROR: failed to send SNMP command: {}' \
                  .format(datetime.datetime.utcnow(), str(exception)))
            log.error('powerd', 'Failed to send SNMP command (' \
                                  + str(exception) + ')')
            return False
