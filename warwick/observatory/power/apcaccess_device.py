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

"""Wrapper for querying an APC UPS via apcaccess"""

# pylint: disable=no-self-use

import datetime
import subprocess
from warwick.observatory.common import log
from .constants import APCUPSStatus, Parameter


class APCAccessParameter(Parameter):
    """Data structure encapsulating a parameter fetched via apcaccess"""
    def __init__(self, name, key, error_value):
        Parameter.__init__(self, name, error_value)
        self.key = key

    def parse_apcaccess_output(self, output):
        """Convert a apcaccess output string for this parameter into a python value"""
        return float(output)


class APCAccessUPSStatusParameter(APCAccessParameter):
    """Parameter representing the read-only UPS status enum"""
    def __init__(self, name):
        APCAccessParameter.__init__(self, name, 'STATUS', APCUPSStatus.Unknown)

    def parse_apcaccess_output(self, output):
        """Convert a apcaccess output string for this parameter into a python value"""
        components = output.split()

        if 'ONBATT' in components:
            return APCUPSStatus.OnBattery

        if 'ONLINE' in components:
            return APCUPSStatus.Online

        return APCUPSStatus.Unknown


class APCAccessUPSBatteryHealthyParameter(APCAccessParameter):
    """Parameter representing the read-only UPS battery health flag"""
    def __init__(self, name):
        APCAccessParameter.__init__(self, name, 'STATFLAG', False)

    def parse_apcaccess_output(self, output):
        """Convert a apcaccess output string for this parameter into a python value"""
        # output is a hex string like 0x05060010
        # Bit 7 is the 'replace battery' flag
        return (int(output, 16) & 0x80) == 0


class APCAccessUPSBatteryRemainingParameter(APCAccessParameter):
    """Parameter representing the read-only UPS battery remaining gauge"""
    def __init__(self, name):
        APCAccessParameter.__init__(self, name, 'BCHARGE', 0)


class APCAccessUPSOutputLoadParameter(APCAccessParameter):
    """Parameter representing the read-only UPS load gauge"""
    def __init__(self, name):
        APCAccessParameter.__init__(self, name, 'LOADPCT', 0)


class APCAccessDevice:
    """Wrapper for querying an APC UPS via apcaccess"""
    def __init__(self, log_name, device, query_timeout, parameters):
        self._log_name = log_name
        self._device = device
        self._query_timeout = query_timeout
        self._last_command_failed = False
        self.parameters = parameters
        self.parameters_by_name = {p.name: p for p in parameters}

    def query_apcaccess(self, p):
        try:
            args = ['/usr/sbin/apcaccess', '-f', self._device, '-p', p.key, '-u']

            output = subprocess.check_output(args, universal_newlines=True, timeout=self._query_timeout).strip()
            if not output:
                return p.error_value

            if self._last_command_failed:
                log.info(self._log_name, 'Restored contact with ' + self._device)
                self._last_command_failed = False

            return p.parse_apcaccess_output(output)
        except Exception as exception:
            print('{} ERROR: failed to query {}: {}' \
                  .format(datetime.datetime.utcnow(), self._device, str(exception)))

            if not self._last_command_failed:
                log.error(self._log_name, 'Lost contact with ' + self._device)
                self._last_command_failed = True

            return p.error_value

    def status(self):
        """Return a dictionary of parameter values for this device"""
        return {p.name: self.query_apcaccess(p) for p in self.parameters}

    def get_parameter(self, parameter_name):
        """Returns the value of a named parameter"""
        if parameter_name not in self.parameters_by_name:
            return False

        return self.query_apcaccess(self.parameters_by_name[parameter_name])

    def set_parameter(self, *_):
        """Sets the value of a named parameter"""
        # apcaccess is read-only
        return False
