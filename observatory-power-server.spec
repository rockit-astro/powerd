Name:      observatory-power-server
Version:   2.6.1
Release:   0
Url:       https://github.com/warwick-one-metre/powerd
Summary:   Power system daemon for the Warwick La Palma telescopes.
License:   GPL-3.0
Group:     Unspecified
BuildArch: noarch
Requires:  python3, python3-Pyro4, python3-warwick-observatory-common, python3-warwick-observatory-power
Requires:  observatory-log-client, net-snmp-utils, %{?systemd_requires}

%description
Part of the observatory software for the Warwick La Palma telescopes.

powerd is a Pyro frontend for interacting with the PDUs and UPSes via SNMP.

%build
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_udevrulesdir}
mkdir -p %{buildroot}%{_sysconfdir}/powerd/

%{__install} %{_sourcedir}/powerd %{buildroot}%{_bindir}
%{__install} %{_sourcedir}/powerd@.service %{buildroot}%{_unitdir}
%{__install} %{_sourcedir}/10-onemetre-power.rules %{buildroot}%{_udevrulesdir}
%{__install} %{_sourcedir}/onemetre.json %{buildroot}%{_sysconfdir}/powerd/
%{__install} %{_sourcedir}/rasa.json %{buildroot}%{_sysconfdir}/powerd/
%{__install} %{_sourcedir}/superwasp.json %{buildroot}%{_sysconfdir}/powerd/

%files
%defattr(0755,root,root,-)
%{_bindir}/powerd
%defattr(0644,root,root,-)
%{_udevrulesdir}/10-onemetre-power.rules
%{_unitdir}/powerd@.service
%{_sysconfdir}/powerd/onemetre.json
%{_sysconfdir}/powerd/rasa.json
%{_sysconfdir}/powerd/superwasp.json

%changelog
