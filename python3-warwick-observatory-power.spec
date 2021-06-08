Name:           python3-warwick-observatory-power
Version:        20210608
Release:        0
License:        GPL3
Summary:        Common backend code for the power daemon.
Url:            https://github.com/warwick-one-metre/powerd
BuildArch:      noarch
Requires:       python3-pyserial, python3-jsonschema

%description

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
