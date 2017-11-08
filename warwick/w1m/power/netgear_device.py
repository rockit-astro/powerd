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

from . import Parameter

class NetgearPoESocket(Parameter):
    """Data structure encapsulating a PoE parameter"""
    def __init__(self, name, port):
        Parameter.__init__(self, name)
        self.port = port
        self.get_oid = '.1.3.6.1.2.1.105.1.1.1.6.1.' + str(port)
        self.set_oid = '.1.3.6.1.2.1.105.1.1.1.3.1.' + str(port)

    def parse_snmp_output(self, output):
        """Convert a snmp output string for this parameter into a python value"""
        return int(output.split(' ')[-1]) == 3

    def format_set_value(self, value):
        """Format a python value to a string to send via SNMP"""
        return '1' if value else '2'

