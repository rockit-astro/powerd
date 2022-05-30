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

"""Helper function to validate and parse the json config file"""

import json
from warwick.observatory.common import daemons, IP, validation

from .apc_device import (
    APCPDUSocketParameter,
    APCUPSSocketGroupParameter,
    APCUPSStatusParameter,
    APCUPSBatteryRemainingParameter,
    APCUPSBatteryHealthyParameter,
    APCUPSOutputLoadParameter,
    APCATSInputSourceParameter)
from .apcaccess_device import (
    APCAccessDevice,
    APCAccessUPSStatusParameter,
    APCAccessUPSBatteryRemainingParameter,
    APCAccessUPSBatteryHealthyParameter,
    APCAccessUPSOutputLoadParameter)
from .dehumidifier_switch_device import DehumidifierParameter, DehumidifierSwitchDevice
from .domealert_device import DomeAlertDevice
from .eth002_device import ETH002SwitchParameter, ETH002Device
from .netgear_device import NetgearPoESocketParameter
from .snmp_device import SNMPDevice
from .battery_voltmeter import BatteryVoltmeterDevice, VoltageParameter
from .dummy_device import DummyDevice, DummyUPSDevice

CONFIG_SCHEMA = {
    'type': 'object',
    'additionalProperties': False,
    'required': ['daemon', 'log_name', 'control_machines', 'devices'],
    'properties': {
        'daemon': {
            'type': 'string',
            'daemon_name': True
        },
        'log_name': {
            'type': 'string',
        },
        'control_machines': {
            'type': 'array',
            'items': {
                'type': 'string',
                'machine_name': True
            }
        },
        'dashboard_machine': {
            'type': 'string',
            'machine_name': True
        },
        'dashboard_toggleable_channels': {
            'type': 'array',
            'items': {
                'type': 'string',
            }
        },
        'devices': {
            'type': 'array',
            'items': {
                'type': 'object',
                'additionalProperties': False,
                'required': ['type'],
                'properties': {
                    'type': {
                        'type': 'string',
                        # These must also be defined in the 'anyOf' cases below
                        'enum': [
                            'APCPDU', 'APCUPS', 'APCAccessUPS', 'APCATS',
                            'DomeAlert', 'NetgearPOE', 'ETH002',
                            'BatteryVoltmeter',
                            'Dummy', 'DummyUPS',
                            'ArduinoRelay'
                        ]
                    },

                    # Used by APCPDU, APCUPS, APCATS, NetgearPOE, ETH002
                    'ip': {
                        'type': 'string',
                    },

                    # Used by APCPDU, APCUPS, APCAccessUPS, APCATS, DomeAlert, NetgearPOE, ETH002
                    'query_timeout': {
                        'type': 'number',
                        'min': 0,
                        'max': 30
                    },

                    # Used by APCPDU, Dummy
                    'sockets': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'additionalProperties': False,
                            'required': ['label', 'name', 'socket', 'display_order'],
                            'properties': {
                                'label': {
                                    'type': 'string',
                                },
                                'name': {
                                    'type': 'string',
                                },
                                'socket': {
                                    'type': 'number',
                                    'min': 1,
                                    'max': 8
                                },
                                'display_order': {
                                    'type': 'number'
                                }
                            }
                        }
                    },

                    # Used by APCUPS
                    'groups': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'additionalProperties': False,
                            'required': ['label', 'name', 'group', 'display_order'],
                            'properties': {
                                'label': {
                                    'type': 'string',
                                },
                                'name': {
                                    'type': 'string',
                                },
                                'group': {
                                    'type': 'number',
                                    'min': 1,
                                    'max': 4
                                },
                                'display_order': {
                                    'type': 'number'
                                }
                            }
                        }
                    },

                    # Used by APCUPS, APCATS, ArduinoRelay, DummyUPS, DomeAlert
                    'name': {
                        'type': 'string',
                    },
                    'label': {
                        'type': 'string',
                    },
                    'display_order': {
                        'type': 'number'
                    },

                    # Used by DomeAlert
                    'daemon': {
                        'type': 'string',
                        'daemon_name': True
                    },

                    # Used by NetgearPOE
                    'ports': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'additionalProperties': False,
                            'required': ['label', 'name', 'port', 'display_order'],
                            'properties': {
                                'label': {
                                    'type': 'string',
                                },
                                'name': {
                                    'type': 'string',
                                },
                                'port': {
                                    'type': 'number',
                                    'min': 1,
                                    'max': 24
                                },
                                'display_order': {
                                    'type': 'number'
                                }
                            }
                        }
                    },

                    # Used by ETH002
                    'relays': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'additionalProperties': False,
                            'required': ['label', 'name', 'relay', 'display_order'],
                            'properties': {
                                'label': {
                                    'type': 'string',
                                },
                                'name': {
                                    'type': 'string',
                                },
                                'relay': {
                                    'type': 'number',
                                    'min': 0,
                                    'max': 1
                                },
                                'display_order': {
                                    'type': 'number'
                                }
                            }
                        }
                    },

                    # Used by ArduinoRelay, BatteryVoltmeter, APCAccessUPS
                    'device': {
                        'type': 'string',
                    }
                },
                'anyOf': [
                    {
                        'properties': {
                            'type': {
                                'enum': ['APCPDU']
                            }
                        },
                        'required': ['ip', 'query_timeout', 'sockets']
                    },
                    {
                        'properties': {
                            'type': {
                                'enum': ['APCUPS', 'APCATS']
                            }
                        },
                        'required': ['ip', 'query_timeout', 'name', 'label']
                    },
                    {
                        'properties': {
                            'type': {
                                'enum': ['APCAccessUPS']
                            }
                        },
                        'required': ['device', 'query_timeout', 'name', 'label']
                    },
                    {
                        'properties': {
                            'type': {
                                'enum': ['NetgearPOE']
                            }
                        },
                        'required': ['ip', 'query_timeout', 'ports']
                    },
                    {
                        'properties': {
                            'type': {
                                'enum': ['ETH002']
                            }
                        },
                        'required': ['ip', 'query_timeout', 'relays']
                    },
                    {
                        'properties': {
                            'type': {
                                'enum': ['ArduinoRelay']
                            }
                        },
                        'required': ['device', 'name', 'label']
                    },
                    {
                        'properties': {
                            'type': {
                                'enum': ['DomeAlert']
                            }
                        },
                        'required': ['daemon', 'name', 'label', 'query_timeout']
                    },
                    {
                        'properties': {
                            'type': {
                                'enum': ['BatteryVoltmeter']
                            }
                        },
                        'required': ['device', 'name', 'label']
                    },
                    {
                        'properties': {
                            'type': {
                                'enum': ['Dummy']
                            }
                        },
                        'required': ['sockets']
                    },
                    {
                        'properties': {
                            'type': {
                                'enum': ['DummyUPS']
                            }
                        },
                        'required': ['name', 'label']
                    }
                ],
            }
        }
    }
}


class Config:
    """Daemon configuration parsed from a json file"""
    def __init__(self, config_filename):
        # Will throw on file not found or invalid json
        with open(config_filename, 'r') as config_file:
            config_json = json.load(config_file)

        # Will throw on schema violations
        validation.validate_config(config_json, CONFIG_SCHEMA, {
            'daemon_name': validation.daemon_name_validator,
            'machine_name': validation.machine_name_validator
        })

        self.daemon = getattr(daemons, config_json['daemon'])
        self.log_name = config_json['log_name']
        self.control_ips = [getattr(IP, machine) for machine in config_json['control_machines']]
        self.dashboard_ip = getattr(IP, config_json['dashboard_machine'])
        self.dashboard_toggleable_parameters = config_json['dashboard_toggleable_channels']

        self._device_config = config_json['devices']

    def get_labels(self):
        """Returns an array mapping parameter names to display labels"""

        labels = []
        for config in self._device_config:
            if config['type'] == 'APCPDU':
                labels.extend([[s['name'], s['label'], 'switch', s['display_order']] for s in config['sockets']])

            elif config['type'] == 'APCUPS':
                labels.append([config['name'], config['label'], 'ups', config['display_order']])
                for g in config.get('groups', []):
                    labels.append([g['name'], g['label'], 'switch', g['display_order']])

            elif config['type'] == 'APCAccessUPS':
                labels.append([config['name'], config['label'], 'ups', config['display_order']])

            elif config['type'] == 'APCATS':
                labels.append([config['name'], config['label'], 'ats', config['display_order']])

            elif config['type'] == 'NetgearPOE':
                labels.extend([[p['name'], p['label'], 'switch', p['display_order']] for p in config['ports']])

            elif config['type'] == 'ETH002':
                labels.extend([[r['name'], r['label'], 'switch', r['display_order']] for r in config['relays']])

            elif config['type'] == 'ArduinoRelay':
                labels.append([config['name'], config['label'], 'switch', config['display_order']])

            elif config['type'] == 'DomeAlert':
                labels.append([config['name'], config['label'], 'switch', config['display_order']])

            elif config['type'] == 'BatteryVoltmeter':
                labels.append([config['name'], config['label'], 'voltage', config['display_order']])

            if config['type'] == 'Dummy':
                labels.extend([[s['name'], s['label'], 'switch', s['display_order']] for s in config['sockets']])

            elif config['type'] == 'DummyUPS':
                labels.append([config['name'], config['label'], 'ups', config['display_order']])

        labels.sort(key=lambda x: x[3])
        return [{'name': l[0], 'label': l[1], 'type': l[2]} for l in labels]

    def get_devices(self, power_daemon):
        """Returns a list of devices wrapped by the power daemon"""
        ret = []
        for config in self._device_config:
            if config['type'] == 'APCPDU':
                parameters = [APCPDUSocketParameter(s['name'], s['socket']) for s in config['sockets']]
                ret.append(SNMPDevice(self.log_name, config['ip'], parameters, config['query_timeout']))

            elif config['type'] == 'APCUPS':
                parameters = [
                    APCUPSStatusParameter(config['name'] + '_status'),
                    APCUPSBatteryRemainingParameter(config['name'] + '_battery_remaining'),
                    APCUPSBatteryHealthyParameter(config['name'] + '_battery_healthy'),
                    APCUPSOutputLoadParameter(config['name'] + '_load'),
                ]

                for g in config.get('groups', []):
                    parameters.append(APCUPSSocketGroupParameter(g['name'], g['group']))

                ret.append(SNMPDevice(self.log_name, config['ip'], parameters, config['query_timeout']))

            elif config['type'] == 'APCAccessUPS':
                parameters = [
                    APCAccessUPSStatusParameter(config['name'] + '_status'),
                    APCAccessUPSBatteryRemainingParameter(config['name'] + '_battery_remaining'),
                    APCAccessUPSBatteryHealthyParameter(config['name'] + '_battery_healthy'),
                    APCAccessUPSOutputLoadParameter(config['name'] + '_load'),
                ]

                ret.append(APCAccessDevice(self.log_name, config['device'], config['query_timeout'], parameters))

            elif config['type'] == 'APCATS':
                parameters = [
                    APCATSInputSourceParameter(config['name'] + '_source')
                ]

                ret.append(SNMPDevice(self.log_name, config['ip'], parameters, config['query_timeout']))

            elif config['type'] == 'NetgearPOE':
                parameters = [NetgearPoESocketParameter(p['name'], p['port']) for p in config['ports']]
                ret.append(SNMPDevice(self.log_name, config['ip'], parameters, config['query_timeout']))

            elif config['type'] == 'ETH002':
                parameters = [ETH002SwitchParameter(p['name'], p['relay']) for p in config['relays']]
                ret.append(ETH002Device(self.log_name, config['ip'], parameters, config['query_timeout']))

            elif config['type'] == 'ArduinoRelay':
                ret.append(DehumidifierSwitchDevice(
                    self.log_name, config['device'],
                    DehumidifierParameter(config['name']), power_daemon))

            elif config['type'] == 'DomeAlert':
                ret.append(DomeAlertDevice(
                    self.log_name, getattr(daemons, config['daemon']), config['name'], config['query_timeout']
                ))

            elif config['type'] == 'BatteryVoltmeter':
                ret.append(BatteryVoltmeterDevice(self.log_name, config['device'], [
                    VoltageParameter(config['name']),
                    VoltageParameter(config['name'] + '_mean')
                ]))

            elif config['type'] == 'Dummy':
                parameters = [APCPDUSocketParameter(s['name'], s['socket']) for s in config['sockets']]
                ret.append(DummyDevice(parameters))

            elif config['type'] == 'DummyUPS':
                parameters = [
                    APCUPSStatusParameter(config['name'] + '_status'),
                    APCUPSBatteryRemainingParameter(config['name'] + '_battery_remaining'),
                    APCUPSBatteryHealthyParameter(config['name'] + '_battery_healthy'),
                    APCUPSOutputLoadParameter(config['name'] + '_load'),
                ]

                ret.append(DummyUPSDevice(parameters))

        return ret
