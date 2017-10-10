## W1m Power daemon [![Travis CI build status](https://travis-ci.org/warwick-one-metre/powerd.svg?branch=master)](https://travis-ci.org/warwick-one-metre/powerd)

Part of the observatory software for the Warwick one-meter telescope.

`powerd` is a Pyro frontend for interacting with the PDUs and UPSes.

`power` is a commandline utility that interfaces with the power system daemon.

`light` is a commandline utility to swith the dome light on and off.

`python34-warwick-w1m-power` is a python module with the common power code.

See [Software Infrastructure](https://github.com/warwick-one-metre/docs/wiki/Software-Infrastructure) for an overview of the W1m software architecture and instructions for developing and deploying the code.

### Software Setup

After installing `onemetre-power-server`, the `powerd` must be enabled using:
```
sudo systemctl enable powerd.service
```

The service will automatically start on system boot, or you can start it immediately using:
```
sudo systemctl start powerd.service
```

### Hardware Setup

The [dehumidifier switch](https://github.com/warwick-one-metre/dehumidifier-switch) is matched against its unique serial number.  If the Arduino is replaced then the serial number should be updated in `10-onemetre-dome-power.rules`.

The IPs for the SNMP devices (PDUs, UPSes, network switch) are hardcoded in `powerd`.
