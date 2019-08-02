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

"""Wrapper for accessing an ETH002 relay board via http"""

import datetime
import urllib.request
import xml.etree.ElementTree as ET

from warwick.observatory.common import log
from .constants import Parameter, SwitchStatus


class ETH002SwitchParameter(Parameter):
    """Data structure encapsulating an ETH002 relay"""
    def __init__(self, name, channel):
        Parameter.__init__(self, name, SwitchStatus.Unknown)
        self.channel = channel

    def parse_status_response(self, response):
        """Extract switch status from XML status output"""
        try:
            status = response.find('relay' + str(self.channel)).text
            if status == '0':
                return SwitchStatus.Off
            if status == '1':
                return SwitchStatus.On
        except Exception:
            pass

        return SwitchStatus.Unknown

    def format_set_parameter(self, value):
        """Format a python value to a url GET parameter"""
        return 'io.cgi?DO{0}{1}=0'.format(
            'A' if value else 'I',
            str(self.channel + 1))


class ETH002Device:
    """Wrapper for querying an ETH002 ethernet relay board via http"""
    def __init__(self, log_name, ip, parameters, query_timeout):
        self._log_name = log_name
        self._ip = ip
        self._query_timeout = query_timeout
        self._last_command_failed = False
        self.parameters = parameters
        self.parameters_by_name = {p.name: p for p in parameters}

    def status(self):
        """Return a dictionary of parameter values for this device"""
        try:
            url = 'http://' + self._ip + '/status.xml'
            with urllib.request.urlopen(url, None, self._query_timeout) as response:
                response = response.read().decode('ascii')
                xml = ET.fromstring(response)

            if self._last_command_failed:
                log.info(self._log_name, 'Restored contact with ' + self._ip)
                self._last_command_failed = False

            # Return a dictionary of values keyed by parameter name
            return {k.name: k.parse_status_response(xml) for k in self.parameters}

        except Exception as exception:
            print('{} ERROR: failed to query {}: {}' \
                  .format(datetime.datetime.utcnow(), self._ip, str(exception)))

            if not self._last_command_failed:
                log.error(self._log_name, 'Lost contact with ' + self._ip)
                self._last_command_failed = True

            return {k.name: k.error_value for k in self.parameters}

    def get_parameter(self, parameter_name):
        """Returns the value of a named parameter"""
        if parameter_name not in self.parameters_by_name:
            return False

        return self.status()[parameter_name]

    def set_parameter(self, parameter_name, value):
        """Sets the value of a named parameter"""
        if parameter_name not in self.parameters_by_name:
            return False

        parameter = self.parameters_by_name[parameter_name]

        try:
            url = 'http://' + self._ip + '/' + parameter.format_set_parameter(value)
            with urllib.request.urlopen(url, None, self._query_timeout) as response:
                response = response.read().decode('ascii')

            if self._last_command_failed:
                log.info(self._log_name, 'Restored contact with ' + self._ip)
                self._last_command_failed = False
        except Exception as exception:
            print('{} ERROR: failed to send HTTP command: {}' \
                  .format(datetime.datetime.utcnow(), str(exception)))

            if not self._last_command_failed:
                log.error(self._log_name, 'Lost contact with ' + self._ip)
                self._last_command_failed = True

            return False

        return response == 'Success! ' + str(value)
