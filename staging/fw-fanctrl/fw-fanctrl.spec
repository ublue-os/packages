%global jobid 899
%global debug_package %{nil}

%global reponame    fw-fanctrl
%global commit      e2a2eb92ead5b87222504e9819515f09300ccc39
%global commit_date 20250302
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global gitrel      .%{commit_date}.git%{shortcommit}

Name:           fw-fanctrl
Version:        0.0.0
Release:        9%{gitrel}%{?dist}
Summary:        Framework FanControl Software

License:        BSD-3-Clause
URL:            https://github.com/TamtamHero/%{name}
Source0:        https://github.com/TamtamHero/%{name}/archive/%{commit}/%{reponame}-%{shortcommit}.tar.gz

BuildRequires:  systemd-rpm-macros
Requires:       python3
Requires:       fw-ectool

%description
Framework Fan control script

%prep
%autosetup -n %{name}-%{commit}

%build
chmod +x fanctrl.py
chmod +x services/system-sleep/%{name}-suspend
sed -i "s/%PREFIX_DIRECTORY%/\/usr/g" services/%{name}.service
sed -i "s/%PREFIX_DIRECTORY%/\/usr/g" services/system-sleep/%{name}-suspend
sed -i "s/%NO_BATTERY_SENSOR_OPTION%//g" services/%{name}.service
sed -i "s/%SYSCONF_DIRECTORY%/\/etc/g" services/%{name}.service

%install
install -Dm755 fanctrl.py %{buildroot}%{_bindir}/fanctrl.py
install -Dm755 fanctrl.py %{buildroot}%{_bindir}/fw-fanctrl
install -Dm644 services/system-sleep/%{name}-suspend %{buildroot}%{_libdir}/systemd/system-sleep/%{name}-suspend
install -Dm755 services/%{name}.service %{buildroot}%{_unitdir}/%{name}.service
install -Dm755 config.json %{buildroot}%{_sysconfdir}/%{name}/config.json


%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%files
%license LICENSE
%{_unitdir}/%{name}.service
%{_sysconfdir}/%{name}/config.json
%{_libdir}/systemd/system-sleep/%{name}-suspend
%attr(0755,root,root) %{_bindir}/fanctrl.py
%attr(0755,root,root) %{_bindir}/fw-fanctrl

%changelog
%autochangelog
