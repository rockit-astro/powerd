## W1m Power daemon [![Travis CI build status](https://travis-ci.org/warwick-one-metre/powerd.svg?branch=master)](https://travis-ci.org/warwick-one-metre/powerd)

Part of the observatory software for the Warwick one-meter telescope.

`powerd` is a Pyro frontend for interacting with the PDUs and UPSes.

`power` is a commandline utility that interfaces with the power system daemon.

`light` is a commandline utility to swith the dome light on and off.

`python36-warwick-observatory-power` is a python module with the common power code.

See [Software Infrastructure](https://github.com/warwick-one-metre/docs/wiki/Software-Infrastructure) for an overview of the W1m software architecture and instructions for developing and deploying the code.

### Software Setup (W1m)

After installing `onemetre-power-server`, the `powerd` must be enabled using:
```
sudo systemctl enable powerd.service
```

The service will automatically start on system boot, or you can start it immediately using:
```
sudo systemctl start powerd.service
```

Finally, open a port in the firewall so that other machines on the network can query the power status:
```
sudo firewall-cmd --zone=public --add-port=9009/tcp --permanent
sudo firewall-cmd --reload
```

### Software Setup (RASA)

After installing `rasa-power-server`, the `powerd` must be enabled using:
```
sudo systemctl enable rasa_powerd.service
```

The service will automatically start on system boot, or you can start it immediately using:
```
sudo systemctl start rasa_powerd.service
```

Finally, open a port in the firewall so that other machines on the network can query the power status:
```
sudo firewall-cmd --zone=public --add-port=9033/tcp --permanent
sudo firewall-cmd --reload
```

### Hardware Setup (W1m)

The [dehumidifier switch](https://github.com/warwick-one-metre/dehumidifier-switch) is matched against its unique serial number.  If the Arduino is replaced then the serial number should be updated in `10-onemetre-dome-power.rules`.

The IPs for the SNMP devices (PDUs, UPSes, network switch) are hardcoded in `warwick/observatory/power/onemetre_config.py`.

### Hardware Setup (RASA)

The IPs for the SNMP devices (PDUs, UPSes, network switch) are hardcoded in `warwick/observatory/power/rasa_config.py`.
