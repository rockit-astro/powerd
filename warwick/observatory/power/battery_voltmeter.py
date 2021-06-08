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

"""Wrapper for accessing the custom Arduino board via USB"""

import re
import threading
import time
import serial
from warwick.observatory.common import log
from .constants import Parameter

# pylint: disable=anomalous-backslash-in-string
DATA_REGEX = b'^(?P<voltage>[-+][0-9]{2}\.[0-9]{2})\r\n$'
# pylint: enable=anomalous-backslash-in-string


class VoltageParameter(Parameter):
    """Parameter representing the read-only voltage measurement"""
    def __init__(self, name):
        Parameter.__init__(self, name, None)


class BatteryVoltmeterDevice:
    """Wrapper for querying an attached Arduino via RS232"""
    def __init__(self, log_name, port_name, parameter):
        self._log_name = log_name
        self._port = None
        self._port_name = port_name
        self._lock = threading.Lock()
        self._port_connected = False
        self._updated_condition = threading.Condition()

        runloop = threading.Thread(target=self.run)
        runloop.daemon = True
        runloop.start()

        self._regex = re.compile(DATA_REGEX, re.DOTALL)
        self._voltage = 0
        self.parameters = [parameter]

    def run(self):
        """Main run loop"""
        while True:
            # Initial setup
            try:
                self._port = serial.Serial(self._port_name, 9600, timeout=3)
                print('Connected to', self._port_name)
                log.info(self._log_name, 'Connected to battery voltmeter')
                self._port_connected = True
            except Exception as exception:
                if self._port_connected:
                    log.error(self._log_name, 'Lost connection to battery voltmeter')

                print('error: failed to connect to battery voltmeter')
                print(exception)
                print('Will retry in 10 seconds...')
                time.sleep(10.)
                continue

            try:
                # Flush any stale state
                self._port.flushInput()
                self._port.flushOutput()

                # Main run loop
                while True:
                    data = self._port.readline()
                    match = self._regex.match(data)

                    if match:
                        self._voltage = float(match.group('voltage'))

            except Exception as exception:
                self._port.close()
                if self._port_connected:
                    log.error(self._log_name, 'Lost connection to battery voltmeter')
                    print('error: lost connection to battery voltmeter')
                    print(exception)

                self._port_connected = False
                print('Will retry in 10 seconds...')
                time.sleep(10.)

    def status(self):
        """Return a dictionary of parameter values for this device"""
        if not self._port_connected:
            return {self.parameters[0].name: self.parameters[0].error_value}

        with self._updated_condition:
            return {self.parameters[0].name: self._voltage}

    def get_parameter(self, parameter_name):
        """Returns the value of a named parameter"""
        if parameter_name != self.parameters[0].name:
            return False

        if not self._port_connected:
            return self.parameters[0].error_value

        with self._updated_condition:
            return self._voltage

    def set_parameter(self, *_):
        """Sets the value of a named parameter"""

        # Voltage is read-only
        return False
