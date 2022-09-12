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

"""Wrapper for querying the SuperWASP roof battery voltage via roofd"""

from warwick.observatory.common import log
from .constants import Parameter


class VoltageParameter(Parameter):
    """Parameter representing the read-only voltage measurement"""
    def __init__(self, name):
        Parameter.__init__(self, name, None)


class SWASPRoofDevice:
    """Wrapper for querying the SuperWASP roof battery voltage via roofd"""
    def __init__(self, log_name, daemon, parameter_name, query_timeout):
        self._log_name = log_name
        self._parameter_name = parameter_name
        self._daemon = daemon
        self._query_timeout = query_timeout
        self._last_command_failed = False
        self.parameters = [VoltageParameter(parameter_name)]
        self.parameters_by_name = {p.name: p for p in self.parameters}

    def status(self):
        """Return a dictionary of parameter values for this device"""
        return {self._parameter_name: self.get_parameter(self._parameter_name)}

    def get_parameter(self, parameter_name):
        """Returns the value of a named parameter"""
        if parameter_name != self._parameter_name:
            return False

        try:
            with self._daemon.connect(timeout=self._query_timeout) as daemon:
                value = daemon.status()[parameter_name]

            if self._last_command_failed:
                log.info(self._log_name, 'Restored contact with ' + self._daemon.name)
                self._last_command_failed = False

            return value

        except Exception:
            if not self._last_command_failed:
                log.error(self._log_name, 'Lost contact with ' + self._daemon.name)
                self._last_command_failed = True

            return None

    def set_parameter(self, *_):
        """Sets the value of a named parameter"""
        # Voltage is read-only
        return False
