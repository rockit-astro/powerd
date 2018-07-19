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

"""Constants and status codes used by powerd"""

# pylint: disable=too-few-public-methods
# pylint: disable=invalid-name

FMT_YELLOW = u'\033[93m'
FMT_GREEN = u'\033[92m'
FMT_RED = u'\033[91m'
FMT_BOLD = u'\033[1m'
FMT_CLEAR = u'\033[0m'

class Parameter:
    """Data structure encapsulating a switchable port/device"""
    def __init__(self, name, error_value):
        self.name = name
        self.error_value = error_value

class SwitchStatus:
    """Represents the state of a power port"""
    Off, On, Unknown = range(3)

class APCUPSStatus:
    """Represents the state of an APC UPS"""
    Unknown = 1
    Online = 2
    OnBattery = 3
    SmartBoost = 4
    TimedSleeping = 5
    SoftwareBypass = 6
    Off = 7
    Rebooting = 8
    SwitchedBypass = 9
    HardwareFailureBypass = 10
    SleepingUntilPowerReturns = 11
    OnSmartTrim = 12

    _messages = {
        1: FMT_BOLD + FMT_RED + 'UNKNOWN' + FMT_CLEAR,
        2: FMT_BOLD + FMT_GREEN + 'ONLINE' + FMT_CLEAR,
        3: FMT_BOLD + FMT_YELLOW + 'ON BATTERY' + FMT_CLEAR,
        4: FMT_BOLD + FMT_RED + 'SMART BOOST' + FMT_CLEAR,
        5: FMT_BOLD + FMT_RED + 'TIMED SLEEPING' + FMT_CLEAR,
        6: FMT_BOLD + FMT_RED + 'SOFTWARE BYPASS' + FMT_CLEAR,
        7: FMT_BOLD + FMT_RED + 'OFF' + FMT_CLEAR,
        8: FMT_BOLD + FMT_RED + 'REBOOTING' + FMT_CLEAR,
        9: FMT_BOLD + FMT_RED + 'SWITCHED BYPASS' + FMT_CLEAR,
        10: FMT_BOLD + FMT_RED + 'HARDWARE FAILURE BYPASS' + FMT_CLEAR,
        11: FMT_BOLD + FMT_RED + 'SLEEPING UNTIL POWER RETURNS' + FMT_CLEAR,
        12: FMT_BOLD + FMT_RED + 'ON SMART TRIM' + FMT_CLEAR,
    }

    @classmethod
    def message(cls, error_code):
        """Returns a human readable string describing a status type"""
        if error_code in cls._messages:
            return cls._messages[error_code]
        return cls._messages[1]
