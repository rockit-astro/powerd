Name:      onemetre-power-server
Version:   2.0.1
Release:   0
Url:       https://github.com/warwick-one-metre/powerd
Summary:   Power system daemon for the Warwick one-metre telescope.
License:   GPL-3.0
Group:     Unspecified
BuildArch: noarch
%if 0%{?suse_version}
Requires:  python3, python34-Pyro4, python34-warwick-observatory-common, python34-warwick-w1m-power, observatory-log-client, net-snmp, %{?systemd_requires}
BuildRequires: systemd-rpm-macros
%endif
%if 0%{?centos_ver}
Requires:  python34, python34-Pyro4, python34-warwick-observatory-common, python34-warwick-w1m-power, observatory-log-client, net-snmp, %{?systemd_requires}
%endif

%description
Part of the observatory software for the Warwick one-meter telescope.

powerd is a Pyro frontend for interacting with the PDUs and UPSes via SNMP.

%build
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_udevrulesdir}

%{__install} %{_sourcedir}/powerd %{buildroot}%{_bindir}
%{__install} %{_sourcedir}/powerd.service %{buildroot}%{_unitdir}
%{__install} %{_sourcedir}/10-onemetre-power.rules %{buildroot}%{_udevrulesdir}

%pre
%if 0%{?suse_version}
%service_add_pre powerd.service
%endif

%post
%if 0%{?suse_version}
%service_add_post powerd.service
%endif
%if 0%{?centos_ver}
%systemd_post powerd.service
%endif

%preun
%if 0%{?suse_version}
%stop_on_removal powerd.service
%service_del_preun powerd.service
%endif
%if 0%{?centos_ver}
%systemd_preun powerd.service
%endif

%postun
%if 0%{?suse_version}
%restart_on_update powerd.service
%service_del_postun powerd.service
%endif
%if 0%{?centos_ver}
%systemd_postun_with_restart powerd.service
%endif

%files
%defattr(0755,root,root,-)
%{_bindir}/powerd
%defattr(0644,root,root,-)
%{_udevrulesdir}/10-onemetre-power.rules
%{_unitdir}/powerd.service

%changelog
