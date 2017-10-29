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

"""Wrapper for accessing the custom Arduino board via USB"""

# pylint: disable=broad-except
# pylint: disable=too-few-public-methods
# pylint: disable=too-many-instance-attributes

import datetime
import threading
import time
import serial
from warwick.observatory.common import log

class DehumidifierSwitchDevice:
    """Wrapper for querying an attached Arduino via RS232"""
    def __init__(self, port_name, parameter, power_daemon):
        self._port = None
        self._port_name = port_name
        self._lock = threading.Lock()
        self._port_connected = False
        self._updated_condition = threading.Condition()

        self._enabled = False
        self._enabled_date = datetime.datetime.min
        self._desired_enabled = False

        self._button_light = False
        self._desired_button_light = False

        runloop = threading.Thread(target=self.run)
        runloop.daemon = True
        runloop.start()

        self._power_daemon = power_daemon
        self.parameters = [parameter]

    def run(self):
        """Main run loop"""
        while True:
            # Initial setup
            try:
                self._port = serial.Serial(self._port_name, 9600, timeout=3)
                print('Connected to', self._port_name)

                first_query = self._enabled_date == datetime.datetime.min
                prefix = 'Established' if first_query else 'Restored'
                log.info('powerd', prefix + ' contact with Dehumidifier switch')
                self._port_connected = True
            except Exception as exception:
                if self._port_connected:
                    log.error('powerd', 'Lost contact with Dehumidifier switch')

                print('error: failed to connect to Dehumidifier switch')
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
                    data = ord(self._port.read(1))

                    # First bit is set when the relay to the dehumidifier is enabled
                    enabled = data & 0x01

                    # Second bit is set when the status light is active
                    # Used internally where we don't care about thread safety, so set directly
                    self._button_light = (data & 0x02) != 0

                    if enabled != self._enabled:
                        with self._updated_condition:
                            self._enabled = enabled
                            self._enabled_date = datetime.datetime.utcnow()

                            # Wake up any threads that requested the change so it can return
                            self._updated_condition.notify_all()

                    # Third bit is set for one update cycle when the button is pressed
                    if data & 0x04:
                        light_enabled = self._power_daemon.value('light')
                        if not self._power_daemon.switch('light', not light_enabled):
                            log.error('powerd', 'Failed to toggle dome lights')

                    if self._desired_enabled != self._enabled \
                            or self._desired_button_light != self._button_light:
                        command = (0x01 if self._desired_enabled else 0) | \
                                  (0x02 if self._desired_button_light else 0)
                        self._port.write(chr(command).encode('ascii'))

            except Exception as exception:
                self._port.close()
                if self._port_connected:
                    log.error('powerd', 'Lost contact with dehumidifier switch')
                    print('error: failed to connect to Dehumidifier switch')
                    print(exception)

                self._port_connected = False
                print('Will retry in 10 seconds...')
                time.sleep(10.)

    def status(self):
        """Return a dictionary of parameter values for this device"""
        with self._updated_condition:
            return {self.parameters[0].name: self._enabled}

    def get_parameter(self, parameter_name):
        """Returns the value of a named parameter"""
        if parameter_name != self.parameters[0].name:
            return False

        with self._updated_condition:
            return self._enabled

    def set_parameter(self, parameter_name, value):
        """Sets the value of a named parameter"""
        if parameter_name != self.parameters[0].name:
            return False

        with self._updated_condition:
            # Already in the desired state?
            if self._desired_enabled == value and self._enabled == value:
                return True

            # Wait for the change to apply
            # Arduino reports every 0.5s, so 1.5s should always be sufficient
            self._desired_enabled = value
            self._updated_condition.wait(1.5)

        return self._enabled == self._desired_enabled

    def set_light(self, enabled):
        """Sets the button LED status"""
        self._desired_button_light = enabled