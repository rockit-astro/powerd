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

"""Dummy device for testing"""

# pylint: disable=unused-argument

import time
from .apc_device import (
    APCUPSStatus,
    APCUPSBatteryRemaining,
    APCUPSBatteryHealthy,
    APCUPSOutputLoad)

class DummyUPSDevice:
    """Dummy UPS device for testing"""
    def __init__(self, ip, parameters, query_timeout):
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
        if isinstance(parameter, APCUPSStatus):
            return 2

        if isinstance(parameter, APCUPSBatteryRemaining):
            return 100

        if isinstance(parameter, APCUPSBatteryHealthy):
            return True

        if isinstance(parameter, APCUPSOutputLoad):
            return 5

        return False

    def set_parameter(self, parameter_name, value):
        """APC UPSes have no settable parameters"""
        return False

class DummyDevice:
    """Dummy device for testing"""
    def __init__(self, ip, parameters, query_timeout):
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
