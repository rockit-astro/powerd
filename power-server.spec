Name:      onemetre-power-server
Version:   1.13
Release:   1
Url:       https://github.com/warwick-one-metre/powerd
Summary:   Power system daemon for the Warwick one-metre telescope.
License:   GPL-3.0
Group:     Unspecified
BuildArch: noarch
Requires:  python3, python3-Pyro4, python3-warwickobservatory, onemetre-obslog-client, net-snmp, %{?systemd_requires}
BuildRequires: systemd-rpm-macros

%description
Part of the observatory software for the Warwick one-meter telescope.

powerd is a Pyro frontend for interacting with the PDUs and UPSes via SNMP.

%build
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_unitdir}

%{__install} %{_sourcedir}/powerd %{buildroot}%{_bindir}
%{__install} %{_sourcedir}/powerd.service %{buildroot}%{_unitdir}

%pre
%service_add_pre powerd.service

%post
%service_add_post powerd.service

%preun
%stop_on_removal powerd.service
%service_del_preun powerd.service

%postun
%restart_on_update powerd.service
%service_del_postun powerd.service

%files
%defattr(0755,root,root,-)
%{_bindir}/powerd
%defattr(-,root,root,-)
%{_unitdir}/powerd.service

%changelog
