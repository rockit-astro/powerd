Name:           python3-warwick-observatory-power
Version:        2.8.0
Release:        0
License:        GPL3
Summary:        Common backend code for the Warwick one-metre and RASA prototype telescopes power daemon
Url:            https://github.com/warwick-one-metre/environmentd
BuildArch:      noarch
Requires:       python3-pyserial, python3-jsonschema

%description
Part of the observatory software for the Warwick one-meter and RASA prototype telescopes.

python3-warwick-observatory-power holds the common power code.

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
