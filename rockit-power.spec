Name:      rockit-power
Version:   %{_version}
Release:   1
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
mkdir -p %{buildroot}%{_udevrulesdir}

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
%{__install} %{_sourcedir}/config/superwasp.json %{buildroot}%{_sysconfdir}/powerd/
%{__install} %{_sourcedir}/config/10-superwasp-power.rules %{buildroot}%{_udevrulesdir}

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

%package data-superwasp
Summary: Power control data for the SuperWASP telescope
Group:   Unspecified
%description data-superwasp

%files data-superwasp
%defattr(0644,root,root,-)
%{_udevrulesdir}/10-superwasp-power.rules
%{_sysconfdir}/powerd/superwasp.json

%changelog
