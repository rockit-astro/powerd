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
import sys
import traceback
import jsonschema
from warwick.observatory.common import daemons, IP

from .apc_device import (
    APCPDUSocketParameter,
    APCUPSSocketGroupParameter,
    APCUPSStatusParameter,
    APCUPSBatteryRemainingParameter,
    APCUPSBatteryHealthyParameter,
    APCUPSOutputLoadParameter)
from .apcaccess_device import (
    APCAccessDevice,
    APCAccessUPSStatusParameter,
    APCAccessUPSBatteryRemainingParameter,
    APCAccessUPSBatteryHealthyParameter,
    APCAccessUPSOutputLoadParameter)
from .domealert_device import DomeAlertDevice
from .eth002_device import ETH002SwitchParameter, ETH002Device
from .netgear_device import NetgearPoESocketParameter
from .snmp_device import SNMPDevice
from .battery_voltmeter import BatteryVoltmeterDevice, VoltageParameter

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
                            'APCPDU', 'APCUPS', 'APCAccessUPS',
                            'DomeAlert', 'NetgearPOE', 'ETH002',
                            'BatteryVoltmeter'
                        ]
                    },

                    # Used by APCPDU, APCUPS, NetgearPOE, ETH002
                    'ip': {
                        'type': 'string',
                    },

                    # Used by APCPDU, APCUPS, APCAccessUPS, DommeAlert, NetgearPOE, ETH002
                    'query_timeout': {
                        'type': 'number',
                        'min': 0,
                        'max': 30
                    },

                    # Used by APCPDU
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

                    # Used by APCUPS, DomeAlert
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

                    # Used by BatteryVoltmeter, APCAccessUPS
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
                                'enum': ['APCUPS']
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
                    }
                ],
            }
        }
    }
}


class ConfigSchemaViolationError(Exception):
    """Exception used to report schema violations"""
    def __init__(self, errors):
        message = 'Invalid configuration:\n\t' + '\n\t'.join(errors)
        super(ConfigSchemaViolationError, self).__init__(message)


def __create_validator():
    """Returns a template validator that includes support for the
       custom schema tags used by the observation schedules:
            daemon_name: add to string properties to require they match an entry in the
                         warwick.observatory.common.daemons address book
            machine_name: add to string properties to require they match an entry in the
                         warwick.observatory.common.IP address book
    """
    validators = dict(jsonschema.Draft4Validator.VALIDATORS)

    # pylint: disable=unused-argument
    def daemon_name(validator, value, instance, schema):
        """Validate a string as a valid daemon name"""
        try:
            getattr(daemons, instance)
        except Exception:
            yield jsonschema.ValidationError('{} is not a valid daemon name'.format(instance))

    def machine_name(validator, value, instance, schema):
        """Validate a string as a valid machine name"""
        try:
            getattr(IP, instance)
        except Exception:
            yield jsonschema.ValidationError('{} is not a valid machine name'.format(instance))
    # pylint: enable=unused-argument

    validators['daemon_name'] = daemon_name
    validators['machine_name'] = machine_name
    return jsonschema.validators.create(meta_schema=jsonschema.Draft4Validator.META_SCHEMA,
                                        validators=validators)


def validate_config(config_json):
    """Tests whether a json object defines a valid environment config file
       Raises SchemaViolationError on error
    """
    errors = []
    try:
        validator = __create_validator()
        for error in sorted(validator(CONFIG_SCHEMA).iter_errors(config_json),
                            key=lambda e: e.path):
            if error.path:
                path = '->'.join([str(p) for p in error.path])
                message = path + ': ' + error.message
            else:
                message = error.message
            errors.append(message)
    except Exception:
        traceback.print_exc(file=sys.stdout)
        errors = ['exception while validating']

    if errors:
        raise ConfigSchemaViolationError(errors)


class Config:
    """Daemon configuration parsed from a json file"""
    def __init__(self, config_filename):
        # Will throw on file not found or invalid json
        with open(config_filename, 'r') as config_file:
            config_json = json.load(config_file)

        # Will throw on schema violations
        validate_config(config_json)

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

            elif config['type'] == 'NetgearPOE':
                labels.extend([[p['name'], p['label'], 'switch', p['display_order']] for p in config['ports']])

            elif config['type'] == 'ETH002':
                labels.extend([[r['name'], r['label'], 'switch', r['display_order']] for r in config['relays']])

            elif config['type'] == 'DomeAlert':
                labels.append([config['name'], config['label'], 'switch', config['display_order']])

            elif config['type'] == 'BatteryVoltmeter':
                labels.append([config['name'], config['label'], 'voltage', config['display_order']])

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

            elif config['type'] == 'APCAccessUPS':
                parameters = [
                    APCAccessUPSStatusParameter(config['name'] + '_status'),
                    APCAccessUPSBatteryRemainingParameter(config['name'] + '_battery_remaining'),
                    APCAccessUPSBatteryHealthyParameter(config['name'] + '_battery_healthy'),
                    APCAccessUPSOutputLoadParameter(config['name'] + '_load'),
                ]

                ret.append(APCAccessDevice(self.log_name, config['device'], config['query_timeout'], parameters))

            elif config['type'] == 'NetgearPOE':
                parameters = [NetgearPoESocketParameter(p['name'], p['port']) for p in config['ports']]
                ret.append(SNMPDevice(self.log_name, config['ip'], parameters, config['query_timeout']))

            elif config['type'] == 'ETH002':
                parameters = [ETH002SwitchParameter(p['name'], p['relay']) for p in config['relays']]
                ret.append(ETH002Device(self.log_name, config['ip'], parameters, config['query_timeout']))

            elif config['type'] == 'DomeAlert':
                ret.append(DomeAlertDevice(
                    self.log_name, getattr(daemons, config['daemon']), config['name'], config['query_timeout']
                ))

            elif config['type'] == 'BatteryVoltmeter':
                ret.append(BatteryVoltmeterDevice(self.log_name, config['device'], VoltageParameter(config['name'])))

        return ret
