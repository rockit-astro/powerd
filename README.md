## Power control daemon ![Build Status](https://github.com/warwick-one-metre/powerd/workflows/RPM%20Packaging/badge.svg)

Part of the observatory software for the Warwick La Palma telescopes.

`powerd` is a Pyro frontend for interacting with the PDUs and UPSes.

`power` is a commandline utility that interfaces with the power system daemon.

`light` is a commandline utility to swith the dome light on and off.

`python3-warwick-observatory-power` is a python module with the common power code.

See [Software Infrastructure](https://github.com/warwick-one-metre/docs/wiki/Software-Infrastructure) for an overview of the W1m software architecture and instructions for developing and deploying the code.

### Software Setup

After installing `observatory-power-server`, the `powerd` must be enabled using:
```
sudo systemctl enable powerd@<telescope>
```
where `<telescope>` can be `onemetre`, `rasa`, `superwasp`, or `gotoupsmon`.

The service will automatically start on system boot, or you can start it immediately using:
```
sudo systemctl start powerd@<telescope>
```

Finally, open a port in the firewall so that other machines on the network can query the power status:
```
sudo firewall-cmd --zone=public --add-port=<port>/tcp --permanent
sudo firewall-cmd --reload
```

where `<port>` is (defined in the warwick-observatory-common daemon config):

| Telescope | Port |
| --------- | ---- |
| onemetre  | 9009 |
| RASA      | 9033 |
| SuperWASP | 9027 |
| GOTO (upsmon) | 9021 |


### Configuration

The IPs and port configurations for PDUs etc are defined in the json config files.

The `power` and `light` scripts define a dictionary defining which daemon should be controlled based on the IP of the system running the script.
