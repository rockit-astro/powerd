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

"""powerd common code"""

from .constants import Parameter, SwitchStatus, APCUPSStatus
from .snmp_device import SNMPDevice, SNMPParameter
from .netgear_device import NetgearPoESocketParameter
from .apc_device import (
    APCPDUSocketParameter,
    APCUPSStatusParameter,
    APCUPSBatteryRemainingParameter,
    APCUPSBatteryHealthyParameter,
    APCUPSOutputLoadParameter)
from .dehumidifier_switch_device import DehumidifierParameter, DehumidifierSwitchDevice
from .dummy_device import DummyUPSDevice, DummyDevice
