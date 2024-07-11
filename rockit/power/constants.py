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

"""Constants and status codes used by powerd"""


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

    _labels = {
        1: 'UNKNOWN',
        2: 'ONLINE',
        3: 'ON BATTERY',
        4: 'SMART BOOST',
        5: 'TIMED SLEEPING',
        6: 'SOFTWARE BYPASS',
        7: 'OFF',
        8: 'REBOOTING',
        9: 'SWITCHED BYPASS',
        10: 'HARDWARE FAILURE BYPASS',
        11: 'SLEEPING UNTIL POWER RETURNS',
        12: 'ON SMART TRIM',
    }

    _colors = {
        1: 'red',
        2: 'green',
        3: 'yellow',
        4: 'red',
        5: 'red',
        6: 'red',
        7: 'red',
        8: 'red',
        9: 'red',
        10: 'red',
        11: 'red',
        12: 'red'
    }

    @classmethod
    def label(cls, status, formatting=False):
        """
        Returns a human readable string describing a status
        Set formatting=true to enable terminal formatting characters
        """
        if formatting:
            if status in cls._labels and status in cls._colors:
                return f'[b][{cls._colors[status]}]{cls._labels[status]}[/{cls._colors[status]}][/b]'
            return '[b][red]UNKNOWN[/red][/b]'

        if status in cls._labels:
            return cls._labels[status]
        return 'UNKNOWN'
