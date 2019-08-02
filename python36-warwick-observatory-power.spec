Name:           python36-warwick-observatory-power
Version:        2.5.0
Release:        0
License:        GPL3
Summary:        Common backend code for the Warwick one-metre and RASA prototype telescopes power daemon
Url:            https://github.com/warwick-one-metre/environmentd
BuildArch:      noarch
Requires:       python36-pyserial

%description
Part of the observatory software for the Warwick one-meter and RASA prototype telescopes.

python34-warwick-observatory-power holds the common power code.

%prep

rsync -av --exclude=build .. .

%build
%{__python3} setup.py build

%install
%{__python3} setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
