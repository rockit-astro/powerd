## Power control daemon

`powerd` is a Pyro frontend for interacting with the PDUs and UPSes.

`power` is a commandline utility that interfaces with the power system daemon.

`light` is a commandline utility to switch the dome light on and off.

See [Software Infrastructure](https://github.com/warwick-one-metre/docs/wiki/Software-Infrastructure) for an overview of the software architecture and instructions for developing and deploying the code.

### Configuration

Configuration is read from json files that are installed by default to `/etc/powerd`.
A configuration file is specified when launching the power server, and the `power` frontend will search this location when launched.

```python
{
  "daemon": "localhost_test", # Run the server as this daemon. Daemon types are registered in `warwick.observatory.common.daemons`.
  "log_name": "powerd", # The name to use when writing messages to the observatory log.
  "control_machines": ["LocalHost"], # Machine names that are allowed to control (rather than just query) state. Machine names are registered in `warwick.observatory.common.IP`.
  "dashboard_machine": "GOTOServer", # Machine name that is allowed to call the `dashboard_switch` method to control lights from the web UI.
  "dashboard_toggleable_channels": ["light"], # Switch names that are allowed to be toggled by `dasboard_switch`.
  "devices": [
    {
      "type": "Dummy", # APCPDU, APCUPS, APCAccessUPS, DomeAlert, NetgearPOE, ETH002, BatteryVoltmeter, Dummy, DummyUPS
      "sockets": [ # Type-specific configuration. See existing config definitions and config.py for details
        {
          "socket": 1,
          "name": "test",
          "label": "Test Socket",
          "display_order": 1
        }
      ]
    }
  ]
}
```

### Initial Installation

The automated packaging scripts will push 6 RPM packages to the observatory package repository:

| Package           | Description |
| ----------------- | ------ |
| observatory-power-server | Contains the `pipelined` server and systemd service file. |
| observatory-power-client | Contains the `pipeline` commandline utility for controlling the power server. |
| python3-warwick-observatory-power | Contains the python module with shared code. |
| onemetre-power-data | Contains the json configuration and udev rules for the W1m. |
| superwasp-power-data | Contains the json configuration and udev rules for SuperWASP. |
| clasp-power-data | Contains the json configuration and udev rules for the CLASP telescope. |
| goto-power-data | Contains the json configuration for the GOTO UPS monitoring. |


`observatory-power-server` and `observatory-power-client` and `onemetre-power-data` packages should be installed on the `onemetre-dome` machine.
`observatory-power-server` and `observatory-power-client` and `clasp-power-data` packages should be installed on the `clasp-tcs` machine.
`observatory-power-server` and `observatory-power-client` and `superwasp-power-data` and `goto-power-data` packages should be installed on the `gotoserver` machine.

After installing packages, the systemd service should be enabled:

```
sudo systemctl enable powerd@<config>
sudo systemctl start powerd@<config>
```

where `config` is the name of the json file for the appropriate telescope (`onemetre` for `onemetre-dome`, `superwasp` *and* `goto` for `gotoserver`).

Now open a port in the firewall:
```
sudo firewall-cmd --zone=public --add-port=<port>/tcp --permanent
sudo firewall-cmd --reload
```
where `port` is the port defined in `warwick.observatory.common.daemons` for the daemon specified in the power config.

### Upgrading Installation

New RPM packages are automatically created and pushed to the package repository for each push to the `master` branch.
These can be upgraded locally using the standard system update procedure:
```
sudo yum clean expire-cache
sudo yum update
```

The daemon should then be restarted to use the newly installed code:
```
sudo systemctl stop powerd@<config>
sudo systemctl start powerd@<config>
```

### Testing Locally

The power server and client can be run directly from a git clone:
```
./powerd test.json
POWERD_CONFIG_PATH=./test.json ./power status
```
