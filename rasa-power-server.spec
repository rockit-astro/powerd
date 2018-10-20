Name:      rasa-power-server
Version:   2.3.2
Release:   0
Url:       https://github.com/warwick-one-metre/powerd
Summary:   Power system daemon for the RASA prototype telescope.
License:   GPL-3.0
Group:     Unspecified
BuildArch: noarch
Requires:  python34, python34-Pyro4, python34-warwick-observatory-common, python34-warwick-observatory-power, observatory-log-client, net-snmp-utils, %{?systemd_requires}

%description
Part of the observatory software for the RASA prototype telescope.

powerd is a Pyro frontend for interacting with the PDUs and UPSes via SNMP.

%build
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_udevrulesdir}

%{__install} %{_sourcedir}/powerd %{buildroot}%{_bindir}
%{__install} %{_sourcedir}/rasa_powerd.service %{buildroot}%{_unitdir}

%post
%systemd_post rasa_powerd.service

%preun
%systemd_preun rasa_powerd.service

%postun
%systemd_postun_with_restart rasa_powerd.service

%files
%defattr(0755,root,root,-)
%{_bindir}/powerd
%defattr(0644,root,root,-)
%{_unitdir}/rasa_powerd.service

%changelog
