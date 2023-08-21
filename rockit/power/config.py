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

"""Helper function to validate and parse the json config file"""

import json
from rockit.common import daemons, IP, validation

from .apc_device import (
    APCPDUSocketParameter,
    APCUPSSocketGroupParameter,
    APCUPSStatusParameter,
    APCUPSBatteryRemainingParameter,
    APCUPSBatteryHealthyParameter,
    APCUPSOutputLoadParameter,
    APCATSInputSourceParameter)
from .pyro_switch_device import PyroSwitchDevice
from .dummy_device import DummyDevice, DummyUPSDevice
from .netgear_device import NetgearPoESocketParameter
from .snmp_device import SNMPDevice
from .roof_device import RoofDevice

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
                            'APCPDU', 'APCUPS', 'APCATS',
                            'PyroSwitch', 'NetgearPOE', 'Roof',
                            'Dummy', 'DummyUPS'
                        ]
                    },

                    # Used by APCPDU, APCUPS, APCATS, NetgearPOE
                    'ip': {
                        'type': 'string',
                    },

                    # Used by APCPDU, APCUPS, APCATS, PyroSwitch, NetgearPOE, Roof
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

                    # Used by APCUPS, APCATS, DummyUPS, PyroSwitch, Roof
                    'name': {
                        'type': 'string',
                    },
                    'label': {
                        'type': 'string',
                    },
                    'display_order': {
                        'type': 'number'
                    },

                    # Used by PyroSwitch, Roof
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

                    # NetgearPOE (optional)
                    'community': {
                        'type': 'string'
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
                                'enum': ['PyroSwitch', 'Roof']
                            }
                        },
                        'required': ['daemon', 'name', 'label', 'query_timeout']
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
        with open(config_filename, 'r', encoding='utf-8') as config_file:
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

            elif config['type'] == 'APCATS':
                labels.append([config['name'], config['label'], 'ats', config['display_order']])

            elif config['type'] == 'NetgearPOE':
                labels.extend([[p['name'], p['label'], 'switch', p['display_order']] for p in config['ports']])

            elif config['type'] == 'PyroSwitch':
                labels.append([config['name'], config['label'], 'switch', config['display_order']])

            elif config['type'] == 'Roof':
                labels.append([config['name'], config['label'], 'voltage', config['display_order']])

            if config['type'] == 'Dummy':
                labels.extend([[s['name'], s['label'], 'switch', s['display_order']] for s in config['sockets']])

            elif config['type'] == 'DummyUPS':
                labels.append([config['name'], config['label'], 'ups', config['display_order']])

        labels.sort(key=lambda x: x[3])
        return [{'name': l[0], 'label': l[1], 'type': l[2]} for l in labels]

    def get_devices(self):
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

            elif config['type'] == 'APCATS':
                parameters = [
                    APCATSInputSourceParameter(config['name'] + '_source')
                ]

                ret.append(SNMPDevice(self.log_name, config['ip'], parameters, config['query_timeout']))

            elif config['type'] == 'NetgearPOE':
                parameters = [NetgearPoESocketParameter(p['name'], p['port']) for p in config['ports']]
                ret.append(SNMPDevice(self.log_name, config['ip'], parameters, config['query_timeout'],
                                      get_community=config.get('community', 'public'),
                                      set_community=config.get('community', 'private')))

            elif config['type'] == 'PyroSwitch':
                ret.append(PyroSwitchDevice(
                    self.log_name, getattr(daemons, config['daemon']), config['name'], config['query_timeout']
                ))

            elif config['type'] == 'Roof':
                ret.append(RoofDevice(
                    self.log_name, getattr(daemons, config['daemon']), config['name'], config['query_timeout']
                ))

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
