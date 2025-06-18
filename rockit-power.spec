Name:      rockit-power
Version:   %{_version}
Release:   1%{dist}
Summary:   Power control
Url:       https://github.com/rockit-astro/powerd
License:   GPL-3.0
BuildArch: noarch

%description


%build
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}/etc/bash_completion.d
mkdir -p %{buildroot}%{_sysconfdir}/powerd/

%{__install} %{_sourcedir}/power %{buildroot}%{_bindir}
%{__install} %{_sourcedir}/light %{buildroot}%{_bindir}
%{__install} %{_sourcedir}/powerd %{buildroot}%{_bindir}
%{__install} %{_sourcedir}/powerd@.service %{buildroot}%{_unitdir}
%{__install} %{_sourcedir}/completion/power %{buildroot}/etc/bash_completion.d
%{__install} %{_sourcedir}/completion/light %{buildroot}/etc/bash_completion.d

%{__install} %{_sourcedir}/config/clasp.json %{buildroot}%{_sysconfdir}/powerd/
%{__install} %{_sourcedir}/config/gotoupsmon.json %{buildroot}%{_sysconfdir}/powerd/
%{__install} %{_sourcedir}/config/halfmetre.json %{buildroot}%{_sysconfdir}/powerd/
%{__install} %{_sourcedir}/config/onemetre.json %{buildroot}%{_sysconfdir}/powerd/
%{__install} %{_sourcedir}/config/sting.json %{buildroot}%{_sysconfdir}/powerd/
%{__install} %{_sourcedir}/config/warwick.json %{buildroot}%{_sysconfdir}/powerd/
%{__install} %{_sourcedir}/config/ngts_m06.json %{buildroot}%{_sysconfdir}/powerd/

%package server
Summary:  Power control server
Group:    Unspecified
Requires: python3-rockit-power net-snmp-utils
%description server

%files server
%defattr(0755,root,root,-)
%{_bindir}/powerd
%defattr(0644,root,root,-)
%{_unitdir}/powerd@.service

%package client
Summary:  Power control client
Group:    Unspecified
Requires: python3-rockit-power
%description client

%files client
%defattr(0755,root,root,-)
%{_bindir}/power
%{_bindir}/light
/etc/bash_completion.d/power
/etc/bash_completion.d/light

%package data-clasp
Summary: Power control data for the CLASP telescope
Group:   Unspecified
%description data-clasp

%files data-clasp
%defattr(0644,root,root,-)
%{_sysconfdir}/powerd/clasp.json

%package data-gotoups
Summary: Power control data for monitoring the GOTO UPSes
Group:   Unspecified
%description data-gotoups

%files data-gotoups
%defattr(0644,root,root,-)
%{_sysconfdir}/powerd/gotoupsmon.json

%package data-halfmetre
Summary: Power control data for the 0.5m telescope
Group:   Unspecified
%description data-halfmetre

%files data-halfmetre
%defattr(0644,root,root,-)
%{_sysconfdir}/powerd/halfmetre.json

%package data-onemetre
Summary: Power control data for the W1m telescope
Group:   Unspecified
%description data-onemetre

%files data-onemetre
%defattr(0644,root,root,-)
%{_sysconfdir}/powerd/onemetre.json

%package data-sting
Summary: Power control data for the STING telescope
Group:   Unspecified
%description data-sting

%files data-sting
%defattr(0644,root,root,-)
%{_sysconfdir}/powerd/sting.json

%package data-warwick
Summary: Power control data for the Windmill Hill Observatory telescope
Group:   Unspecified
%description data-warwick

%files data-warwick
%defattr(0644,root,root,-)
%{_sysconfdir}/powerd/warwick.json

%package data-ngts-m06
Summary: Power control data for NGTS M06
Group:   Unspecified
%description data-ngts-m06

%files data-ngts-m06
%defattr(0644,root,root,-)
%{_sysconfdir}/powerd/ngts_m06.json

%changelog
