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

from warwick.observatory.common import TFmt


class Parameter:
    """Data structure encapsulating a switchable port/device"""
    def __init__(self, name, error_value):
        self.name = name
        self.error_value = error_value


class SwitchableParameter:
    pass


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
        1: TFmt.Bold + TFmt.Red + 'UNKNOWN' + TFmt.Clear,
        2: TFmt.Bold + TFmt.Green + 'ONLINE' + TFmt.Clear,
        3: TFmt.Bold + TFmt.Yellow + 'ON BATTERY' + TFmt.Clear,
        4: TFmt.Bold + TFmt.Red + 'SMART BOOST' + TFmt.Clear,
        5: TFmt.Bold + TFmt.Red + 'TIMED SLEEPING' + TFmt.Clear,
        6: TFmt.Bold + TFmt.Red + 'SOFTWARE BYPASS' + TFmt.Clear,
        7: TFmt.Bold + TFmt.Red + 'OFF' + TFmt.Clear,
        8: TFmt.Bold + TFmt.Red + 'REBOOTING' + TFmt.Clear,
        9: TFmt.Bold + TFmt.Red + 'SWITCHED BYPASS' + TFmt.Clear,
        10: TFmt.Bold + TFmt.Red + 'HARDWARE FAILURE BYPASS' + TFmt.Clear,
        11: TFmt.Bold + TFmt.Red + 'SLEEPING UNTIL POWER RETURNS' + TFmt.Clear,
        12: TFmt.Bold + TFmt.Red + 'ON SMART TRIM' + TFmt.Clear,
    }

    @classmethod
    def message(cls, error_code):
        """Returns a human readable string describing a status type"""
        if error_code in cls._messages:
            return cls._messages[error_code]
        return cls._messages[1]
