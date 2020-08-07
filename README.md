## W1m Power daemon [![Travis CI build status](https://travis-ci.org/warwick-one-metre/powerd.svg?branch=master)](https://travis-ci.org/warwick-one-metre/powerd)

Part of the observatory software for the Warwick La Palma telescopes.

`powerd` is a Pyro frontend for interacting with the PDUs and UPSes.

`power` is a commandline utility that interfaces with the power system daemon.

`light` is a commandline utility to swith the dome light on and off.

`python3-warwick-observatory-power` is a python module with the common power code.

See [Software Infrastructure](https://github.com/warwick-one-metre/docs/wiki/Software-Infrastructure) for an overview of the W1m software architecture and instructions for developing and deploying the code.

### Software Setup

After installing `observatory-power-server`, the `powerd` must be enabled using:
```
sudo systemctl enable powerd.service@<telescope>
```
where `<telescope>` can be `onemetre` or `rasa`.

The service will automatically start on system boot, or you can start it immediately using:
```
sudo systemctl start powerd.service@<telescope>
```

Finally, open a port in the firewall so that other machines on the network can query the power status:
```
sudo firewall-cmd --zone=public --add-port=<port>/tcp --permanent
sudo firewall-cmd --reload
```

where `<port>` is 9009 for the onemetre and 9033 for the RASA (defined in the daemon config).

### Configuration

The onemetre [dehumidifier switch](https://github.com/warwick-one-metre/dehumidifier-switch) is matched against its unique serial number.  If the Arduino is replaced then the serial number should be updated in `10-onemetre-dome-power.rules`.

The IPs and port configurations for PDUs etc are defined in the json config files.

The `power` and `light` scripts define a dictionary defining which daemon should be controlled based on the IP of the system running the script.
