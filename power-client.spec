Name:      onemetre-power-client
Version:   1.12
Release:   0
Url:       https://github.com/warwick-one-metre/powerd
Summary:   Power system client for the Warwick one-metre telescope.
License:   GPL-3.0
Group:     Unspecified
BuildArch: noarch
Requires:  python3, python3-Pyro4, python3-warwickobservatory

%description
Part of the observatory software for the Warwick one-meter telescope.

power is a commandline utility that interfaces with the power system daemon.
light is a commandline utility to swith the dome light on and off.

%build
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}/etc/bash_completion.d
%{__install} %{_sourcedir}/power %{buildroot}%{_bindir}
%{__install} %{_sourcedir}/light %{buildroot}%{_bindir}
%{__install} %{_sourcedir}/completion/power %{buildroot}/etc/bash_completion.d/power
%{__install} %{_sourcedir}/completion/light %{buildroot}/etc/bash_completion.d/light

%files
%defattr(0755,root,root,-)
%{_bindir}/power
%{_bindir}/light
/etc/bash_completion.d/power
/etc/bash_completion.d/light

%changelog
