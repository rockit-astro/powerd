#
# This file is part of the Robotic Observatory Control Kit (rockit)
#
# rockit is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# rockit is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with rockit.  If not, see <http://www.gnu.org/licenses/>.

"""Dummy device for testing"""

import time
from .apc_device import (
    APCUPSStatusParameter,
    APCUPSBatteryRemainingParameter,
    APCUPSBatteryHealthyParameter,
    APCUPSOutputLoadParameter)


class DummyUPSDevice:
    """Dummy UPS device for testing"""
    def __init__(self, parameters):
        # IP and query_timeout are deliberately ignored
        self.parameters = parameters
        self.parameters_by_name = {p.name: p for p in parameters}

    def status(self):
        """Return a dictionary of parameter values for this device"""
        time.sleep(0.2)
        return {k.name: self.get_parameter(k.name) for k in self.parameters}

    def get_parameter(self, parameter_name):
        """Returns the value of a named parameter"""

        if parameter_name not in self.parameters_by_name:
            return False

        time.sleep(0.2)
        parameter = self.parameters_by_name[parameter_name]
        if isinstance(parameter, APCUPSStatusParameter):
            return 2

        if isinstance(parameter, APCUPSBatteryRemainingParameter):
            return 100

        if isinstance(parameter, APCUPSBatteryHealthyParameter):
            return True

        if isinstance(parameter, APCUPSOutputLoadParameter):
            return 5

        return False

    def set_parameter(self, *_):
        """APC UPSes have no settable parameters"""
        return False


class DummyDevice:
    """Dummy device for testing"""
    def __init__(self, parameters):
        # IP and query_timeout are deliberately ignored
        self.parameters = parameters
        self.parameters_by_name = {p.name: p for p in parameters}

        self._state = {p.name: False for p in parameters}

    def status(self):
        """Return a dictionary of parameter values for this device"""
        time.sleep(0.2)
        return self._state

    def get_parameter(self, parameter_name):
        """Returns the value of a named parameter"""
        if parameter_name not in self.parameters_by_name:
            return False

        time.sleep(0.2)
        return self._state[parameter_name]

    def set_parameter(self, parameter_name, value):
        """Sets the value of a named parameter"""
        if parameter_name not in self._state:
            return False

        time.sleep(0.2)
        self._state[parameter_name] = value
        return True
