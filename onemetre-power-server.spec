Name:      onemetre-power-server
Version:   2.5.0
Release:   0
Url:       https://github.com/warwick-one-metre/powerd
Summary:   Power system daemon for the Warwick one-metre telescope.
License:   GPL-3.0
Group:     Unspecified
BuildArch: noarch
Requires:  python36, python36-Pyro4, python36-warwick-observatory-common, python36-warwick-observatory-power
Requires:  observatory-log-client, net-snmp-utils, %{?systemd_requires}

%description
Part of the observatory software for the Warwick one-meter telescope.

powerd is a Pyro frontend for interacting with the PDUs and UPSes via SNMP.

%build
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_udevrulesdir}
mkdir -p %{buildroot}%{_sysconfdir}/powerd/

%{__install} %{_sourcedir}/powerd %{buildroot}%{_bindir}
%{__install} %{_sourcedir}/powerd.service %{buildroot}%{_unitdir}
%{__install} %{_sourcedir}/10-onemetre-power.rules %{buildroot}%{_udevrulesdir}
%{__install} %{_sourcedir}/onemetre.json %{buildroot}%{_sysconfdir}/powerd/

%post
%systemd_post powerd.service

%preun
%systemd_preun powerd.service

%postun
%systemd_postun_with_restart powerd.service

%files
%defattr(0755,root,root,-)
%{_bindir}/powerd
%defattr(0644,root,root,-)
%{_udevrulesdir}/10-onemetre-power.rules
%{_unitdir}/powerd.service
%{_sysconfdir}/powerd/onemetre.json

%changelog
