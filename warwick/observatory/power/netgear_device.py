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

"""Netgear-specific parameters for SNMPDevice"""

# pylint: disable=too-few-public-methods
# pylint: disable=no-self-use

from . import SNMPParameter, SwitchStatus

class NetgearPoESocketParameter(SNMPParameter):
    """Data structure encapsulating a PoE parameter"""
    def __init__(self, name, port):
        get_oid = '.1.3.6.1.2.1.105.1.1.1.6.1.' + str(port)
        set_oid = '.1.3.6.1.2.1.105.1.1.1.3.1.' + str(port)
        SNMPParameter.__init__(self, name, get_oid, set_oid, SwitchStatus.Unknown)
        self.port = port

    def parse_snmpget_output(self, output):
        """Convert a snmpget output string for this parameter into a python value"""
        return SwitchStatus.On if int(output.split(' ')[-1]) == 3 else SwitchStatus.Off

    def parse_snmpset_output(self, output):
        """Convert a snmpset output string for this parameter into a python value"""
        return SwitchStatus.On if int(output.split(' ')[-1]) == 1 else SwitchStatus.Off

    def format_set_value(self, value):
        """Format a python value to a string to send via SNMP"""
        return '1' if value == SwitchStatus.On else '2'
